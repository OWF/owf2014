#!/usr/bin/env python

import csv, phonenumbers
import re
import string

count = 0


with open("/Users/fermigier/projects/owf2013/data/open-world-forum_inscrits_20130928.csv") as fd:
  reader = csv.reader(fd, delimiter=';')
  for row in reader:
    phone = row[21]
    if phone:
      phone = phone.replace(" ", "")
      phone = phone.replace(".", "")
      phone = phone.replace("-", "")
      phone = phone.replace("(0)", "")
      if phone.startswith("00"):
        phone = "+" + phone[2:]
      if len(phone) > 10 and phone.startswith("33"):
        phone = "+" + phone
      try:
        x = phonenumbers.parse(phone, "FR")
        #print phone, '->', x
        national_number = str(x.national_number)
        if x.country_code == 33 and len(national_number) == 9 and national_number.startswith('6'):
          count += 1
          print "0" + national_number
      except:
        print "Error on", phone


print count