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

ENTRY_ID_PARAM = "e"
USER_ID_PARAM = "u"

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get(USER_ID_PARAM)
        key = self.request.get(ENTRY_ID_PARAM)
        entry = models.Entry(key=key)
        db.delete(entry)
        

app = webapp2.WSGIApplication([
    ('/delete', DeleteHandler)
], debug=True)
