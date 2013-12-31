#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, os
import webapp2
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from json_util import *

DEFAULT_FETCH_SIZE = 10

class RestHandler(webapp2.RequestHandler):
	model = ndb.Model

	@staticmethod
	def qo(page, limit):
		return ndb.QueryOptions(offset=page*limit, limit=limit)

	def get(self, ndbid=None):
		self.response.content_type = 'application/json'
		if ndbid is None:
			limit = self.request.get('limit', DEFAULT_FETCH_SIZE)
			page = int(self.request.get('page', 0))
			#models = self.model.query().fetch(options=self.qo(page, limit))
			models = self.model.query().fetch()
			self.response.write(to_json(models))
		else:
			model = self.model.get_by_id(int(ndbid))
			self.response.write(to_json(model))
	def post(self, ndbid=None):
		params = from_json(self.request.body)
		instance = self.model()
		for prop in instance._properties:
			if prop in params:
				setattr(instance, prop, params[prop])
		instance.put()
		self.response.content_type = 'application/json'
		self.response.write(to_json({'success':True}))
	def delete(self, ndbid=None):
		result = False
		if ndbid is not None:
			instance = self.model.get_by_id(int(ndbid))
			instance.key.delete()
			result = True
		self.response.content_type = 'application/json'
		self.response.write(to_json({'success':result}))
	def put(self, ndbid=None):
		result = False
		if ndbid is not None:
			params = from_json(self.request.body)
			instance = self.model.get_by_id(int(ndbid))
			for prop in instance._properties:
				if prop in params:
					setattr(instance, prop, params[prop])
			instance.put()
			result = True
		self.response.content_type = 'application/json'
		self.response.write(to_json({'success':result}))
