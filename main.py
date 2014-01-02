#!/usr/bin/env python
# -*- coding: utf8 -*-

import webapp2
import jinja2
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from json_util import *
from rest import *
from model import *
from blobstore import *
import urllib
from google.appengine.api import urlfetch

api_url_template = 'http://apis.daum.net/local/geo/addr2coord?apikey=6b878d3f61024706c8d261d500a59ff43edf28ed&output=json&q=%s'

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

options = {
	'title': u'제주 충신교회 지도',
}

class MainHandler(webapp2.RequestHandler):
	def get(self):
		main = JINJA_ENVIRONMENT.get_template('views/main.html')
		options['data'] = to_json(People.query().fetch())
		self.response.write(main.render(options))

class SampleHandler(RestHandler):
	model = SampleModel

class PeopleHandler(RestHandler):
	model = People

class AdminHandler(webapp2.RequestHandler):
	def get(self):
		admin = JINJA_ENVIRONMENT.get_template('views/admin.html')
		self.response.write(admin.render(options))

class TestHandler(webapp2.RequestHandler):
	def get(self):
		test = JINJA_ENVIRONMENT.get_template('views/test.html')
		self.response.write(test.render(options))

app = webapp2.WSGIApplication([
	(r'/', MainHandler),
	(r'/sample', SampleHandler),
	(r'/sample/(\d+)', SampleHandler),
	(r'/people', PeopleHandler),
	(r'/people/(\d+)', PeopleHandler),
	(r'/upload', UploadHandler),
	(r'/admin', AdminHandler),
	(r'/test', TestHandler),
	('/serve/([^/]+)?', ServeHandler)
], debug=True)
