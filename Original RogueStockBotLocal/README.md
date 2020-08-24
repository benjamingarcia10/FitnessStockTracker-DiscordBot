# RogueStockBotLocal - Local Rogue Item Tracker
### Why?
I'm a college student powerlifter who as many people during COVID-19 was
unable to access the gym. As a result, I decided to create a home gym and to do
that I needed some gym equipment. However, many sites were out of stock, especially
Rogue, my favorite fitness company. As a result, I decided to create this bot
to update myself whenever an equipment is back in stock. I encountered a community
on reddit r/homegym where other users faced the same problem and I decided this would
be a great tool to help others just like me.

### View Original Project
Check out the original version of this tracker that worked as a Facebook Messenger bot.
[Original Source From jonniechow](https://github.com/jonniechow/RogueStockBot/)

### What?
* Search for your favorite Rogue Fitness equipment
* Get notified via Discord Webhook whenever items are back in stock
* No limit on number of items you can check
* Checks items as often as you'd like so

### How to Use
There are two files you must create/modify for the tracker to work:
 - "check.txt" - File containing all products you want to check
	 - On a new line for each item, put the command that corresponds to the item you want.
	 - Find all the available commands here: [https://roguestockbot.com/current-items](https://roguestockbot.com/current-items)
 - ".env" - File containing your Discord Webhook URL and Plivo Notification configurations
	- Paste these in your .env file and replace the values after the "=" with your corresponding information:
		- **DISCORD_WEBHOOK_URL=**REPLACE THIS WITH YOUR DISCORD WEBHOOK URL
		- **PLIVO_SOURCE_PHONE_NUMBER=**REPLACE WITH PLIVO SOURCE NUMBER (in E.164 format, for example +15671234567)
		- **PHONE_NUMBER_TO_NOTIFY=**REPLACE WITH DESTINATION PHONE NUMBER (in E.164 format, for example +15671234567)
		- **PLIVO_AUTH_ID=**REPLACE WITH PLIVO AUTH ID
		- **PLIVO_AUTH_TOKEN=**REPLACE WITH PLIVO AUTH TOKEN