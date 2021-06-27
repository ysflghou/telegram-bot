import time
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import configparser


def initiate_bot() -> None:
    TOKEN = get_api_token()
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    dispatcher.add_handler(inline_caps_handler)
    # handles all unknown commands (called last always)
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    updater.start_polling()
    # time.sleep(2)
    # updater.stop()


def start(update: Update, context: CallbackContext) -> None:
    text = "I'm lghou's bot, please talk to me! I will repeat what you say"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def echo(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update: Update, context: CallbackContext) -> None:
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def get_api_token() -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']['API_TOKEN']


if __name__ == '__main__':
    initiate_bot()

