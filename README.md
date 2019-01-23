# Discord Google Assistant Bot

> A bot that hangs out in Discord and sometimes talks to Google Assistant. 

## Features
#### Google Assistant
- Google Assistant intent for asking which members of a Discord guild are online.

### Music Player
- Plays music from YouTube, SoundCloud, etc. through [youtube-dl](https://github.com/rg3/youtube-dl/commit/f7560859a3e25ccaa74123428d42f821299a2bed).


## Installation
- [Create a Discord bot account and invite it to your server](https://discordpy.readthedocs.io/en/rewrite/discord.html).
- `cd` to the project directory, and run the installer script `./install.sh`.
- The bot's command prefix defaults to `.`. This can be configured to suit your guild's needs.

#### Google Assistant
If you want to use Google Assistant features, [follow the Dialogflow setup instructions](https://developers.google.com/actions/dialogflow/project-agent). Set the fulfillment URL to point to your hosted `index.py`. 
	
- If you need free web hosting, you host your web service locally and expose a port to the web using a tool like [Serveo](https://serveo.net/).

### Custom Responses
The bot uses Google Sheets as a shared database of custom responses. This Sheet can be edited on-the-fly to setup custom bot text or audio responses to text typed in the Discord channels. 

Create a new Sheet and configure a service account for the but [following this tutorial](https://youtu.be/vISRn5qFrkM). If you wish, share the link with your guild's members to allow them to add their own flavor to the bot. 


## Usage 

### Vanilla bot
Run `bot/bot_service.sh` to run the Discord bot without any fancy Google Assistant functionality.

### Google Assistant mode
Run the Sanic server with `python3 bot/index.py`. This will run the web server at http://localhost:8000. 

If you're hosting the bot elsewhere, run the server the way you're used to. You may need to edit the configuration in `index.py`. 

Type `<command_prefix> help` to see what the bot can do!


## Roadmap
- More bot features. Got an idea? Open an issue! 
