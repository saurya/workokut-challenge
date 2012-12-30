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

REPS_CGI_PARAM = "r"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        entry = models.Entry
        # entry.time = get the current time
        entry.reps = self.request.get(REPS_CGI_PARAM)
        entry.user = users.get_current_user()
        entry.points = exercise.points_per_unit * entry.reps
        
        if entry.user:
            # Render JSONP Response
            self.response.headers['Content-Type'] = 'applicaton/javascript'
            self.response.out.write(ADD_FN + '(' + entry.points + ',' + entry.exercise.name)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
