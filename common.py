import models
import os
import datetime
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Record(list):
    pass

# returns a tuple of (score, entries_by_date)
def getDays(user):
    your_score = 0
    index = -1
    date = []
    yourdays = Record()
    # run the query to get all entries for this user
    parent_key = db.Key.from_path("User", user.user_id())
    entries = models.Entry().all()
    entries.ancestor(parent_key)
    entries.order('-date')
    your_entries = entries.run()
    for entry in your_entries:
        if date != entry.date.date():
            date = entry.date.date()
            day = Record()
            day.date = date
            yourdays.append(day)
            index += 1
        your_score += entry.points
        yourdays[index].append(entry)
    yourdays.name = user.nickname().split("@")[0]
    yourdays.score = your_score
    yourdays.nickname = user.nickname()
    return yourdays
    
def renderDays(user, path):
    yourdays = getDays(user)
    today = Record()
    today.date = datetime.datetime.now().date()
    if len(yourdays) == 0 or yourdays[0].date != today.date:
        yourdays.insert(0, today)
    template_values = {
       'yourdays' : yourdays
    }
    return template.render(path, template_values)
    
def getCompetitors(user):
    contest = models.Contest.all()
    contest.filter('user =', user)
    user_contest = contest.get()
    if user_contest:
        return user_contest.participants
    return []