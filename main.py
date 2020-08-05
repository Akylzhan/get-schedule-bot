import os
import requests as req
import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler, ConversationHandler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

import utilities
import messages


DEBUG = os.environ.get('PROD') is None
TOKEN = "949738996:AAHVrnVCsv4LUP0y-0FNPS_dCs2lCVhcQ08"

if DEBUG:
  TOKEN = "1201714568:AAHLzZRyHaW3jGXawZJP2-VD8Wr_tMJXa2E"

# TODO: add priorities
# TODO: add other term_ids
# TODO: add department ids
termId = 521
data = eval(open("data.json").read())['data']
for course in data:
  for key in course:
    course[key] = " ".join(course[key].strip().split())


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
  try:
    update.message.reply_text(messages.startMsg)
  except:
    print("ERROR in START")


def getCourseName(update, context):
  print(update.message.text)
  try:
    query = update.message.text.lower()
    if len(query) < 3:
      update.message.reply_text(random.choice(messages.smallQueryMsg))
      return

    courseList = utilities.getSearchData(data, query)

    if courseList == -1:
      update.message.reply_text(random.choice(messages.emptyCourseListMsg))
      return

    keyboard = []
    for i in range(0, len(courseList), 2):
      course1 = courseList[i]
      button1 = (course1['ABBR'] + " " + course1['TITLE'])[:63]
      keyboard.append([InlineKeyboardButton(button1, callback_data="i"+button1)])
      if i + 1 != len(courseList):
        course2 = courseList[i + 1]
        button2 = (course2['ABBR'] + " " + course2['TITLE'])[:63]
        keyboard[-1].append(InlineKeyboardButton(button2, callback_data="i"+button2))

    replyMarkup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)
  except:
    context.bot.send_message(chat_id=384134675, text=update.message.text)

def sendCourseInfo(update, context):
  query = update.callback_query
  query.answer()
  formattedInfo = ""
  courseId = ""
  for course in data:
    if (course['ABBR'] + " " + course['TITLE'])[:63] == query.data[1:]:
      formattedInfo, courseId = utilities.formatCourseInfo(course, termId)
      courseId = courseId + ";" + course['ABBR'] + " " + course['TITLE'][:50]
      break
  keyboard = [[InlineKeyboardButton("Schedule", callback_data="s"+courseId)]]
  replyMarkup = InlineKeyboardMarkup(keyboard)
  query.edit_message_text(text=formattedInfo, reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)

# also convert schedule to multiple buttons
def sendSchedule(update, context):
  try:
    query = update.callback_query
    query.answer()
    courseId, title = query.data.split(';')
    courseId = courseId[1:]
    formattedSchedule = utilities.formattedSchedule(courseId, termId)
    if formattedSchedule == -1:
      query.edit_message_text(text="cannot find schedule")
      context.bot.send_message(chat_id=384134675, text=update.message.text + "ERROR in sendSchedule")
      return
    for c in utilities.replaceMD:
      title.replace(c, '\\'+c)
    formattedSchedule = f'*{title}*\n{formattedSchedule}'
    query.edit_message_text(text=formattedSchedule, parse_mode=ParseMode.MARKDOWN_V2)
  except:
    query.edit_message_text(text="schedule is too long like my pp")

def error():
  print("OTHER ERROR")


def main():
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, getCourseName))
  dp.add_handler(CallbackQueryHandler(sendCourseInfo, pattern="^i"))
  dp.add_handler(CallbackQueryHandler(sendSchedule, pattern="^s"))
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
