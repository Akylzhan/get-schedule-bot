import os
import requests as req
import time

from database import Database
replaceMD = ['`', '(', ')', '+', '-', '.', '!']

db = Database()

instr = eval(open('data/instructors.json', 'r').read())
instructors = {}
for i in instr:
  instructors[i['NAME']] = i['ID']


r = req.Session()
getScheduleHeaders = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate',
      'Referer': 'https://registrar.nu.edu.kz/index.php?q=user/login',
      'DNT': '1',
      'Connection': 'close',
      'Upgrade-Insecure-Requests': '1'
  }
getScheduleUrl = "http://178.91.253.115/my-registrar/public-course-catalog/json?method=getSchedule&courseId={}&termId={}"


def rateProf(profId, userId, rating):
  return db.rate(profId, userId, rating)


def showRatingOfProf(profId):
  return db.calculateRating(profId)


def searchProf(arg1, arg2):
  result = []
  arg1 = arg1.lower()
  arg2 = arg2.lower()
  for name in instructors:
    lower_name = name.lower()
    if arg1 in lower_name and arg2 in lower_name:
      result.append({"NAME": name, "ID": instructors[name]})
  return result


def getProfId(nameSurname):
  nameSurname = nameSurname.replace(',', '')
  delim = ' '

  if ',' in nameSurname:
    delim = ',' + delim
  name, surname = nameSurname.split(delim)[:2]

  for i in instructors:
    if name in i and surname in i:
      return i, instructors[i]


def getSearchData(data, query):
  result = []
  words = query.split()
  occurs = {}

  for i in range(0, len(data)):
    abbr = data[i]['ABBR'].lower()
    title = data[i]['TITLE'].lower()
    occurs[i] = [0, i]

    for x in words:
      x = x.lower()
      if x in abbr:
        occurs[i][0] += 1
        continue
      if x in title:
        occurs[i][0] += 1

    if occurs[i][0] < len(words):
      del occurs[i]

  result = [j[1] for i,j in sorted(occurs.items(), key=lambda x: x[1][0], reverse=True)]

  if len(result) > 0:
    return result
  return -1


def formattedCourseInfo(course, termId):
  message = ""
  message += f"*{course['ABBR']}* - *{course['TITLE']}*\n"
  message += f"ECTS: {course['CRECTS']}\n"
  message += f"Prereqs: {course['PREREQ']}\n"
  message += f"Coreqs: {course['COREQ']}\n"
  message += f"Antireqs: {course['ANTIREQ']}\n"
  message += f"Description: {course['SHORTDESC']}\n"

  for c in replaceMD:
    message = message.replace(c, "\\" + c)
  return message


def formattedSchedule(courseId, termId):
  message = ""
  schedule = getSchedule(courseId, termId)
  if schedule == -1:
    return -1
  profRatingSet = {}
  for j in schedule:
    cell = "\n"
    cell += f"*{j['ST']}*\n"
    cell += f"Days: {j['DAYS']}\n"
    cell += f"Times: {j['TIMES']}\n"

    faculty = []
    if '<br>' in j['FACULTY']:
      faculty = j['FACULTY'].split('<br>')
    else:
      s = j['FACULTY'].split()
      faculty.append(' '.join(s[:2]))
      faculty.append(' '.join(s[-2:]))
    for i in range(0, len(faculty)):
      # all combinations
      name, profId = getProfId(faculty[i])

      rating = 0
      if profId in profRatingSet:
        rating = profRatingSet[profId]
      else:
        rating, count_ratings = showRatingOfProf(profId)
        profRatingSet[profId] = rating

      if rating > 0:
        faculty[i] = f'{name} ({str(rating)}/5.0# {count_ratings} rated)'
    faculty = ', '.join(set([i.replace(',','').replace('#',',') for i in faculty]))

    cell += f"Profs: *{faculty}*\n"

    percentage = 0
    if int(j['CAPACITY']) > 0:
      percentage = int(j['ENR']) / int(j['CAPACITY'])

    enrEmoji = "🟢"
    if percentage >= 0.49:
      enrEmoji = "🟡"
    if percentage >= 0.76:
      enrEmoji = "🟠"
    if percentage >= 0.99:
      enrEmoji = "🔴"

    cell += f"Enrolled: {enrEmoji}*{str(j['ENR'])}/{str(j['CAPACITY'])}*\n"
    cell += f"Room: {j['ROOM']}\n"
    message += cell

  for c in replaceMD:
    message = message.replace(c, "\\" + c)
  return message


def getSchedule(courseId, termId):
  try:
    courseSchedule = r.post(getScheduleUrl.format(courseId, termId), headers=getScheduleHeaders).text
    if len(courseSchedule) > 2:
      courseSchedule = eval(courseSchedule.replace('false', 'False'))
      return courseSchedule
  except:
    return -1