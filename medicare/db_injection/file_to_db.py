#!/bin/env python
import sys
import os
import codecs
import re
import csv
import pymongo
sys.path.append('..')
import config

class MedicareData(object):
    def inject_medicare_one(self):
        with codecs.open(config.medicare_data_dir + '/' + 'geocoded_npi.csv','r','utf-8') as tfile: # In case of multilingual text.
           reader = csv.reader(tfile, delimiter=',', quotechar='|')
           for row in reader:
                # NPI,lat,lng,confidence
                npi = int(row[0])
                latitude = row[1]
                longitude = row[2]
                confidence = row[3]

                config.medicare_npi_ll_collection.insert(
                    {
                        'year':2011,
                        'NPI': npi,
                        'location':[round(float(longitude),10),round(float(latitude),10)],
                        'confidence': round(float(confidence),5)
                    },
                    safe=True)

        config.medicare_npi_ll_collection.create_index([("year", pymongo.ASCENDING)])
        config.medicare_npi_ll_collection.create_index([("location", pymongo.GEO2D)])
        config.medicare_npi_ll_collection.create_index([("NPI", pymongo.ASCENDING)])
        config.medicare_npi_ll_collection.create_index([("confidence", pymongo.ASCENDING)])

    def inject_medicare_two(self):
        with codecs.open(config.medicare_data_dir + '/' + 'Medicare_Provider_Charge_Inpatient_DRG100_FY2011.csv','r','utf-8') as tfile: # In case of multilingual text.
           reader = csv.reader(tfile, delimiter=',', quotechar='"')
           for row in reader:
                # DRG Definition,Provider Id,Provider Name,Provider Street Address,Provider City,Provider State,Provider Zip Code,Hospital Referral Region Description, Total Discharges , Average Covered Charges , Average Total Payments
                drg_def = row[0]
                drg_def_id = int(row[0].split('-')[0])
                drg_def_string = row[0].split('-')[1].strip()
                provider_id = int(row[1])
                provider_name = row[2]
                provider_addr = row[3]
                provider_city = row[4]
                provider_state = row[5]
                provider_zip = row[6]
                hosp_referral_region_desc = row[7]
                total_discharges = int(row[8])
                avg_covered_charges = round(float(row[9]),8)
                avg_total_payments = round(float(row[10]),8)

                config.medicare_provider_charge_collection.insert(
                    {
                        'year':2011,
                        'drg_def_id':drg_def_id,
                        'drg_def_string':drg_def_string,
                        'provider_id':provider_id,
                        'provider_name':provider_name,
                        'provider_addr':provider_addr,
                        'provider_city':provider_city,
                        'provider_state':provider_state,
                        'provider_zip':provider_zip,
                        'hosp_referral_region_desc':hosp_referral_region_desc,
                        'total_discharges':total_discharges,
                        'avg_covered_charges':avg_covered_charges,
                        'avg_total_payments':avg_total_payments
                    },
                    safe=True)

        config.medicare_provider_charge_collection.create_index([("year", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.create_index([("drg_def_id", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.create_index([("provider_id", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.create_index([("provider_state", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.create_index([("provider_zip", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.create_index([("drg_def_string", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.create_index([("total_discharges", pymongo.ASCENDING)])

    def inject_medicare_three(self):
        with codecs.open(config.medicare_data_dir + '/' + 'refer2011.csv','r','utf-8') as tfile: # In case of multilingual text.
           reader = csv.reader(tfile, delimiter=',', quotechar='"')
           for row in reader:
                # Referrer_NPI,Referred_To_NPI,Refer_count
                referrer_NPI = int(row[0])
                referred_to_NPI = int(row[1])
                refer_count = int(row[2])

                config.medicare_npi_r_collection.insert(
                    {
                        'year':2011,
                        'referrer_NPI':referrer_NPI,
                        'referred_to_NPI':referred_to_NPI,
                        'refer_count':refer_count
                    },
                    safe=True)

        config.medicare_npi_r_collection.create_index([("year", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.create_index([("referrer_NPI", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.create_index([("referred_to_NPI", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.create_index([("refer_count", pymongo.ASCENDING)])

    def just_index(self):
        config.medicare_npi_ll_collection.ensure_index([("year", pymongo.ASCENDING)])
        config.medicare_npi_ll_collection.ensure_index([("location", pymongo.GEO2D)])
        config.medicare_npi_ll_collection.ensure_index([("NPI", pymongo.ASCENDING)])
        config.medicare_npi_ll_collection.ensure_index([("confidence", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("year", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("drg_def_id", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("provider_id", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("provider_state", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("provider_zip", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("drg_def_string", pymongo.ASCENDING)])
        config.medicare_provider_charge_collection.ensure_index([("total_discharges", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.ensure_collection([("year", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.ensure_collection([("referrer_NPI", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.ensure_collection([("referred_to_NPI", pymongo.ASCENDING)])
        config.medicare_npi_r_collection.ensure_collection([("refer_count", pymongo.ASCENDING)])
        print "indexing..."
        print "done"

if __name__ == "__main__":
   w = MedicareData()
   #w.inject_medicare_one()
   #w.inject_medicare_two()
   w.inject_medicare_three()
   w.just_index()
