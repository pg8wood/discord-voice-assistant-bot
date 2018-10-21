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
async def test(request):
    users = await bot.get_online_users()
    return json({users[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
