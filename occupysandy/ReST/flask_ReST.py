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

    results = [x for x in config.weather_collection.find({}).limit(10)]

    outbound = []
    for r in results:

        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    for r in results:
        outbound.extend(
            [[r['_id'],r['year'],r['location'],r['precips_mm'][n],r['temps_f'][n]] for n in xrange(len(r['precips_mm']))]
            )

    if request_wants_json():
        return jsonify(items=outbound)
    return jsonify(items=outbound)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/year/<int:year>/',defaults={'month':None},methods=['GET'])
@app.route('/year/<int:year>/month/<int:month>/',methods=['GET'])
def by_ym(year,month):
    request_dict = {}
    if year:
        request_dict['year'] = year
    results = [x for x in config.weather_collection.find(request_dict).limit(50000)]

    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    if month in xrange(13):
        outbound = []
        for r in results:
            outbound.append(
                {'_id':r['_id'],'year':r['year'],'location':r['location'],
                 'precip_mm':r['precips_mm'][month],
                 'temp_f':r['temps_f'][month],'temp_c':r['temps_c'][month]}
                )
        results = outbound

    if request_wants_json():
        return jsonify(items=results)

    return jsonify(items=results)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/temp/<string:c_or_f>/<float:temperature_f>/',methods=['GET'])
@app.route('/temp/<string:c_or_f>/<int:temperature_f>/',methods=['GET'])
def by_temp(c_or_f,temperature_f):
    request_dict = {}
    #request['temps_%s' % c_or_f] = {'$gt':math.ceil(temperature_f),'$lte':math.floor(temperature_f)}
    request_dict['temps_%s' % c_or_f] = {'$gt':math.ceil(temperature_f) + 0.5,'$lte':math.floor(temperature_f) - 0.5}

    results = [x for x in config.weather_collection.find(request_dict).limit(10000)]

    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    outbound = []
    for r in results:
        for month in xrange(12):
            if math.floor(temperature_f) - 0.5 < r['temps_f'][month] < math.ceil(temperature_f) + 0.5:
                outbound.append(
                    {'_id':r['_id'],'year':r['year'],'location':r['location'],
                     'precip_mm month %d' % month:r['precips_mm'][month],
                     'temp_f month %d' % month:r['temps_f'][month],'temp_c month %d' % month:r['temps_c'][month]
                        }
                    )
    results = outbound

    if request_wants_json():
        return jsonify(items=results)

    return jsonify(items=results)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/temp/<string:c_or_f>/-<float:temperature_f>/',methods=['GET'])
@app.route('/temp/<string:c_or_f>/-<int:temperature_f>/',methods=['GET'])
def by_neg_temp(c_or_f,temperature_f):
    temperature_f = -temperature_f
    return by_temp(c_or_f,temperature_f)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    app.run(config.query_f_server,config.query_f_port)

