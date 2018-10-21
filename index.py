import os
import dialogflow
import requests
import json
import pusher
import bot

from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route('/')
async def run(request):
    users = await bot.get_online_users()
    reply = {
        "fulfillmentText": users[0]
    }
    return json(reply)


@app.route('/get_discord_voice_channel_status', methods=['POST'])
async def get_discord_voice_channel_status(self):
    users = await bot.get_online_users()
    reply = {
        "fulfillmentText": users[0]
    }
    return json(reply)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
