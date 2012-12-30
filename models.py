from google.appengine.ext import db
from google.appengine.api import users

exercises = { 'pushups' : ('pushups', 'reps', 10),
              'pullups' : ('pullups', 'reps', 10),
              'burpees' : ('burpees', 'reps', 20),
              'squats' : ('squats', 'reps', 10),
              'punching' : ('punching', 'minutes', 60),
              'jumping' : ('jumping', 'minutes', 40),
              'plank' : ('plank', 'minutes', 60) }

class Entry(db.Model):
  reps = db.IntegerProperty()
  points = db.IntegerProperty()
  date = db.DateTimeProperty()
  name = db.StringProperty(choices=set(exercises.keys()))
    
class Contest(db.Model):
  participants = db.ListProperty(users.User)
  user = db.UserProperty()

