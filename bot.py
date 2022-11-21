from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import json
from handlers.StartHandeler import start
from handlers.FetchHandeler import text
# heroku config
import environ
env = environ.Env()
environ.Env.read_env()
json_file = env('CONFIG')
config = json.loads(json_file)

# Local config
# with open('config.json') as json_file:
#     config = json.load(json_file)
token = config["token"]
allowedUsers = config["allowedusers"]

updater = Updater(token=token, use_context=False)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text, text))

updater.start_polling()
updater.idle()