from . import helpers

import requests as req
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



replaceMD = ['`', '(', ')', '+', '-', '.', '!']
def replaceMardownReservedChars(arg):
  for c in replaceMD:
    arg = arg.replace(c, '\\' + c)
  return arg

def formatCourseInfo(course, termId):
  message = ""
  message += f"*{course['ABBR']}* - *{course['TITLE']}*\n"
  message += f"ECTS: {course['CRECTS']}\n"
  message += f"Prereqs: {course['PREREQ']}\n"
  message += f"Coreqs: {course['COREQ']}\n"
  message += f"Antireqs: {course['ANTIREQ']}\n"
  message += f"Description: {course['SHORTDESC']}\n"

  return replaceMardownReservedChars(message)


def formatFaculty(facultyList):
  faculty = []

  if '<br>' in facultyList:
    faculty = facultyList.split('<br>')
  else:
    s = facultyList.split()
    faculty.append(' '.join(s[:2]))
    faculty.append(' '.join(s[-2:]))

  formattedFaculty = []
  for i in range(0, len(faculty)):
    # all combinations
    profName, profId = helpers.getProfId(faculty[i])

    profRating, countRatings = 0, 0
    # check if we calculated prof rating before
    if profId in profRatingSet:
      profRating, countRatings = profRatingSet[profId]
    else:
      profRating, countRatings = helpers.showRatingOfProf(profId)
      profRatingSet[profId] = [profRating,countRatings]

    if rating > 0:
      formattedFaculty.append(f'{profName} ({profRating}/5.0 - {countRatings} people rated)')
    else:
      formattedFaculty.append(faculty[i])
  faculty = ', '.join(set([i.replace(',','') for i in formattedFaculty]))

  return faculty


def formatSchedule(courseId, termId):
  message = []
  schedule = requestSchedule(courseId, termId)
  if schedule == -1:
    return -1
  profRatingSet = {}

  for course in schedule:
    cell = "\n"
    cell += f"Type: *{course['ST']}*\n"
    cell += f"Days: {course['DAYS']}\n"
    cell += f"Times: {course['TIMES']}\n"
    cell += f"Profs: *{formatFaculty(course['FACULTY'])}*\n"

    percentage = 0
    if int(course['CAPACITY']) > 0:
      percentage = int(course['ENR']) / int(course['CAPACITY'])

    enrEmoji = "🟢"
    if percentage >= 0.49:
      enrEmoji = "🟡"
    if percentage >= 0.76:
      enrEmoji = "🟠"
    if percentage >= 0.99:
      enrEmoji = "🔴"

    cell += f"Enr: {enrEmoji}*{str(course['ENR'])}/{str(course['CAPACITY'])}*\n"
    cell += f"Room: {course['ROOM']}\n"
    message.append(cell)

  for i in range(0, len(message)):
    message[i] = replaceMardownReservedChars(message[i])
  return message


def requestSchedule(courseId, termId):
  try:
    courseSchedule = r.post(getScheduleUrl.format(courseId, termId), headers=getScheduleHeaders).text
    if len(courseSchedule) > 2:
      courseSchedule = eval(courseSchedule.replace('false', 'False'))
      return courseSchedule
    return -1
  except:
    return -1

def requestJoke():
  try:
    url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist&format=txt"
    return req.get(url).text
  except:
    return -1
