# Discord Google Assistant Bot

A bot that hangs out in Discord and sometimes talks to Google Assistant. 

## Installation
- [Create a Discord bot account and invite it to your server](https://discordpy.readthedocs.io/en/rewrite/discord.html)
- Create a virtual environment using Python version 3.6 
- `pip install -r requirements.txt; mkdir secret; touch secret/token.txt`
- Copy and paste your Client ID into `token.txt`

## Usage 
Start your virtualenv, then the Sanic server with `python3 index.py`. This will run the bot at http://localhost:8000.


The bot won't do much as of yet. More to come as the bot is developed. Stay tuned. 

## Roadmap
- Install script for ezpz installation
- Include Dialogflow setup instructions in README
- More bot features. Got an idea? Open an issue! 
- Update to Python 3.7 once discord.py supports it