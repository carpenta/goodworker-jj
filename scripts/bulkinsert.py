#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
import urllib
import httplib
import traceback
import datetime
import json

class InitTool:
  def __init__(self, filepath, host='goodworker-jj.appspot.com'):
    self.filepath = filepath
    self.host = host
    self.conn = httplib.HTTPConnection(self.host)
    self.template = '{"name":"%s", "address":"%s", "group":"%s", "latitude":"%s", "longitude":"%s"}'

  def close(self):
    try:
      self.conn.close()
    except:
      traceback.print_exc()

  def req(self, url='/', method='GET', data='', headers={}):
    result = None
    try:
      self.conn.request(method, url, data, headers)
      response = self.conn.getresponse()
      result = response.read()
    except:
      traceback.print_exc()
    return result

  def insert(self):
    success_cnt = 0
    f = open(self.filepath, 'r')
    for l in f.xreadlines():
      tokens = l.split('\t')
      name = tokens[0]
      addr = ''
      group = ''
      lat = ''
      lng = ''

      if len(tokens) > 1:
        addr = tokens[1].strip()
      if len(tokens) > 2:
        group = tokens[2].strip()
      if len(tokens) > 4:
        lat = tokens[3].strip()
        lng = tokens[4].strip()

      body = self.template % (name, addr, group, lat, lng)
      print body
      response = self.req('/people', 'POST', body)
      try:
        print response
        result = json.loads(response)
        if result['success']:
          success_cnt +=1 
      except:
        print tokens
        traceback.print_exc()
    f.close()
    return success_cnt


if __name__ == '__main__':
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')

  import optparse
  argv = sys.argv
  argc = len(argv)

  parser = optparse.OptionParser()
  parser.add_option('-f', '--file', default=None, help='input file')
  parser.add_option('-t', '--host', default='goodworker-jj.appspot.com', help='input host path')
  (options, args) = parser.parse_args(args=argv)

  if options.file is not None:
    it = InitTool(options.file, options.host)
    it.insert()
    it.close()
  
  print 'complete!'
