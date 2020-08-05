import os
import requests as req

def getSearchData(data, query):
  result = []
  words = query.split()
  occurs = {}
  for i in data:
      occurs[i['ABBR']] = [0, i]
      for x in words:
        if x.lower() in (i['ABBR']).lower():
          occurs[i['ABBR']][0] += 1
          continue
        if x.lower() in (i['TITLE']).lower():
          occurs[i['ABBR']][0] += 1
      if(occurs[i['ABBR']][0] < len(words)):
          del occurs[i['ABBR']]
  res = sorted(occurs.items(), key=lambda x: x[1][0], reverse=True)
  for i, j in res:
      result.append(j[1])

  if len(result) > 0:
    return result
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
    if len(courseSchedule) > 2:
      courseSchedule = eval(courseSchedule.replace('false', 'False'))
      return courseSchedule
  except:
    return -1
