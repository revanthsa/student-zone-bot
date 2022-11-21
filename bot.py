from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import json
from handlers.StartHandeler import start
from handlers.FetchHandeler import text

with open('config.json') as json_file:
    config = json.load(json_file)
token = config["token"]
allowedUsers = config["allowedusers"]

updater = Updater(token=token, use_context=False)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text, text))

updater.start_polling()
updater.idle()