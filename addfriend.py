import os
import cgi
import common
import datetime
import re
import models
import webapp2

from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

FRIEND_NICK_PARAM = "f"
USER_ID_PARAM = "u"
ADD_FN = "addFriend"

class AddFriendHandler(webapp2.RequestHandler):        
    def emailFriend(self, friend):
        mail.send_mail(sender="saurya@gmail.com",
                      to=friend.nickname() + " <" + friend.email() + ">",
                      subject="A friend wants to challenge you to workout!",
                      body="""
                      Hey there!
                      
                      Head on over to http://omarvssaurya.appspot.com and track your workouts!
                      One of your friends, who has already been using it, wants to challenge you.
                      
                      The way it works: you can track your own workouts. Add friends, to see how 
                      they're doing and compete with them!
                      
                      Cheers,
                      The Workout Challenge Team
                      """)

    def get(self):
        user_id = self.request.get(USER_ID_PARAM)
        parent_key = db.Key.from_path("User", user_id)
        contest = models.Contest().all().ancestor(parent_key).get()
        friend = users.User(self.request.get(FRIEND_NICK_PARAM))
        if contest and friend not in contest.participants:
            contest.participants.append(friend)
            contest.put()
        friend_contest = models.Contest().all().filter('user =', friend).get()
        if not friend_contest:
            self.emailFriend(friend)
        else:
            friend = friend_contest.user
            # Render JSONP Response
            path = os.path.join(os.path.dirname(__file__), 'scorecard.html')
            self.response.headers['Content-Type'] = 'applicaton/javascript'
            self.response.out.write(ADD_FN + "('" + common.renderDays(friend, path) + "')")

app = webapp2.WSGIApplication([
    ('/addfriend', AddFriendHandler)
], debug=True)
