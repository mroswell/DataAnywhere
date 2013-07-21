import os
import pymongo

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Medicare data
medicare_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'db_injection/data'))
connection = pymongo.Connection()
medicare_db = pymongo.database.Database(connection,'medicare')
medicare_npi_ll_collection = medicare_db['medicare_npi_longlat']
medicare_npi_r_collection = medicare_db['medicare_npi_refer']
medicare_provider_charge_collection = medicare_db['medicare_provider_charge']

static_db = pymongo.database.Database(connection,'STATIC_DATA')
zipcode_collection = static_db['zipcode_longlat']
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Flask config
query_f_server='127.0.0.1'
query_f_port_weather=5000
query_f_port_sandy=5001
query_f_port_medicare=5002
