"""
    author  : Tal Avraham
    Created : 5/28/2020
    Purpose : Implement the bot commands.
"""


# === Imports === #
from abc import ABC, abstractmethod
import logging
import config
from github_utils import GithubRepoInstaller, RepoInstallError
from minecraft.minecraft import Minecraft
from minecraft.minecraft_reconnector import MinecraftServerReconnector
from minecraft.captcha_detector import CaptchaDetector
import subprocess
import time
import functools
from enum import Enum

# === Constants === #
SEND_IMAGE_DELAY_SECS = 4
STATS_BORDER = '---------------------------\n'
END_OF_FILE = 2


class ReplyMsg(Enum):
    ERROR = "Woops! Something went wrong."
    START = "Hello master, how can i be of service?"
    CONNECT = "Getting those minions back to work sir!"
    DISCONNECT = "Disconnecting from server."
    RECONNECT = "Reconnecting to server."
    REFRESH = "You're right, they do need a break... Refreshing!"
    RESET_STATS = "Resetting cobbleminer stats."
    ESC = "ESC pressed."
    SET_CAPTCHA_CHAT = "Setting this chat as the captcha alerts chat."
    CAPTCHA_ALERT = "Captcha detected!\nUse /solvecaptcha@<bot_name> " \
                    "<text> to solve it."
    BAD_CAPTCHA_USAGE = "Bad arguments. Usage:\n" \
                        "/solvecaptcha@<bot_name> <text>"
    MONITOR_START = "Waking up the babysitter! Monitor up."
    MONITOR_STOP = "Stopping monitor."
    UPDATE_BOT = "Time for some new features... Updating!"
    UPDATE_COBBLEMINER = "Updating CobbleMiner macros..."
    MACROS_INSTALLED = "CobbleMiner macros successfully updated!\n" \
                       "Reconnecting to hypixel so changes can take effect..."
    RESTARTING = "I'm restarting, be back in a moment hopefully. " \
                 "Try to /start me in a few moments."
    UPDATE_FAILED = "Woops! Updated failed."
    RELAUNCH = "As you wish master, relaunching!\nMay take about 2 " \
               "minutes...\nI'll send you an update when I'm done."


# === Decorators === #
def auth(func):
    """Authenticate the user before executing a command."""
    @functools.wraps(func)
    def wrapper(self, update, context):
        user = update.message.from_user.username
        if user in config.AUTHORISED_USERS:
        	return func(self, update, context)
        else:
        	logging.warning(f"Unauthorized user: '{user}', tried to "
                            f"execute '{update.message.text}'.")

    return wrapper


def send_image(func):
    """Send live image after executing a minecraft command to see result."""
    @functools.wraps(func)
    def wrapper(self, update, context):
        retval = func(self, update, context)
        time.sleep(SEND_IMAGE_DELAY_SECS)
        LiveImage().run(update, context)
        return retval

    return wrapper


# === Abstract Classes === #
class Command(ABC):
    """A base class for bot commands."""
    @abstractmethod
    def run(self, update, context):
        raise NotImplementedError

    @staticmethod
    def _reply(update, context, msg):
        """Send a reply message to the chat."""
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    @staticmethod
    def _send_photo(update, context, img_path):
        """Send a photo reply to the chat."""
        with open(img_path, "rb") as img:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)


class MinecraftCommand(Command):
    """Command operating directly on minecraft game."""
    def __init__(self):
        self._minecraft = Minecraft()

    @abstractmethod
    def run(self, update, context):
        raise NotImplementedError


class MonitorCommand(Command):
    """Command to control the minecraft server reconnector."""
    def __init__(self):
        self._mc_server_reconnector = MinecraftServerReconnector()

    @abstractmethod
    def run(self, update, context):
        raise NotImplementedError


class UpdateCommand(Command):
    """Command to download and install updates from Github."""
    def __init__(self, repo_name, local_install_dir):
        self._repo_installer = GithubRepoInstaller(repo_name,
                                                   local_install_dir)

    @abstractmethod
    def run(self, update, context):
        raise NotImplementedError


# === Commands === #
class LiveImage(MinecraftCommand):
    IMAGE_SAVE_PATH = "live_image.png"

    @auth
    def run(self, update, context):
        self._minecraft.save_live_image(self.IMAGE_SAVE_PATH)
        self._send_photo(update, context, self.IMAGE_SAVE_PATH)


class Stats(MinecraftCommand):
    @auth
    def run(self, update, context):
        logging.info("Collecting minion stats...")
        self._reply(update, context, self._get_minion_stats())

    def _get_minion_stats(self):
        try:
            return self._read_stats_from_file()
        except FileNotFoundError:
            return "Woops! Stats file missing."

    def _read_stats_from_file(self):
        with open(config.COBBLEMINER_STATS_FILE, "r") as stats_file:
            stats_file_data = stats_file.read()
            return self._extract_most_recent_stats(stats_file_data)

    @staticmethod
    def _extract_most_recent_stats(raw_stats):
        last_chunk_start_index = raw_stats.rfind(STATS_BORDER,
                                                 0, len(raw_stats) - 1)
        return raw_stats[last_chunk_start_index:].strip(STATS_BORDER)


class ResetStats(MinecraftCommand):
    @auth
    def run(self, update, context):
        self._minecraft.reset_cobbleminer_stats()
        self._reply(update, context, ReplyMsg.RESET_STATS.value)
        Stats().run(update, context)


class Connect(MinecraftCommand):
    @send_image
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.CONNECT.value)
        self._minecraft.connect()


class Disconnect(MinecraftCommand):
    @send_image
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.DISCONNECT.value)
        self._minecraft.disconnect()


class Reconnect(MinecraftCommand):
    @send_image
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.RECONNECT.value)
        self._minecraft.reconnect()


class Refresh(MinecraftCommand):
    @send_image
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.REFRESH.value)
        self._minecraft.refresh()


class Relaunch(MinecraftCommand):
    @send_image
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.RELAUNCH.value)
        self._minecraft.relaunch()


class Escape(MinecraftCommand):
    @send_image
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.ESC.value)
        self._minecraft.press_escape()


class SolveCaptcha(MinecraftCommand):
    EXPECTED_ARGS_AMOUNT = 1

    @send_image
    @auth
    def run(self, update, context):
        if len(context.args) == self.EXPECTED_ARGS_AMOUNT:
            self._minecraft.send_chat_message(context.args[0])
        else:
            self._reply(update, context, ReplyMsg.BAD_CAPTCHA_USAGE.value)


class SetCaptchaChat(Command):
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.SET_CAPTCHA_CHAT.value)
        CaptchaDetector(context.bot).set_alerts_target_chat(
            update.effective_chat.id
        )


class GreetUser(Command):
    @auth
    def run(self, update, context):
        self._reply(update, context, ReplyMsg.START.value)


class StartMonitor(MonitorCommand):
    @auth
    def run(self, update, context):
        if not self._mc_server_reconnector.is_up():
            self._mc_server_reconnector.keep_connected()
        self._reply(update, context, ReplyMsg.MONITOR_START.value)


class StopMonitor(MonitorCommand):
    @auth
    def run(self, update, context):
        self._mc_server_reconnector.stop()
        self._reply(update, context, ReplyMsg.MONITOR_STOP.value)


class UpdateAndRebootBot(UpdateCommand):
    """Note: this command causes the program to reboot."""
    def __init__(self):
        super().__init__('MinionManager', config.MINION_MANAGER_DIR)

    @auth
    def run(self, update, context):
        try:
            self._reply(update, context, ReplyMsg.UPDATE_BOT.value)
            self._repo_installer.install_latest_files()
            self._reply(update, context, ReplyMsg.RESTARTING.value)
            self._reboot_program()
        except RepoInstallError:
            self._reply(update, context, ReplyMsg.UPDATE_FAILED.value)

    @staticmethod
    def _reboot_program():
        logging.info("Rebooting program...")
        subprocess.Popen("run.bat", cwd=config.MINION_MANAGER_DIR)
        exit(0)


class UpdateCobbleMiner(UpdateCommand):
    """Update minecraft macro scripts."""
    SERVER_LOAD_TIME_SECS = 5

    def __init__(self):
        super().__init__('CobbleMiner', config.COBBLEMINER_MACROS_DIR)
        self._minecraft = Minecraft()

    @auth
    def run(self, update, context):
        try:
            self._reply(update, context, ReplyMsg.UPDATE_COBBLEMINER.value)
            self._repo_installer.install_latest_files()
            self._apply_macro_changes()
            self._reply(update, context, ReplyMsg.MACROS_INSTALLED.value)
        except RepoInstallError:
            self._reply(update, context, ReplyMsg.UPDATE_FAILED.value)

    def _apply_macro_changes(self):
        self._minecraft.reconnect()
        time.sleep(self.SERVER_LOAD_TIME_SECS)
