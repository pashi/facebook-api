#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import requests
import sys
import string
#import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1


REQUEST_TYPE_FEED = 1
REQUEST_TYPE_EVENTS = 2

def get_request(config, request_type):
  url = None
  if request_type == REQUEST_TYPE_FEED:
    url = """%(base_url)s/%(group_id)s/feed?access_token=%(token)s""" % (config)
  elif request_type == REQUEST_TYPE_EVENTS:
    url = """%(base_url)s/%(group_id)s/events?access_token=%(token)s""" % (config)
  else:
    return []
  try:
    r = requests.get( url )
    if r.status_code == 400:
      # no permissions
      return []
    if not r.status_code == 200:
      return []
    data = json.loads(r.text)
    if data.has_key('data'):
      return data['data']
    else:
      return []
  except:
    print "error"
    sys.exit(1)
   
  
def load_config(filename):
  f = open(filename)
  config = json.loads(f.read())
  f.close()
  return config




def generate_html_feed(config, data):

  result = []
  html_line = config['feed_line']
  for line in data:
    if line.has_key('message'):
      line['message'] = line['message'].encode('ascii', 'xmlcharrefreplace')
      result_line = html_line % line
      result.append(result_line)
  if len(result) > 0:
    f = open (config['output_feed_file'], 'w')
    f.write(string.join(result,''))
    f.close()


def generate_html_event(config, data):

  result = []
  html_line = config['event_line']
  for line in data:
    if line.has_key('name'):
      line['name'] = line['name'].encode('ascii', 'xmlcharrefreplace')
      result_line = html_line % line
      result.append(result_line)
  if len(result) > 0:
    f = open (config['output_event_file'], 'w')
    f.write(string.join(result,''))
    f.close()


def main():
  
  config = load_config(sys.argv[1])

  feeds = get_request (config, REQUEST_TYPE_FEED)
  if config.has_key('output_feed_json'):
    f = open(config['output_feed_json'], 'w')
    f.write(json.dumps(feeds))
    f.close()
  generate_html_feed(config, feeds)

  events = get_request (config, REQUEST_TYPE_EVENTS)
  if config.has_key('output_event_json'):
    f = open(config['output_event_json'], 'w')
    f.write(json.dumps(feeds))
    f.close()
  generate_html_event(config, events)
  sys.exit(0)

if __name__ == "__main__":
  main()

