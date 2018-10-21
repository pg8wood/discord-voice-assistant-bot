from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

# run Flask app
if __name__ == "__main__":
        app.run()
