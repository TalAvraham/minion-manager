"""
    Author  : Tal Avraham
    Created : 4/29/2020
    Purpose : Telegram Minion Manager bot.
"""

from telegram.ext import Updater, CommandHandler
from bot import commands
from minecraft.minecraft_reconnector import MinecraftServerReconnector
from minecraft.captcha_detector import CaptchaDetector
import logging


class MinionBot:
    """Telegram minion manager bot to remotely control minions."""

    COMMAND_HANDLERS = \
        [CommandHandler('start', commands.GreetUser().run),
         CommandHandler('stats', commands.Stats().run),
         CommandHandler('statsreset', commands.ResetStats().run),
         CommandHandler('liveimage', commands.LiveImage().run),
         CommandHandler('connect', commands.Connect().run),
         CommandHandler('disconnect', commands.Disconnect().run),
         CommandHandler('reconnect', commands.Reconnect().run),
         CommandHandler('refresh', commands.Refresh().run),
         CommandHandler('esc', commands.Escape().run),
         CommandHandler('relaunch', commands.Relaunch().run),
         CommandHandler('solvecaptcha', commands.SolveCaptcha().run),
         CommandHandler('setcaptchachat', commands.SetCaptchaChat().run),
         CommandHandler('monitorstart', commands.StartMonitor().run),
         CommandHandler('monitorstop', commands.StopMonitor().run),
         CommandHandler('updatebot', commands.UpdateAndRebootBot().run),
         CommandHandler('updatecobbleminer', commands.UpdateCobbleMiner().run)]

    def __init__(self, token):
        self._updater = Updater(token=token, use_context=True)
        self._dispatcher = self._updater.dispatcher
        self._set_handlers()
        self._mc_server_reconnector = MinecraftServerReconnector()
        self._captcha_detector = CaptchaDetector(self._updater.bot)

    def run(self):
        logging.info("Starting Minion Manager bot.")
        self._updater.start_polling()
        self._mc_server_reconnector.keep_connected()
        self._captcha_detector.run_forever()

    def shutdown(self):
        self._mc_server_reconnector.stop()
        logging.info("Shutting down Minion Manager bot.")
        self._updater.stop()

    def _set_handlers(self):
        self._set_command_handlers()
        self._set_error_handlers()

    def _set_command_handlers(self):
        for handler in self.COMMAND_HANDLERS:
            self._dispatcher.add_handler(handler)

    def _set_error_handlers(self):
        self._dispatcher.add_error_handler(self._telegram_error_callback)

    def _telegram_error_callback(self, update, context):
        logging.error(f"Telegram error: {context.error}")
        if update is not None:
            self._send_error_reply(update)

    @staticmethod
    def _send_error_reply(update):
        if update.message:
            update.message.reply_text(text=commands.ReplyMsg.ERROR.value)
        elif update.callback_query:
            update.callback_query.message.reply_text(
                text=commands.ReplyMsg.ERROR.value
            )
