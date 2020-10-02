# Minion-Manager
Monitor and remote control over a minecraft bot.  
To give you a little bit of background, this program is a bot that plays minecraft on Hypixel Skyblock server by itself, breaks cobblestone blocks, crafts them into enchanted ones, and stores them (to later sell them and generate in-game currency).  
The way it works is a bit complex, we use a minecraft mod - 'Macro/Keybinds Mod', which allows you to write code in some sort of weird scripting language, which we use to make the minecraft in-game movement, block breaking, item storing and any type of in-game mechanic we need for our task.  
We built a system out of this scripting language which starts working as soon as you enter Hypixel server, and is plug & play, meaning as soon as you connect to the server, it will take the reins and start playing on its own. This 'inner' system is called 'Cobble Miner', and the code for it is found here: [CobbleMiner](https://github.com/TalAvraham/cobble-miner).

This python program is a monitor over that bot we just discussed, and here are its key features:
* Runs forever and handles all types of disconnections / crashes by itself.
* Controlled remotely using telegram.
* Detects captcha pop ups, and lets you solve them remotely.
* Can be updated remotely (pulls updates from the github repository).
* Sends live screenshots of the game on telegram.
* Multiple bots may be controlled at once, with broadcast commands (on telegram).

# Dependencies:
``` pip install -r requirements.txt ```

# Configuration
Modify the configuration file to fit to your machine.\
Make sure to set the coordinates of the minecraft buttons precisely, use the [MouseLocator](https://www.softpedia.com/get/Others/Miscellaneous/Mouse-Locator.shtml) to do so.\
Notice that you also need to set your bot token which you can get from the [BotFather](https://telegram.me/BotFather), and a Github token with repository read rights which you can generate [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).
