#!/usr/bin/python3

import os
import models
from telegram_bot_helper import TelegramBotHelper
from flask import Flask

# Create flask app
app = Flask(__name__)

@app.route(f"/{os.environ['TELEGRAM_BOT_TOKEN']}")
def teste():
    return "oi"

@app.route('/')
def index():
    TelegramBotHelper.start_polling()
    return "It Works!"


# if __name__ == '__main__':
    # create_app()