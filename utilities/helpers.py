import os
import time

from .database import Database
from . import formatters

replaceMardownReservedChars = formatters.replaceMardownReservedChars

instr = eval(open('data/instructors.json', 'r').read())
instructors = {}
for i in instr:
    instructors[i['NAME']] = i['ID']

db = Database()


def rateProf(profId, userId, rating):
    return db.rate(profId, userId, rating)


def showRatingOfProf(profId):
    return db.calculateRating(profId)


def searchProf(args):
    profName = args[0].lower()
    profSurname = args[0].lower()
    if len(args) > 1:
        profSurname = args[1].lower()

    result = []
    for fullName in instructors:
        lowerFullName = fullName.lower()
        if profName in lowerFullName and profSurname in lowerFullName:
            result.append({"NAME": fullName, "ID": instructors[fullName]})
    return result


def getProfId(nameSurname):
    nameSurname = nameSurname.replace(',', '')
    delim = ' '

    if ',' in nameSurname:
        delim = ',' + delim
    profName, profSurname = nameSurname.split(delim)[:2]

    for fullName in instructors:
        if profName in fullName and profSurname in fullName:
            return fullName, instructors[fullName]


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

    result = [
        j[1]
        for i, j in sorted(occurs.items(), key=lambda x: x[1][0], reverse=True)
    ]

    if len(result) > 0:
        return result
    return -1


def getSchedule(courseId, termId):
    return formatters.formatSchedule(courseId, termId)


def getCourseInfo(courseId, termId):
    return formatters.formatCourseInfo(courseId, termId)


def getJoke():
    return formatters.requestJoke()
