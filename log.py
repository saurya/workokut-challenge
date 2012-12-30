import os
import cgi
import datetime
import re
import models
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

QUERY_CGI_PARAM = "q"
USER_ID_PARAM = "u"
ADD_FN = "addNewEntry"

class LogHandler(webapp2.RequestHandler):
    def getExerciseName(self, query):
        words = [s for s in query.split() if not s.isdigit()]
        return words[0]
        
    def getExercise(self, query):
        return models.exercises[self.getExerciseName(query)]
        
    def getNumber(self, query):
        numbers = [int(s) for s in query.split() if s.isdigit()]
        return numbers[0]    
        
    def get(self):
        user_id = self.request.get(USER_ID_PARAM)
        parent_key = db.Key.from_path("User", user_id)
        contest = models.Contest.all().ancestor(parent_key).get()
        nickname = contest.user.nickname()
        entry = models.Entry(parent=parent_key)
        query = self.request.get(QUERY_CGI_PARAM)
        exercise = self.getExercise(query)
        entry.date = datetime.datetime.now()
        entry.reps = self.getNumber(query)
        entry.points = exercise[2] * entry.reps
        entry.name = exercise[0]
        entry.put()
        
        if user_id:
            # Render JSONP Response
            self.response.headers['Content-Type'] = 'applicaton/javascript'
            self.response.out.write(ADD_FN + '(' + str(entry.points) + ',"' + entry.name + '", "' + nickname + '", "' + str(entry.key()) + '")')


app = webapp2.WSGIApplication([
    ('/log', LogHandler)
], debug=True)
