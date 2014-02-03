#!/usr/bin/env python

import requests
from pprint import pprint

EMAIL = "m.ali-ziane@systematic-paris-region.org"
PASSWORD = "OWF!2013"
APIKEY = "cc89c5629dfdc3086f73ffc193ef85fc"
ID_EVENT = "42230"

res = requests.get("https://api.weezevent.com/auth/access_token/",
                   params={'username': EMAIL,
                           'password': PASSWORD,
                           'api_key': APIKEY})
access_token = res.json()['accessToken']
print access_token

res = requests.get("https://api.weezevent.com/participants",
                   params={'api_key': APIKEY,
                           'access_token': access_token,
                           'id_event[]': ID_EVENT,
                           'full': 1})
participants = res.json()['participants']
for p in participants:
  pprint(p)
  print 78 * '-'
