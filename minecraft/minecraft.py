"""
    Author  : Tal Avraham
    Created : 4/29/2020
    Purpose : Minecraft API.
"""

# === Imports === #
import time
import logging
import config
import pynput.keyboard
import subprocess
import utils
from utils.decorators import Singleton
from utils.window import Window
from minecraft.chest import Chest

# === Constants === #
KEYBOARD_BUTTON_HIT_DELAY_SECS = 1
MINECRAFT_LOAD_TIME_SECS = 60
LAUNCHER_LOAD_TIME_SECS = 15
MINECRAFT_CHAT_KEY = 't'


# === Classes === #
class Minecraft(metaclass=Singleton):
    """An easy interface for Minecraft operations."""

    def __init__(self):
        self._game_window = Window(r'Minecraft \d+(\.\d+)*')
        self._launcher_window = Window('Minecraft Launcher')
        self._keyboard = pynput.keyboard.Controller()

    def save_live_image(self, save_path):
        logging.info("Taking screenshot of Minecraft window.")
        self._game_window.save_screenshot(save_path)

    def update_macro_config(self):
        logging.info("Updating macro config.")
        self._hit_keyboard_button(config.CONFIG_KEYBIND)

    def reset_cobbleminer_stats(self):
        logging.info("Resetting cobbleminer stats.")
        self._hit_keyboard_button(config.RESET_STATS_KEYBIND)

    def refresh(self):
        logging.info("Refreshing cobbleminer.")
        self._hit_keyboard_button(config.REFRESH_KEYBIND)

    def press_escape(self):
        logging.info("Pressing ESC in game.")
        self._hit_keyboard_button('t')

    def send_chat_message(self, message):
        logging.info(f"Sending chat message: '{message}'.")
        self._game_window.focus()
        self._hit_keyboard_button(MINECRAFT_CHAT_KEY)
        self._keyboard.type(message)
        self._hit_keyboard_button(pynput.keyboard.Key.enter)

    def _hit_keyboard_button(self, key):
        self._game_window.focus()
        self._keyboard.press(key)
        self._keyboard.release(key)
        time.sleep(KEYBOARD_BUTTON_HIT_DELAY_SECS)

    def click_chest_slot(self, chest: Chest, chest_slot: int):
        self._game_window.focus()
        utils.mouse_click(chest.get_slot_coordinates(chest_slot))

    def reconnect(self):
        self.disconnect()
        self.connect()

    def disconnect(self):
        logging.info("Disconnecting from hypixel server.")
        self._hit_keyboard_button(pynput.keyboard.Key.esc)
        utils.mouse_click(config.DISCONNECT_BUTTON)

    def connect(self):
        self._return_to_server_list_menu()
        self._connect_to_hypixel()

    def _return_to_server_list_menu(self):
        self._game_window.focus()
        utils.mouse_click(config.BACK_TO_SERVER_LIST_BUTTON)

    @staticmethod
    def _connect_to_hypixel():
        logging.info("Connecting to hypixel server.")
        utils.mouse_click(config.MULTIPLAYER_BUTTON)
        utils.mouse_click(config.HYPIXEL_BUTTON)
        utils.mouse_click(config.JOIN_SERVER_BUTTON)

    def relaunch(self):
        logging.info("Relaunching minecraft...")
        self._close_minecraft()
        self._launch_minecraft()

    @staticmethod
    def _close_minecraft():
        utils.kill_task(config.LAUNCHER_PROCESS_NAME)
        utils.kill_task(config.MINECRAFT_PROCESS_NAME)

    def _launch_minecraft(self):
        logging.info("Running minecraft launcher and entering game.")
        self._open_minecraft_launcher()
        self._start_minecraft_from_launcher()
        self._connect_to_hypixel()

    def _open_minecraft_launcher(self):
        subprocess.Popen(config.MINECRAFT_EXE)
        time.sleep(LAUNCHER_LOAD_TIME_SECS)
        self._launcher_window.focus()

    def _start_minecraft_from_launcher(self):
        utils.mouse_click(config.PLAY_BUTTON)
        time.sleep(MINECRAFT_LOAD_TIME_SECS)
        self._game_window.focus()
