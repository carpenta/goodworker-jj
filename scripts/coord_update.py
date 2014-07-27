#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import traceback
from tornado import httpclient, escape
from time import sleep
import httplib
from addr2coord import *

def get_people(host):
  client = httpclient.HTTPClient()
  url = 'http://%s/people'%(host)
  resp = client.fetch(url)
  client.close()
  return json.loads(resp.body)

def get_person(id, host):
  client = httpclient.HTTPClient()
  url = 'http://%s/people/%s'%(host, id)
  resp = client.fetch(url)
  client.close()
  return json.loads(resp.body)

def process(filename):
  pass

def update(id, host):
  uri = '/people/%s'%(id)
  p = get_person(id, host)
  coord = addr2coord(p['address'])
  if coord:
    conn = httplib.HTTPConnection(host)
    conn.request('PUT', uri, json.dumps(coord), {})
    response = conn.getresponse()
    result = response.read()
    conn.close()
    print result
    


if __name__ == '__main__':
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')

  import optparse
  argv = sys.argv
  argc = len(argv)

  parser = optparse.OptionParser()
  parser.add_option('-t', '--host', default='goodworker-jj.appspot.com', help='host')
  parser.add_option('-f', '--file', default=None, help='input file')
  parser.add_option('-i', '--id', default=None, help='input person id')
  parser.add_option('-a', '--auto', default=None, help='auto find')

  (options, args) = parser.parse_args(args=argv)

  if options.file is not None:
    process(options.file)
  elif options.id:
    update(options.id, options.host)
  elif options.auto:
    persons = get_people(options.host)
    need_update_people = []
    for p in persons:
      if 'latitude' in p and p['latitude'] == "":
        need_update_people.append(p)
    for n in need_update_people:
      update(n['__id__'], options.host)
  print 'complete!'
