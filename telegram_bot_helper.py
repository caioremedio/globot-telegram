import logging
import os
from string import Template
from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from globo_helper import GloboHelper, RequestCityType

class TelegramBotHelper:
    """docstring for TelegramBotHelper"""
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'])
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    response_template = Template("""
        Na notícia: *$article_title*

O usuário *$comment_author_name* comentou:

        *$comment_text*
    """)

    # @classmethod
    # def handle_request(cls, )

    @classmethod
    def command_comentario_home(cls, bot, update):
        comment = GloboHelper.get_random_comment_for_request_type(RequestCityType.TYPE_HOME_ID)

        print("====================")
        print(update)
        print("====================")

        cls.send_message_with_comment(bot, update, comment)

    @classmethod
    def command_comentario_sp(cls, bot, update):
        comment = GloboHelper.get_random_comment_for_request_type(RequestCityType.TYPE_SP_ID)

        print("====================")
        print(update)
        print("====================")

        cls.send_message_with_comment(bot, update, comment)

    @classmethod
    def command_comentario_rj(cls, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Em breve...")

    @classmethod
    def send_message_with_comment(cls, bot, update, comment):
        bot.send_message(
            chat_id=update.message.chat_id,
            text=cls.response_template.substitute(
                article_title=comment.article.title,
                comment_author_name=comment.author_name,
                comment_text=comment.text
            ),
            parse_mode='Markdown'
        )

    @classmethod
    def setup_webhooks(cls):
        cls.setupCommandHandlers()
        cls.updater.start_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=os.environ['TELEGRAM_BOT_TOKEN'])
        cls.updater.bot.set_webhook(f"{os.environ['APP_URL']}/{os.environ['TELEGRAM_BOT_TOKEN']}")
        cls.updater.idle()

    @classmethod
    def handle_request_json(cls, json):
        update = Update.de_json(json, cls.updater.bot)
        cls.dispatcher.process_update(update)

    @classmethod
    def setupCommandHandlers(cls):
        cls.dispatcher.add_handler(CommandHandler('comentario_home', cls.command_comentario_home))
        cls.dispatcher.add_handler(CommandHandler('comentario_sp', cls.command_comentario_sp))
        cls.dispatcher.add_handler(CommandHandler('comentario_rj', cls.command_comentario_rj))