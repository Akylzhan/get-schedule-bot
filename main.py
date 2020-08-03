import os
import requests as req

import scrapers

token = "949738996:AAHVrnVCsv4LUP0y-0FNPS_dCs2lCVhcQ08"
# TODO: add other term_ids
# TODO: add department ids
term_id = 521

data = eval(open("data.json", "r").read())['data']


import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
  update.message.reply_text('Hello! Send me course name (eg. CSCI 152 or public speaking) and I will send you schedule of this course')

def getCourseName(update, context):
  print(update.message.text)
  courseInfo = update.message.text.lower()
  courseInfo = scrapers.getSearchData(data, courseInfo)

  if courseInfo == -1:
    update.message.reply_text("An error occured, consider changing search text")
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
      update.message.reply_text("An error occured, consider changing search text")
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


def main():
  updater = Updater(token, use_context=True)
  PORT = int(os.environ.get('PORT', '8443'))
  updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=token)
  updater.bot.set_webhook("https://schedule-bot-akylzhan.herokuapp.com/" + token)

  # Get the dispatcher to register handlers
  dp = updater.dispatcher

  # on different commands - answer in Telegram
  dp.add_handler(CommandHandler("start", start))

  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, getCourseName))

  updater.start_polling()

  updater.idle()


if __name__ == '__main__':
  main()