import logging
import os
from string import Template
from telegram.ext import Updater, CommandHandler
from globo_helper import GloboHelper

class TelegramBotHelper:
    """docstring for TelegramBotHelper"""
    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'])
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    response_template = Template("""
        Na notícia: *$article_title*

O usuário *$comment_author_name* comentou:

        *$comment_text*
    """)

    @classmethod
    def command_comentario_home(cls, bot, update):
        comment = GloboHelper.get_random_comment()

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
    def command_comentario_sp(cls, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Denissp")

    @classmethod
    def command_comentario_rj(cls, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Denisrj")

    @classmethod
    def start_polling(cls):
        cls.setupCommandHandlers()
        cls.updater.start_polling()
        cls.updater.idle()

    @classmethod
    def setupCommandHandlers(cls):
        cls.dispatcher.add_handler(CommandHandler('comentario_home', cls.command_comentario_home))
        cls.dispatcher.add_handler(CommandHandler('comentario_sp', cls.command_comentario_sp))
        cls.dispatcher.add_handler(CommandHandler('comentario_rj', cls.command_comentario_rj))