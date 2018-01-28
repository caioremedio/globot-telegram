from main import app

if __name__ == "__main__":
    from telegram_bot_helper import TelegramBotHelper
    app.run()
    TelegramBotHelper.setup_webhooks()
