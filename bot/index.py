import bot
import json
import os
import ssl

from sanic import Sanic
from sanic import response

app = Sanic()

context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain("/etc/letsencrypt/live/li1294-116.members.linode.com/fullchain.pem", keyfile="/etc/letsencrypt/live/li1294-116.members.linode.com/privkey.pem")


@app.route('/')
async def run(request):
    return response.html('<p>You found the API!</p>')


@app.route('/get_discord_voice_channel_status', methods=['POST'])
async def get_discord_voice_channel_status(self):
    voice_chat_dict = await bot.get_online_users()
    fulfillment_message = "No one's in any of the voice channels right now."

    if len(voice_chat_dict) > 0:
        fulfillment_message = ""
        for key in voice_chat_dict:
            num_users = len(voice_chat_dict[key])
            user_list = voice_chat_dict[key]

            if num_users == 1:
                fulfillment_message += "%s is" % user_list[0]
            elif num_users == 2:
                fulfillment_message += " and ".join(user_list) + " are"
            else:
                fulfillment_message += ", ".join(user_list[:-1]) + ", and " + user_list[-1] + "are"

            fulfillment_message += " in %s." % key

    reply = {
        "fulfillmentText": fulfillment_message
    }

    return response.json(reply)


@app.route('on_gspread_edit', methods=['GET'])
async def on_gspread_edit(self):
    bot.sheets_client.refresh_records()
    return response.html('<p>You found the Google Sheets fulfillment API!</p>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl=context)
