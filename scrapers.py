import os
import requests as req

def getSearchData(data):
  try:
    sh = "sh getSearchData.sh {}".format(data)
    courseData = os.popen(sh).read()
    courseData = eval(courseData)
    courseData = courseData['data']
    if len(courseData) > 0:
      return courseData
    return -1
  except:
    return -1


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
    courseSchedule = eval(courseSchedule.replace('false', 'False'))
    return courseSchedule
  except:
    return -1