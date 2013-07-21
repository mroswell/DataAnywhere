#!/bin/env python
import sys
import math
import datetime
from bson import ObjectId
from flask import Flask,render_template,request,jsonify

sys.path.append('..')
import config

app = Flask(__name__)
app.debug=True

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route('/')
def sanity_test():
    # If no params, send the first 10 records (exploratory)

    results = [x for x in config.medicare_npi_ll_collection.find({}).limit(10)]

    outbound = []
    for r in results:

        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    for r in results:
        outbound.extend(
            [r['_id'],r['year'],r['location'],r['confidence'],r['NPI']]
            )

    if request_wants_json():
        return jsonify(items=outbound)
    return jsonify(items=outbound)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/drg_def_id/<int:drg_def_id>/',defaults={'zipcode':None},methods=['GET'])
@app.route('/drg_def_id/<int:drg_def_id>/zipcode/<string:zipcode>/',methods=['GET'])
def by_dzgeo(drg_def_id,zipcode):
    request_dict = {}

    request_dict['drg_def_id'] = drg_def_id
    if zipcode:
        # USPS zipcode collection
        longlat = config.zipcode_collection.find_one({'postal_code':zipcode})
        request_dict['location'] = {'$near': [longlat['longitude'],longlat['latitude']]}

    results = [x for x in config.medicare_provider_charge_collection.find(request_dict).limit(50000)]

    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    if request_wants_json():
        return jsonify(items=results)

    return jsonify(items=results)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    #app.run(config.query_f_server,config.query_f_port_medicare)
    app.run('192.81.210.33',80)

