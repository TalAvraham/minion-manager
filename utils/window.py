"""
    Author  : Tal Avraham
    Created : 4/29/2020
    Purpose : Window manager.
"""

# === Imports === #
import win32gui
import win32con
import win32com.client
import re
import pyautogui
import time
import logging
from utils.decorators import retry_no_raise

# === Constants === #
FOCUS_DELAY_SECS = 0.3


# === Exceptions === #
class FocusWindowError(BaseException):
    pass


# === Classes === #
class Window:
    """Encapsulates some calls to the winapi for window management."""

    def __init__(self, window_name_wildcard):
        self._handle = None
        self._wildcard = window_name_wildcard
        self._set_window_handle_by_wildcard()
        self._shell = win32com.client.Dispatch("WScript.Shell")

    def save_screenshot(self, save_path):
        self.focus()
        img = pyautogui.screenshot(region=self._get_dimensions())
        img.save(save_path)

    @retry_no_raise(stop_max_attempt_number=3, wait_fixed=3000)
    def focus(self):
        try:
            self._set_window_handle_by_wildcard()
            self._bring_to_foreground()
        except Exception:
            logging.error("Failed to focus window. Retrying.")
            raise FocusWindowError

    def _bring_to_foreground(self):
        # Small hack to make SetForegroundWindow work.
        self._shell.SendKeys('%')
        win32gui.ShowWindow(self._handle, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(self._handle)
        time.sleep(FOCUS_DELAY_SECS)

    def _set_window_handle_by_wildcard(self):
        self._handle = None
        win32gui.EnumWindows(self._set_handle_if_wildcard_match,
                             self._wildcard)

    def _set_handle_if_wildcard_match(self, window_handle, wildcard):
        if re.match(wildcard, self._get_window_name(window_handle)):
            self._handle = window_handle

    @staticmethod
    def _get_window_name(window_handle):
        return str(win32gui.GetWindowText(window_handle))

    def _get_dimensions(self):
        x1, y1, x2, y2 = win32gui.GetClientRect(self._handle)
        x1, y1 = win32gui.ClientToScreen(self._handle, (x1, y1))
        x2, y2 = win32gui.ClientToScreen(self._handle, (x2 - x1, y2 - y1))
        return x1, y1, x2, y2
