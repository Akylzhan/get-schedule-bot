import os
import requests as req

import scrapers

TOKEN = "949738996:AAHVrnVCsv4LUP0y-0FNPS_dCs2lCVhcQ08"

# TODO: add other term_ids
# TODO: add department ids
term_id = 521

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
  try:
    update.message.reply_text('Hello! Send me course name (eg. CSCI 152 or public speaking) and I will send you schedule of this course')
  except:
    print("ERROR in START")

def getCourseName(update, context):
  print(update.message.text)
  try:
    courseInfo = update.message.text.lower()
    if len(courseInfo) < 3:
      update.message.reply_text("your query is smol")
      return
    courseInfo = '+'.join(courseInfo.split(' '))
    courseInfo = scrapers.getSearchData(courseInfo)

    if courseInfo == -1:
      update.message.reply_text("Такого курса нет, либо я ошибка природы :(")
      return

    for i in courseInfo:
      message = ""
      message += "Abbr: "    + i["ABBR"] + "\n"
      message += "Title: "   + i["TITLE"] + "\n"
      message += "ECTS: "    + i["CRECTS"] + "\n"
      message += "Prereqs: " + i["PREREQ"] + "\n"
      message += "Coreqs: " + i["COREQ"] + "\n"
      message += "Antireqs: " + i["ANTIREQ"] + "\n"
      message += "Description: " + i["SHORTDESC"] + "\n"
      
      schedule = scrapers.getSchedule(i['COURSEID'], term_id)
      if schedule == -1:
        update.message.reply_text("Такого курса нет, либо я ошибка природы :(")
        return
      for j in schedule:
        cell = "\n"
        cell += "Type: "     + j['ST'] + "\n"
        cell += "Days: "     + j['DAYS'] + "\n"
        cell += "Times: "    + j['TIMES'].replace('R', "R(Thursday)") + "\n"
        cell += "Profs: "    + j['FACULTY'] + "\n"
        cell += "Enrolled: " + str(j['ENR']) + "/" + str(j['CAPACITY']) + "\n"
        cell += "Room: "     + j['ROOM'] + "\n"
        message += cell
      update.message.reply_text(message)
  except:
    print("ERROR")

def error():
  print("SOME ERROR")

def main():
  try:
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, getCourseName))
    dp.add_error_handler(error)

    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://<appname>.herokuapp.com/" + TOKEN)

    updater.idle()
  except:
    print("ERROR in MAIN")


if __name__ == '__main__':
  main()