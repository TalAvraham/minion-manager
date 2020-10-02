"""
    Author  : Tal Avraham
    Created : 4/29/2020
    Purpose : Remote Minion Manager using a Telegram bot.
"""

# === Imports === #
import logging
import logging.config
from bot import MinionBot
import config
import time


# === Functions === #
def wait_for_exit_signal():
    """Sleep and wait for keyboard interrupt."""
    while True:
        time.sleep(1000)


def main():
    """Initiates the program."""
    logging.config.dictConfig(config.LOG_CONFIG)
    bot = MinionBot(config.BOT_TOKEN)

    try:
        bot.run()  # Runs in a separate thread
        wait_for_exit_signal()
    except KeyboardInterrupt:
        bot.shutdown()


if __name__ == '__main__':
    main()
