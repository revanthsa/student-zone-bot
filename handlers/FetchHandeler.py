from processors.MessageProcessor import MessageProcessor
import json
from telegram.ext.dispatcher import run_async
# heroku config
import environ
env = environ.Env()
environ.Env.read_env()
json_file = env('CONFIG')
config = json.loads(json_file)

# Local config
# with open('config.json') as json_file:
#     config = json.load(json_file)

allowedUsers = config["allowedusers"]
roll_no = config["student_credentials"].keys()

@run_async
def text(bot, update):
    from_user = update.message.from_user
    if from_user["username"] not in allowedUsers:
        bot.sendMessage(chat_id=update.message.chat_id, text=f"@{from_user.username} you are not allowed to use this bot!")
        return

    if update.message.text in roll_no:
        bot.sendMessage(chat_id=update.message.chat_id, text="Please wait while we fetch your data.")
        processor = MessageProcessor()
        res = processor.reply(update.message.text)

        if len(res) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="Try again later.")
        elif len(res) == 3:
            bot.sendPhoto(chat_id=update.message.chat_id, photo=res[0], caption= str(update.message.text) + "'s Attendance")
            bot.sendPhoto(chat_id=update.message.chat_id, photo=res[1], caption= str(update.message.text) + "'s CA marks")
            bot.sendPhoto(chat_id=update.message.chat_id, photo=res[2], caption= str(update.message.text) + "'s Exam Results")
        else:
            bot.sendPhoto(chat_id=update.message.chat_id, photo=res[0], caption= str(update.message.text) + "'s Attendance")
            bot.sendPhoto(chat_id=update.message.chat_id, photo=res[1], caption= str(update.message.text) + "'s CA marks")
    
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=f"Sorry! '{update.message.text}' is not a valid rollno or command.\nType /start to get started.")
