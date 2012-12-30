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

FRIEND_NICK_PARAM = "f"
USER_ID_PARAM = "u"

class DeleteFriendHandler(webapp2.RequestHandler):       
    def get(self):
        user_id = self.request.get(USER_ID_PARAM)
        parent_key = db.Key.from_path("User", user_id)
        contest = models.Contest().all().ancestor(parent_key).get()           
        friend = users.User(self.request.get(FRIEND_NICK_PARAM))
        if contest and friend in contest.participants:
            contest.participants.remove(friend)
            contest.put()
        
app = webapp2.WSGIApplication([
    ('/deletefriend', DeleteFriendHandler)
], debug=True)
