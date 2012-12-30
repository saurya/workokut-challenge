#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import os
import datetime
import models
import common
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp 
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if not current_user:
	    self.redirect(users.create_login_url(self.request.uri))
	    return
	contest = models.Contest.all().filter('user =', current_user).get()
	if not contest:
	    contest = models.Contest(parent=db.Key.from_path("User", current_user.user_id()),user=current_user)
	    contest.put()
        competitors = common.getCompetitors(current_user)
        everyone = [common.getDays(competitor) for competitor in competitors]
        user_entries = common.getDays(current_user)
        today = common.Record()
	today.date = datetime.datetime.now().date()
	if len(user_entries) == 0 or user_entries[0].date != today.date:
	    user_entries.insert(0, today)

        everyone.insert(0, user_entries)
        # Fetch records for others
        # Fetch my record
        template_values = {
                       'users' : everyone,
                       'score' : user_entries.score,
                       'user_id' : current_user.user_id(),
                        }
        path = os.path.join(os.path.dirname(__file__), 'log_workout.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
