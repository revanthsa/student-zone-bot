import json
from telegram.ext.dispatcher import run_async
with open('config.json') as json_file:
    config = json.load(json_file)

allowedUsers = config["allowedusers"]
roll_no = config["student_credentials"].keys()

@run_async
def start(bot, update):
    from_user = update.message.from_user
    if from_user["username"] not in allowedUsers:
        bot.sendMessage(chat_id=update.message.chat_id, text=f"@{from_user.username} you are not allowed to use this bot!")
        return
    bot.sendMessage(chat_id=update.message.chat_id, text=f"@{from_user.username} you are authorised to use this bot\nType the rollno to fetch your attendance and marks.")
