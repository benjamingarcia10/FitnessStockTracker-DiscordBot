# FitnessStockTracker DiscordBot
### Why?
I'm a college student powerlifter who as many people during COVID-19 was
unable to access the gym. As a result, I decided to create a home gym and to do
that I needed some gym equipment. However, many sites were out of stock, especially
Rogue, my favorite fitness company. As a result, I decided to create this bot
to update myself whenever an equipment is back in stock. I encountered a community
on reddit r/homegym where other users faced the same problem and I decided this would
be a great tool to help others just like me.

### [View Original Project](https://github.com/jonniechow/RogueStockBot/)
Check out the original version of this tracker from jonniechow that worked as a Facebook Messenger bot.

### What?
* Search for your favorite Rogue Fitness equipment
* Get notified via Discord Webhook whenever items are back in stock
* No limit on number of items you can check
* Checks items as often as you'd like so

# How to Use
0. Install [Python](https://www.python.org/downloads/) and be sure to install pip and add Python to PATH as well using the Python installer.
1. Create a Discord server or use an existing one that you have Administrator permission to.
2. Create a text channel of where you want the stock updates to be posted to.
3. Create a Webhook to that text channel and save the Webhook URL for step 5.
	- You can view instructions on how to do that here: [Intro to Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
4. Create a Discord bot and invite the bot with the "Administrator" permission. Save the token from the created Discord bot for step 4.
	- You can view instructions on how to do that here: [Creating a Bot Account](https://discordpy.readthedocs.io/en/latest/discord.html)
5. Create a ".env" file in the root directory of the project and paste these lines in your .env file but replace the text after the "=" with your corresponding information:
	- **DISCORD_TOKEN=** DISCORD BOT TOKEN FROM STEP 4
	- **ROGUE_FITNESS_WEBHOOK_URL=** DISCORD WEBHOOK URL FOR ROGUE FITNESS STOCK INFO FROM STEP 3
	
	6. The following are optional if you want to receive text notifications:
	    - **PLIVO_SOURCE_PHONE_NUMBER=** PLIVO SOURCE NUMBER (in E.164 format, for example +15671234567)
	    - **PHONE_NUMBER_TO_NOTIFY=** DESTINATION PHONE NUMBER (in E.164 format, for example +15671234567)
	    - **PLIVO_AUTH_ID=** PLIVO AUTH ID
	    - **PLIVO_AUTH_TOKEN=** PLIVO AUTH TOKEN
	    - Then open the variables.py file in a text editor and change the line that says ``send_text_notification = False`` to ``send_text_notification = True``
7. Install all dependencies for this project
	- Open a CMD/Powershell window in the root directory of the project and run the following command:
		- ``pip install -r requirements.txt``
		- Ensure there are no errors when running the command.
8. Run the bot.py file and you should see your bot come online in your Discord server.
9. Create a role that you would like to authorize to use the bot and run the following command (you can change this at any time by rerunning the command): ``/authrole {role}``
10. Use the following commands to track your items:
	- ``/rogue`` When this command is run, it will prompt for all items you want tracked separated by a new line. Find all the available items here: [https://roguestockbot.com/current-items](https://roguestockbot.com/current-items) For each item you want tracked, type the corresponding text from the "Command" column and add a new line by pressing ``Shift + Enter``. Once started, you will see a confirmation that it is tracking the items you entered which looks like this:
	
	![result](/images/Start-Tracking.png)

	Once any of the items you chose are in stock, it will send a Discord webhook that looks like this:

	![result](/images/InStock-Webhook.png)
	
	- ``/roguestop`` This stops tracking Rogue items if it is currently tracking and displays a confirmation for what items it is no longer tracking.
	- ``/roguetest`` This sends a test webhook to the assigned webhook URL to ensure it is working properly.
	- ``/roguenotify`` (Default: Off) This toggles Rogue notifications which tags @everyone when an item stock notification is sent via the Discord webhook.
	- ``/roguedebug`` (Default: Off) This toggles Rogue debug mode which adds additional printout in the console.
	- ``/roguepersist`` (Default: Off) This toggles Rogue persistent logging which means if you were to start checking Rogue and stop it, it will maintain the status of the items previously so when you restart it, it will not notify items that were already notified as in stock.
