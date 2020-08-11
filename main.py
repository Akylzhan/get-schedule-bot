import os
import requests as req
import logging
import random


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler, ConversationHandler
from telegram.ext.dispatcher import run_async
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

import utilities
import messages


DEBUG = os.environ.get('PROD') is None
TOKEN = "949738996:AAHVrnVCsv4LUP0y-0FNPS_dCs2lCVhcQ08"

if DEBUG:
  TOKEN = "1201714568:AAHLzZRyHaW3jGXawZJP2-VD8Wr_tMJXa2E"

# manually change termId in getInfo.sh
termId = int(eval(open("data/semesters.json", 'r').read())[0]['ID'])
courseList = eval(open("data/courseList.json", 'r').read())['data']
for course in courseList:
  for key in course:
    course[key] = " ".join(course[key].strip().split())

nufypCourses = [
  'FEAP 001', 'FBIO 011', 'FBUS 011', 'FCHM 011',
  'FGEO 011', 'FHUM 011', 'FPHY 011', 'FMATH 001'
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
  try:
    update.message.reply_text(messages.startMsg)
  except:
    print("ERROR in START")

# TODO
# change this to call external function to do this entirely
# just to write `rate name` and also `/rate name`
# check line 88
def listOfProfs(update, context):
  try:
    if len(" ".join(context.args)) < 5:
      update.message.reply_text(random.choice(messages.smallQueryMsg))
      return

    arg1 = context.args[0]
    arg2 = context.args[0]
    if len(context.args) > 1:
      arg2 = context.args[1]

    profs = utilities.searchProf(arg1, arg2)
    if len(profs) == 0:
      update.message.reply_text("Could not find this prof")
      return

    keyboard = []
    for prof in profs:
      name = prof['NAME']
      id = prof['ID']
      keyboard.append([InlineKeyboardButton(name, callback_data="rate"+name+";"+id)])

    replyMarkup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)

  except (IndexError):
    update.message.reply_text("Usage: \n/rate ProfName ProfSurname\nor\n/rate ProfName")
  except:
    print(' '.join(context.args) + " ERROR in listOfProfs")

@run_async
def getCourseName(update, context):
  try:
    print(update.message.text)
    data = update.message.text.lower()
    if len(data) < 3:
      update.message.reply_text(random.choice(messages.smallQueryMsg))
      return
    if data.split()[0] == 'rate':
      update.message.reply_text("Usage: \n/rate ProfName ProfSurname\nor\n/rate ProfName")
      return

    searchResult = utilities.getSearchData(courseList, data)

    if searchResult == -1:
      update.message.reply_text(random.choice(messages.emptyCourseListMsg))
      return

    keyboard = []
    for i in range(0, len(searchResult), 2):
      coursePos1 = searchResult[i]
      course1 = courseList[coursePos1]
      button1 = (course1['ABBR'] + " " + course1['TITLE'])
      keyboard.append([InlineKeyboardButton(button1, callback_data="i"+str(coursePos1))])

      if i + 1 != len(searchResult):
        coursePos2 = searchResult[i + 1]
        course2 = courseList[coursePos2]
        button2 = (course2['ABBR'] + " " + course2['TITLE'])
        keyboard[-1].append(InlineKeyboardButton(button2, callback_data="i"+str(coursePos2)))

    replyMarkup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)
  except:
    context.bot.send_message(chat_id=384134675, text=update.message.text)


def sendCourseInfo(update, context):
  try:
    query = update.callback_query
    query.answer()
    coursePos = int(query.data[1:])
    formattedInfo = utilities.formattedCourseInfo(courseList[coursePos], termId)

    keyboard = [[InlineKeyboardButton("Schedule", callback_data="s"+str(coursePos))]]
    replyMarkup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=formattedInfo, reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)
  except:
    context.bot.send_message(chat_id=384134675, text=courseList[int(query.data[1:])]['ABBR']+" ERROR in sendCourseInfo")


def sendSchedule(update, context):
  # try:
    query = update.callback_query
    query.answer()
    coursePos = int(query.data[1:])
    abbr = courseList[coursePos]['ABBR']

    if abbr in nufypCourses:
      context.bot.send_message(chat_id=update.effective_message.chat_id, text=messages.longScheduleMsg)
      return

    courseId = courseList[coursePos]['COURSEID']
    title = abbr + " " + courseList[coursePos]['TITLE']

    formattedSchedule = utilities.formattedSchedule(courseId, termId)
    if formattedSchedule == -1:
      query.edit_message_text(text="cannot find schedule or it is too long :(")
      context.bot.send_message(chat_id=384134675, text="ERROR in formattedSchedule")
      return

    for c in utilities.replaceMD:
      title = title.replace(c, '\\'+c)

    first_part = formattedSchedule[:25]
    second_part = formattedSchedule[25:]

    if len(second_part) > 0:
      first_part = f'*{title}*\nFIRST PART OF SCHEDULE\n{"".join(first_part)}'
      second_part = f'*{title}*\nSECOND PART OF SCHEDULE\n{"".join(second_part)}'
      query.edit_message_text(text=first_part, parse_mode=ParseMode.MARKDOWN_V2)
      context.bot.send_message(chat_id=update.effective_message.chat_id, text=second_part, parse_mode=ParseMode.MARKDOWN_V2)
    else:
      first_part = f'*{title}*\n{"".join(first_part)}'
      query.edit_message_text(text=first_part, parse_mode=ParseMode.MARKDOWN_V2)
  # except:
  #   context.bot.send_message(chat_id=384134675, text=courseList[int(query.data[1:])]['ABBR']+" ERROR in sendSchedule")


def rateProf(update, context):
  query = update.callback_query
  query.answer()
  data = query.data[4:].split(';')
  name = data[0]
  id = data[1]
  keyboard = [
    [InlineKeyboardButton('1 star', callback_data="ratingbutton"+name+";"+id+';1')],
    [InlineKeyboardButton('2 star', callback_data="ratingbutton"+name+";"+id+';2')],
    [InlineKeyboardButton('3 star', callback_data="ratingbutton"+name+";"+id+';3')],
    [InlineKeyboardButton('4 star', callback_data="ratingbutton"+name+";"+id+';4')],
    [InlineKeyboardButton('5 star', callback_data="ratingbutton"+name+";"+id+';5')]
  ]
  for c in utilities.replaceMD:
    name = name.replace(c, '\\' + c)
  replyMarkup = InlineKeyboardMarkup(keyboard)
  query.edit_message_text(text=f'Please rate *{name}*:', reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)


def ratingButton(update, context):
  query = update.callback_query
  data = query.data[12:].split(';')
  name = data[0]
  id = data[1]
  rating = data[2]

  rating, count_ratings = utilities.rateProf(id, str(update.effective_message.chat_id), rating)
  rating = str(rating)
  count_ratings = str(int(count_ratings))
  for c in utilities.replaceMD:
      rating = rating.replace(c, '\\' + c)
      name = name.replace(c, '\\' + c)
  query.edit_message_text(text=f'Thanks for rating *{name}*\nCurrent rating: {rating} \\({count_ratings} people rated\\)', parse_mode=ParseMode.MARKDOWN_V2)


def error():
  print("OTHER ERROR")


def main():
  updater = Updater(TOKEN, use_context=True, workers=16)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("rate", listOfProfs))
  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, getCourseName))
  dp.add_handler(CallbackQueryHandler(sendCourseInfo, pattern="^i"))
  dp.add_handler(CallbackQueryHandler(sendSchedule, pattern="^s"))
  dp.add_handler(CallbackQueryHandler(rateProf, pattern="^rate"))
  dp.add_handler(CallbackQueryHandler(ratingButton, pattern="^ratingbutton"))
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
