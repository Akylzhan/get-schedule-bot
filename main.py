import os
import requests as req
import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import scrapers
import messages


DEBUG = os.environ.get('PROD') is None
TOKEN = "949738996:AAHVrnVCsv4LUP0y-0FNPS_dCs2lCVhcQ08"

if DEBUG:
  TOKEN = "1201714568:AAHLzZRyHaW3jGXawZJP2-VD8Wr_tMJXa2E"

# TODO: add other term_ids
# TODO: add department ids
term_id = 521
data = eval(open("data.json").read())['data']
for course in data:
  for key in course:
    course[key] = " ".join(course[key].strip().split())

replace_md = ['`', '(', ')', '+', '-', '.', '!']


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
  try:
    update.message.reply_text('Hello! Send me course name (eg. CSCI 152 or public speaking) and I will send you schedule of this course')
  except:
    print("ERROR in START")

def getCourseName(update, context):
  # print(update.message.text)
  # try:
    query = update.message.text.lower()
    if len(query) < 3:
      update.message.reply_text(random.choice(messages.smallQueryMsg))
      return
    courseList = scrapers.getSearchData(data, query)

    if courseList == -1:
      update.message.reply_text(random.choice(messages.emptyCourseListMsg))
      return

    for i in courseList:
      message = ""
      message += "Abbr: *"    + i["ABBR"] + "*\n"
      message += "Title: "   + i["TITLE"] + "\n"
      message += "ECTS: "    + i["CRECTS"] + "\n"
      message += "Prereqs: " + i["PREREQ"] + "\n"
      message += "Coreqs: " + i["COREQ"] + "\n"
      message += "Antireqs: " + i["ANTIREQ"] + "\n"
      message += "Description: " + i["SHORTDESC"] + "\n"

      schedule = scrapers.getSchedule(i['COURSEID'], term_id)
      if schedule == -1:
        update.message.reply_text(random.choice(messages.emptyCourseListMsg))
        return
      for j in schedule:
        cell = "\n"
        cell += "Type: *"     + j['ST'] + "*\n"
        cell += "Days: "     + j['DAYS'] + "\n"
        cell += "Times: "    + j['TIMES'].replace('R', "R(Thursday)") + "\n"
        cell += "Profs: *"    + j['FACULTY'].replace('<br>', ',') + "*\n"
        
        percentage = 0
        if int(j['CAPACITY']) > 0:
          percentage = int(j['ENR']) / int(j['CAPACITY'])
        enr_emoji = "🟢"
        if percentage >= 0.50:
          enr_emoji = "🟠"
        if percentage >= 0.99:
          enr_emoji = "🔴"
        cell += f"Enrolled: {enr_emoji}*{str(j['ENR'])}/{str(j['CAPACITY'])}*\n"
        
        cell += "Room: " + j['ROOM'] + "\n"
        message += cell
      for c in replace_md:
        message = message.replace(c, "\\" + c)
      update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
  # except:
    # print("ERROR in getCourseName")

def error():
  print("OTHER ERROR")

def main():
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))

  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, getCourseName))
  dp.add_error_handler(error)
  
  if DEBUG:
    updater.start_polling()
  else:
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://schedule-bot-akylzhan.herokuapp.com/" + TOKEN)
  
  updater.idle()


if __name__ == '__main__':
  main()
