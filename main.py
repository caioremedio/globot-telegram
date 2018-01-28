#!/usr/bin/python3

import os
from pprint import pprint
# import models
from telegram_bot_helper import TelegramBotHelper
from flask import Flask, request

# Create flask app
app = Flask(__name__)

@app.route(f"/{os.environ['TELEGRAM_BOT_TOKEN']}", methods=['POST'])
def telegram_bot_post():
    TelegramBotHelper.setupCommandHandlers()
    TelegramBotHelper.handle_request_json(request.get_json(force=True))
    return "ata"

@app.route('/')
def index():
    return "It Works!"