#!/bin/env python
import sys
import os
import codecs
import re
import csv
import pymongo
sys.path.append('..')
import config

class GeocodeZips(object):
    def geocode_zip(self):
        for r in config.medicare_provider_charge_collection.find({}):

            if len(r['provider_zip']) < 5:
               r['provider_zip'] = str("%05d" % int(r['provider_zip']))

            z = config.zipcode_collection.find_one({'postal_code':r['provider_zip']})
            try:
                config.medicare_provider_charge_collection.update(
                    {
                        '_id':r['_id']
                    },
                    {
                        '$set':{ 
                            'location':[round(float(z['longitude']),10),round(float(z['latitude']),10)]
                        }
                    },upsert=False,safe=True)
            except:
                print r
                print z
                raise

        config.medicare_provider_charge_collection.create_index([("location", pymongo.GEO2D)])

if __name__ == "__main__":
   GeocodeZips().geocode_zip()
