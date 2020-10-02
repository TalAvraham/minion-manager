"""
    Author  : Tal Avraham
    Created : 7/4/2020
    Purpose : Captcha detection and solving.
"""

import tailer
import config
import logging
import os
from minecraft.minecraft import Minecraft
from utils.decorators import Singleton, threaded
from datetime import datetime
from bot import commands
import pathlib
import telegram

LOG_LINE_READ_DELAY = 2


class CaptchaDetector(metaclass=Singleton):
    def __init__(self, bot: telegram.Bot,
                 alerts_chat_id: int = config.DEFAULT_CAPTCHA_ALERTS_CHAT_ID):
        self._minecraft = Minecraft()
        self._bot = bot
        self._alerts_chat_id = alerts_chat_id
        self._captcha_sample = None

    def set_alerts_target_chat(self, chat_id):
        self._alerts_chat_id = chat_id

    @threaded
    def run_forever(self):
        logging.info("Starting captcha detector.")
        with open(config.CAPTCHA_ALERTS_FILE) as captcha_file:
            for _ in tailer.follow(captcha_file, LOG_LINE_READ_DELAY):
                self._save_captcha_sample()
                self._send_alert()

    def _save_captcha_sample(self):
        self._captcha_sample = self._build_captcha_save_path()
        self._minecraft.save_live_image(self._captcha_sample)

    @staticmethod
    def _build_captcha_save_path():
        if not os.path.exists(config.CAPTCHA_SAMPLES_DIR):
            os.makedirs(config.CAPTCHA_SAMPLES_DIR)

        curr_dir = pathlib.Path().absolute()
        curr_time = datetime.now().strftime("%d-%m-%Y %H;%M;%S")
        return f"{curr_dir}\\{config.CAPTCHA_SAMPLES_DIR}\\{curr_time}.png"

    def _send_alert(self):
        logging.warning("Captcha detected! Sending alert via telegram.")
        with open(self._captcha_sample, "rb") as img:
            self._bot.send_photo(chat_id=self._alerts_chat_id, photo=img)
            self._bot.send_message(chat_id=self._alerts_chat_id,
                                   text=commands.ReplyMsg.CAPTCHA_ALERT.value)
