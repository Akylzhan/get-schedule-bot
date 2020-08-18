import psycopg2
import os

class Database:
  def __init__(self, table="users"):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    self.connection = None
    if DATABASE_URL is None:
      self.connection = psycopg2.connect(
                  host="localhost",
                  database="training",
                  user="akylzhansauranbay")
    else:
      self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    self.tableName = table
    self.cursor = self.connection.cursor()
    
    instructors = open('data/instructors.json', 'r').read()
    self.instructors = eval(instructors)

    courseIds = open('data/courseList.json', 'r').read()
    courseIds = eval(courseIds)['data']
    self.courseIds = []
    for i in courseIds:
      self.courseIds.append(i['COURSEID'])

    self.createTable()


  def createTable(self):
    createRatingsTableQuery = """CREATE TABLE
                          IF NOT EXISTS bot_table
                          (prof_id TEXT UNIQUE,
                          ratings TEXT)"""
    createLinksTableQuery = """CREATE TABLE
                          IF NOT EXISTS links_list
                          (course_id TEXT UNIQUE,
                          links TEXT)"""
    insertRatingsRowQuery = """INSERT INTO
                     bot_table(prof_id) VALUES(%s)
                     ON CONFLICT (prof_id) DO NOTHING"""
    insertLinksRowQuery = """INSERT INTO
                     links_list(course_id) VALUES(%s)
                     ON CONFLICT (course_id) DO NOTHING
                     """
    self.cursor.execute(createRatingsTableQuery)
    self.cursor.execute(createLinksTableQuery)

    for i in self.instructors:
      values = (i['ID'],)
      self.cursor.execute(insertRatingsRowQuery, values)
    for i in self.courseIds:
      values = (i,)
      self.cursor.execute(insertLinksRowQuery, values)
    self.connection.commit()


  def addLink(self, id, section, link):
    insertQuery = """UPDATE links_list SET links = '{}' WHERE course_id = '{}'"""
    oldList = self.listOfLinks(id)
    if oldList is None:
      self.cursor.execute(insertQuery.format(f'{section} {link},', id))
    # TODO


  def listOfLinks(self, id):
    getLinksQuery = """SELECT links FROM links_list WHERE course_id = '{}'"""
    self.cursor.execute(getLinksQuery.format(id))
    return self.cursor.fetchone()[0]


  def rate(self, profId, userId, rating):
    insertQuery = """UPDATE bot_table SET ratings = '{}' WHERE prof_id = '{}'"""
    oldRating = self.listOfRatings(profId)
    if oldRating is None:
      self.cursor.execute(insertQuery.format(f'{userId} {rating},', profId))
    else:
      oldRating = oldRating.split(',')
      modify, oldRating = self.tryModifyingRating(oldRating, userId, rating)
      oldRating = ','.join(oldRating)

      if modify:
        self.cursor.execute(insertQuery.format(oldRating, profId))
      else:
        self.cursor.execute(insertQuery.format(f'{oldRating}{userId} {rating},', profId))

    self.connection.commit()
    return self.calculateRating(profId)


  def tryModifyingRating(self, oldRating, userId, rating):
    for i, r in enumerate(oldRating):
      r = r.split()
      if r and r[0] == userId:
        r[1] = rating
        oldRating[i] = ' '.join(r)
        return True, oldRating
    return False, oldRating


  def listOfRatings(self, profId):
    getRatingQuery = """SELECT ratings FROM bot_table WHERE prof_id = '{}'"""
    self.cursor.execute(getRatingQuery.format(profId))
    return self.cursor.fetchone()[0]


  def calculateRating(self, profId):
    ratings = self.listOfRatings(profId)
    if not ratings:
      return 0, 0
    ratings = ratings.split(',')
    count_ratings = len(ratings) - 1
    s = 0
    for r in ratings:
      r = r.split()
      if r:
        s += int(r[1])
    return round(s / (count_ratings), 2), count_ratings

# update bot_table set ratings = null where prof_id = '8703';