import os
import requests as req

replaceMD = ['`', '(', ')', '+', '-', '.', '!']


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

  for j in schedule:
    cell = "\n"
    cell += f"Type: *{j['ST']}*\n"
    cell += f"Days: {j['DAYS'].replace('R', 'R(Thursday)')}\n"
    cell += f"Times: {j['TIMES']}\n"
    cell += f"Profs: *{j['FACULTY'].replace('<br>', ',')}*\n"

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
  r = req.Session()
  headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate',
      'Referer': 'https://registrar.nu.edu.kz/index.php?q=user/login',
      'DNT': '1',
      'Connection': 'close',
      'Upgrade-Insecure-Requests': '1'
  }
  url = "https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json?method=getSchedule&courseId={}&termId={}"
  try:
    courseSchedule = r.post(url.format(courseId, termId), headers=headers).text
    if len(courseSchedule) > 2:
      courseSchedule = eval(courseSchedule.replace('false', 'False'))
      return courseSchedule
  except:
    return -1