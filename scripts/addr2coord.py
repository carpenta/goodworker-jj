import json
import traceback
from tornado import httpclient, escape
from time import sleep

api_url_template = 'http://apis.daum.net/local/geo/addr2coord?apikey=6b878d3f61024706c8d261d500a59ff43edf28ed&output=json&q=%s'

def get_url(addr):
  return api_url_template%escape.url_escape(addr)

def addr2coord_file(filepath):
  f = open(filepath, 'r')
  if f is not None:
    client = httpclient.HTTPClient()
    for l in f.xreadlines():
      tokens = l.split('\t')
      addr = tokens[1].strip()
      resp = client.fetch(get_url(addr))
      try:
        result = json.loads(resp.body)
        item = result['channel']['item'][0]
        print '%s\t%s\t%s'%(l.strip(), item['lat'], item['lng'])
      except:
        print '%s\t \t '%(l.strip())
        #traceback.print_exc()
        pass
      sleep(1)
    client.close()
  f.close()

def addr2coord(addr):
  client = httpclient.HTTPClient()
  resp = client.fetch(get_url(addr))
  result = None
  try:
    result = json.loads(resp.body)
    item = result['channel']['item'][0]
    result = {'latitude': '%s'%item['lat'], 'longitude': '%s'%item['lng']}
    #print '%s\t%s\t%s'%(addr, item['lat'], item['lng'])
  except:
    #print '%s\t \t '%(addr)
    traceback.print_exc()
  client.close()
  return result
  
if __name__ == '__main__':
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')

  import optparse
  argv = sys.argv
  argc = len(argv)

  parser = optparse.OptionParser()
  parser.add_option('-f', '--file', default=None, help='input file')
  parser.add_option('-a', '--address', default=None, help='input address')

  (options, args) = parser.parse_args(args=argv)

  if options.file is not None:
    addr2coord_file(options.file)
  elif options.address is not None:
    addr2coord(options.address)
  
  print 'complete!'
  
