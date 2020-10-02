"""
    Author  : Tal Avraham
    Created : 5/1/2020
    Purpose : Utility functions for the program.
"""


# === Imports === #
import win32api
import win32con
import time
import subprocess
import logging
from typing import Tuple

# === Constants === #
CLICK_DELAY_SECS = 1.5
CURSOR_MOVE_DELAY_SECS = 0.1


# === Functions === #
def mouse_click(coordinates: Tuple[int, int]):
    """Click a position on the screen."""
    win32api.SetCursorPos(coordinates)
    time.sleep(CURSOR_MOVE_DELAY_SECS)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, *coordinates, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, *coordinates, 0, 0)
    time.sleep(CURSOR_MOVE_DELAY_SECS)


def kill_task(task_name):
    """Kill a windows task."""
    logging.info(f"Killing {task_name}")
    subprocess.run(f"taskkill /f /im  {task_name}",
                   shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT, timeout=3)
