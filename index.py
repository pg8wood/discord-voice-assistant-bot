import os
import dialogflow
import requests
import json
import pusher
import bot

from sanic import Sanic
from sanic import response

app = Sanic()


@app.route('/')
async def run(request):
    return response.html('<p>You found the API!')


@app.route('/get_discord_voice_channel_status', methods=['POST'])
async def get_discord_voice_channel_status(self):
    voice_chat_dict = await bot.get_online_users()
    reply = "No one's in any of the voice channels right now."

    if len(voice_chat_dict) > 0:
        reply = ""
        for key in voice_chat_dict:
            num_users = len(voice_chat_dict[key])

            if num_users == 1:
                reply += "%s is in %s." % (voice_chat_dict[key], key)
            elif num_users == 2:
                reply += " and ".join(voice_chat_dict[key]) + (" are in %s" % key)
            else:
                reply += ", ".join(voice_chat_dict[key][:-1]) + ", and " + voice_chat_dict[key][-1] + ("are in %s." % key)

    reply = {
        "fulfillmentText": reply
    }

    return response.json(reply)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
