"""
    Author  : Tal Avraham
    Created : 4/30/2020
    Purpose : Program configuration.
"""

# === Bot Configuration === #
BOT_TOKEN = '*Insert your bot token here*'
AUTHORISED_USERS = ['*Insert telegram username here*',
					'*you can insert multiple users...*']
# The ID of the default telegram chat to send captcha alerts to.
DEFAULT_CAPTCHA_ALERTS_CHAT_ID = -1001276019784

# === Github === #
GITHUB_TOKEN = "*Insert your github access token here*"

# === Paths & Processes === #
# You need to set these to match the paths on your pc, left my own config
# just to make it clear of what files you need here.
COBBLEMINER_STATS_FILE = "C:\\Users\\win10\\AppData\\Roaming\\.minecraft\\" \
                         "liteconfig\\common\\macros\\logs\\CobbleStats.txt"
COBBLEMINER_MACROS_DIR = "C:\\Users\\win10\\AppData\\Roaming\\.minecraft\\" \
                         "liteconfig\\common\\macros"
CAPTCHA_ALERTS_FILE = "C:\\Users\\win10\\AppData\\Roaming\\.minecraft\\" \
                      "liteconfig\\common\\macros\\logs\\CaptchaAlerts.txt"
MINECRAFT_LOG_FILE = "C:\\Users\\win10\\AppData\\Roaming\\.minecraft\\" \
                      "logs\\latest.log"
MINECRAFT_CRASH_DIR = "C:\\Users\\win10\\AppData\\Roaming\\.minecraft\\" \
                      "crash-reports\\"
MINECRAFT_EXE = "C:\\Program Files (x86)\\Minecraft\\MinecraftLauncher.exe"
MINION_MANAGER_DIR = "C:\\Users\\win10\\Desktop\\Minion Manager"
CAPTCHA_SAMPLES_DIR = "CaptchaSamples"
LAUNCHER_PROCESS_NAME = "MinecraftLauncher.exe"
MINECRAFT_PROCESS_NAME = "javaw.exe"

# === Minecraft Buttons Coordinates === #
# Also needs to be adjusted to the cooridnates on your screen.
BACK_TO_SERVER_LIST_BUTTON = (963, 575)
DISCONNECT_BUTTON = (960, 505)
HYPIXEL_BUTTON = (935, 130)
JOIN_SERVER_BUTTON = (750, 950)
PLAY_BUTTON = (1050, 1000)
MULTIPLAYER_BUTTON = (950, 440)
SMALL_CHEST_TOP_LEFT_SLOT = (815, 415)

# === Keybinds === #
# Macro mod keybinds in minecraft
REFRESH_KEYBIND = 'r'
CONFIG_KEYBIND = 'c'
RESET_STATS_KEYBIND = 'p'

# === Constants === #
KB = 1024
MB = 1024 * KB

# === Logging === #
LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(thin_white)s%(asctime)s [%(log_color)s%(levelname)-7s'
                      '%(thin_white)s] %(reset)s%(white)s%(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S',
            'log_colors': {
                'DEBUG': 'bold_cyan',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red'
            }
        },
        'basic': {
            'format': '%(asctime)s [%(levelname)-7s] %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'basic',
            'level': 'INFO',
            'filename': 'bot.log',
            'maxBytes': 1 * MB
        }
    },
    'loggers': {
        '': {
            'handlers': ['stream', 'file'],
            'level': 'INFO'
        },
    }
}
