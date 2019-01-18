# Discord Google Assistant Bot

A bot that hangs out in Discord and sometimes talks to Google Assistant. 

## Installation
- [Create a Discord bot account and invite it to your server](https://discordpy.readthedocs.io/en/rewrite/discord.html)
- Clone the repo, `cd` to the project directory, and run the installer script `./install.sh`

## Usage 
### Google Assistant mode
Start your virtualenv with `source python-3.6-env/bin/activate`, then the Sanic server with `python3 bot/index.py`. This will run the bot at http://localhost:8000.

### Vanilla bot
Run `bot/bot_service.sh` to run the Discord bot without any fancy Google Assistant functionality.

The bot won't do much as of yet. More to come as the bot is developed. Stay tuned. 

## Roadmap
- Document Google Sheets response functionality
- Add music functionality
- Include Dialogflow setup instructions in README
- More bot features. Got an idea? Open an issue! 
