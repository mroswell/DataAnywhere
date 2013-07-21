#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import csv
import re
import codecs
import pprint
import pymongo
sys.path.append('..')
import config

'''
fields:

"zip","type","primary_city","acceptable_cities","unacceptable_cities","state","
county","timezone","area_codes","latitude","longitude","world_region","country"
,"decommissioned","estimated_population","notes"
'''

# NOTE: This is destructive!
config.zipcode_collection.drop()

master_ref = {} # for backfilling during parse

with codecs.open('./data/us_zip_to_longlat.csv', "rt", encoding='iso-8859-15') as zi:
    reader = csv.reader(zi, delimiter=',', quotechar='"')
    '''
    We do not use the provided Olson timezones here, they are not close 
    enough to the actual mcity or real local time zone, sadly (why is 
    everyone so sloppy about this? *shakes fists at sky*)
    '''
    try:
      for row in reader:
        newrow = {}
        newrow['postal_code'] = row[0]
        newrow['state'] = row[5]
        newrow['county'] = row[6].encode('iso-8859-15')
        newrow['country'] = row[12]
        newrow['longitude'] = round(float(row[10]),4)
        newrow['latitude'] = round(float(row[9]),4)
        config.zipcode_collection.insert(newrow)

        #pprint.pprint(newrow)
        print ( newrow['postal_code'] )
    except:
      print row
      raise

config.zipcode_collection.create_index([('postal_code',pymongo.ASCENDING)])
