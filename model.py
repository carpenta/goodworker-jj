#!/usr/bin/env python
# -*- coding: utf8 -*-

from google.appengine.ext import ndb

class BaseModel(ndb.Model):
	created = ndb.DateTimeProperty(auto_now_add=True)
	def json(self, data, *args, **kwargs):
		return json.dumps(data, cls=DatastoreEncoder, *args, **kwargs)

class SampleModel(BaseModel):
	name=ndb.StringProperty()
	content=ndb.StringProperty()


class People(BaseModel):
	name=ndb.StringProperty()
	address=ndb.StringProperty()
	longitude=ndb.StringProperty()
	latitude=ndb.StringProperty()
	group=ndb.StringProperty()

