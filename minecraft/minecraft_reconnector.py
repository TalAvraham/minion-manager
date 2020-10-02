"""
    Author  : Tal Avraham
    Created : 5/1/2020
    Purpose : Detect minecraft disconnections and crashes.
"""

import re
import config
import logging
import tailer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from utils.decorators import threaded, Singleton
from minecraft.minecraft import Minecraft

DISCONNECTION_LOG = \
    ".*Terminating .+ active macro|" \
    ".*Couldn't connect to server|" \
    ".*java.io.IOException: An existing connection was forcibly closed"
JOIN_SERVER_LOG = ".* Joined server."
LOG_LINE_READ_DELAY = 2


class CrashDirEventHandler(FileSystemEventHandler):
    """Handles file system events in crash reports directory."""

    def __init__(self):
        super().__init__()
        self._minecraft = Minecraft()

    def on_created(self, event):
        """Relaunch minecraft when a new crash report is detected."""
        logging.warning("Crash report detected.")
        self._minecraft.relaunch()


class MinecraftServerReconnector(metaclass=Singleton):
    """Monitors minecraft for disconnections and crashes."""

    MAX_RECONNECT_TRIES = 5

    def __init__(self):
        self._minecraft = Minecraft()
        self._crash_event_handler = CrashDirEventHandler()
        self._init_crash_dir_observer()
        self._reconnect_tries = 0

    def keep_connected(self):
        logging.info("Starting minecraft server reconnector.")
        self._init_observer_if_stopped()
        self._crash_dir_observer.start()
        self._detect_and_handle_disconnections()

    def stop(self):
        logging.info("Stopping minecraft server reconnector.")
        self._crash_dir_observer.stop()

    def is_up(self):
        return self._crash_dir_observer.is_alive()

    def _init_observer_if_stopped(self):
        if not self.is_up():
            # Observer start method can only be invoked once per instance.
            self._init_crash_dir_observer()

    def _init_crash_dir_observer(self):
        self._crash_dir_observer = Observer()
        self._crash_dir_observer.schedule(self._crash_event_handler,
                                          config.MINECRAFT_CRASH_DIR)

    @threaded
    def _detect_and_handle_disconnections(self):
        with open(config.MINECRAFT_LOG_FILE) as log_file:
            for log_line in tailer.follow(log_file, LOG_LINE_READ_DELAY):
                if not self.is_up():
                    break
                self._process_log_line(log_line)

    def _process_log_line(self, line):
        if re.match(DISCONNECTION_LOG, line):
            logging.warning("Disconnection from hypixel detected.")
            self._handle_disconnection()
        elif re.match(JOIN_SERVER_LOG, line):
            logging.info("Successfully reconnected.")
            self._reconnect_tries = 0

    def _handle_disconnection(self):
        if self._reconnect_tries < self.MAX_RECONNECT_TRIES:
            self._minecraft.connect()
            self._reconnect_tries += 1
        else:
            logging.warning("Max retries exceeded, relaunching minecraft.")
            self._minecraft.relaunch()
            self._reconnect_tries = 0
