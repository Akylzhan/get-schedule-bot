import os
import requests as req
import logging
import random


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler, ConversationHandler
from telegram.ext.dispatcher import run_async
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from utilities import helpers
import messages


DEBUG = os.environ.get('PROD') is None
TOKEN = os.environ.get('BOT_TOKEN')

if DEBUG:
  TOKEN = open('debug_token.txt', 'r').read()

# manually change termId in getInfo.sh
termId = int(eval(open("data/semesters.json", 'r').read())[0]['ID'])
courseList = eval(open("data/courseList.json", 'r').read())['data']
for course in courseList:
  for key in course:
    course[key] = " ".join(course[key].strip().split())


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
  try:
    update.message.reply_text(messages.startMsg)
  except:
    if DEBUG:
      raise
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

    profs = helpers.searchProf(context.args)
    if len(profs) == 0:
      update.message.reply_text("Could not find this prof")
      return

    keyboard = []
    for prof in profs:
      profName = prof['NAME']
      profId = prof['ID']
      keyboard.append([InlineKeyboardButton(profName, callback_data="rate"+profName+";"+profId)])

    replyMarkup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)

  except (IndexError):
    update.message.reply_text("Usage: \n/rate ProfName ProfSurname\nor\n/rate ProfName")
  except:
    if DEBUG:
      raise
    print(' '.join(context.args) + " ERROR in listOfProfs")

@run_async
def listOfProfRatings(update, context):
  try:
    if len(" ".join(context.args)) < 5:
      update.message.reply_text(random.choice(messages.smallQueryMsg))
      return

    arg1 = context.args[0]
    arg2 = context.args[0]
    if len(context.args) > 1:
      arg2 = context.args[1]

    profs = helpers.searchProf(arg1, arg2)
    if len(profs) == 0:
      update.message.reply_text("Could not find this prof")
      return

    keyboard = []
    for prof in profs:
      profName = prof['NAME']
      profId = prof['ID']
      keyboard.append([InlineKeyboardButton(profName, callback_data="rating"+profName+";"+profId)])

    replyMarkup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)

  except (IndexError):
    if DEBUG:
      raise
    update.message.reply_text("Usage: \n/rating ProfName ProfSurname\nor\n/rating ProfName")
  except:
    if DEBUG:
      raise
    print(' '.join(context.args) + " ERROR in listOfProfRatings")


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

    searchResult = helpers.getSearchData(courseList, data)

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
    if DEBUG:
      raise
    context.bot.send_message(chat_id=384134675, text=update.message.text)


def sendCourseInfo(update, context):
  try:
    query = update.callback_query
    query.answer()
    coursePos = int(query.data[1:])
    formattedInfo = helpers.getCourseInfo(courseList[coursePos], termId)

    keyboard = [[InlineKeyboardButton("Schedule", callback_data="s"+str(coursePos))]]
    replyMarkup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=formattedInfo, reply_markup=replyMarkup, parse_mode=ParseMode.MARKDOWN_V2)
  except:
    if DEBUG:
      raise
    context.bot.send_message(chat_id=384134675, text=courseList[int(query.data[1:])]['ABBR']+" ERROR in sendCourseInfo")


def sendSchedule(update, context):
  try:
    query = update.callback_query
    query.answer()
    coursePos = int(query.data[1:])
    abbr = courseList[coursePos]['ABBR']

    courseId = courseList[coursePos]['COURSEID']
    title = abbr + " " + courseList[coursePos]['TITLE']

    formattedSchedule = helpers.getSchedule(courseId, termId)
    if formattedSchedule == -1:
      query.edit_message_text(text="cannot find schedule or it is too long :(")
      context.bot.send_message(chat_id=384134675, text="ERROR in getSchedule")
      return

    title = helpers.replaceMardownReservedChars(title)

    first_part = formattedSchedule[:25]
    second_part = formattedSchedule[25:50]
    third_part = formattedSchedule[50:]

    if len(second_part) > 0:
      first_part = f'*{title}*\nFIRST PART OF SCHEDULE\n{"".join(first_part)}'
      second_part = f'*{title}*\nSECOND PART OF SCHEDULE\n{"".join(second_part)}'

      query.edit_message_text(text=first_part, parse_mode=ParseMode.MARKDOWN_V2)

      context.bot.send_message(chat_id=update.effective_message.chat_id,
                               text=second_part,
                               parse_mode=ParseMode.MARKDOWN_V2)

      if len(third_part) > 0:
        third_part = f'*{title}*\nTHIRD PART OF SCHEDULE\n{"".join(third_part)}'

        context.bot.send_message(chat_id=update.effective_message.chat_id,
                                 text=third_part,
                                 parse_mode=ParseMode.MARKDOWN_V2)
    else:
      first_part = f'*{title}*\n{"".join(first_part)}'
      query.edit_message_text(text=first_part, parse_mode=ParseMode.MARKDOWN_V2)

  except:
    if DEBUG:
      raise
    context.bot.send_message(chat_id=384134675,
                             text=courseList[int(query.data[1:])]['ABBR']+" ERROR in sendSchedule")


def sendRatingProf(update, context):
  query = update.callback_query
  query.answer()
  data = query.data[6:].split(';')

  profName, profId = data
  profRating, countRatings = helpers.showRatingOfProf(profId)

  msg = f'Rating of:\n*{profName}* - {profRating}/5.0 ({countRatings} people rated)'
  msg = helpers.replaceMardownReservedChars(msg)

  query.edit_message_text(text=msg,
                          parse_mode=ParseMode.MARKDOWN_V2)

def rateProf(update, context):
  query = update.callback_query
  query.answer()
  data = query.data[4:].split(';')

  profName, profId = data
  keyboard = [
    [InlineKeyboardButton('1 star', callback_data="ratebutton"+profName+";"+profId+';1')],
    [InlineKeyboardButton('2 star', callback_data="ratebutton"+profName+";"+profId+';2')],
    [InlineKeyboardButton('3 star', callback_data="ratebutton"+profName+";"+profId+';3')],
    [InlineKeyboardButton('4 star', callback_data="ratebutton"+profName+";"+profId+';4')],
    [InlineKeyboardButton('5 star', callback_data="ratebutton"+profName+";"+profId+';5')]
  ]

  profName = helpers.replaceMardownReservedChars(profName)

  replyMarkup = InlineKeyboardMarkup(keyboard)
  query.edit_message_text(text=f'Please rate *{profName}*:',
                          reply_markup=replyMarkup,
                          parse_mode=ParseMode.MARKDOWN_V2)


def ratebutton(update, context):
  query = update.callback_query

  userId = str(update.effective_message.chat_id)

  data = query.data[10:].split(';')
  profName, profId, profRating = data

  profRating, countRatings = helpers.rateProf(profId, userId, profRating)

  profRating = helpers.replaceMardownReservedChars(profRating)
  profName = helpers.replaceMardownReservedChars(profName)

  query.edit_message_text(text=f"Thanks for rating *{profName}*\nCurrent rating: {profRating} \\({countRatings} people rated\\)",
                          parse_mode=ParseMode.MARKDOWN_V2)


def error():
  print("OTHER ERROR")


def main():
  updater = Updater(TOKEN, use_context=True, workers=16)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("rate", listOfProfs))
  dp.add_handler(CommandHandler("rating", listOfProfRatings))
  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, getCourseName))
  dp.add_handler(CallbackQueryHandler(sendCourseInfo, pattern="^i"))
  dp.add_handler(CallbackQueryHandler(sendSchedule, pattern="^s"))
  dp.add_handler(CallbackQueryHandler(sendRatingProf, pattern="^rating"))
   # ratebutton should come before rateProf button;
   # since regex engine finds ^rate
   # faster than ^ratebutton
  dp.add_handler(CallbackQueryHandler(ratebutton, pattern="^ratebutton"))
  dp.add_handler(CallbackQueryHandler(rateProf, pattern="^rate"))
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
