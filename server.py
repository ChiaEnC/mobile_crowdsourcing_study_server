from flask import Flask, request, jsonify, json, render_template
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_pymongo import PyMongo
import datetime
from datetime import datetime
import dateutil.parser
from bson import json_util
import codecs
import ast
import logging


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mobileCrowdsourceStudy'
app.config['MONGO_URI'] = 'mongodb://localhost/mobileCrowdsourceStudy'
app.config['UPLOAD_FOLDER'] = '/path/to/static/videos'

mongo = PyMongo(app)

Key = ['Accessibility', 'MobileCrowdsource', 'Notification', 'Sensor', "Telephony", 'AppUsage', 'Battery', 'Connectivity', 'Ringer', 'ActivityRecognition', 'Location', 'TransportationMode', 'QuestionnaireAns']
UserKey = ["device_id", "todayMCount", "todayNCount", "allMCount", "allNCount", "total"]
SearchKey = ["id", "DayNumber", "todayMCount", "todayNCount", "totalMCount", "totalNCount", "total", "startDay", "endDay"]


@app.route('/', methods=['POST'])
def test():
    print("test")
    json_request = request.get_json(force=True, silent=True)
    # for j in json_request['Accessibility']:
    #     print("readble : "+str(j['readable']))
    # user_id = json_request['device_id']
    # print("user_id : "+str(user_id))

    # print (str(json_request))
    user = mongo.db.dump
    user.insert(json_request)
    if(str(json_request) != None):
        allTimeStamp = dict()
        # user.insert(json_request)
        # user_id = request.args['id']
        # check all creationTime
        group = dict()
        for key in Key:
            if(key in json_request):
                for targetObject in json_request[key]:
                    data = user.find({'device_id': json_request['device_id']})
                    keyStr = key + ".timestamp"
                    print("keystr : " + keyStr)
                    for item in data.distinct(keyStr):
                        if item == targetObject['timestamp']:
                            if key in allTimeStamp:
                                allTimeStamp[key].append(item)
                            else:
                                allTimeStamp[key] = [item]
                            print("target time stamp : " + str(item))
        allTimeStamp['device_id'] = json_request['device_id']

        # for key in Key:
        #     user.aggregate([
        #      {'$group':{
        #      '_id': { 'readable': $readable, year: { $year: "$date" } },
        #     itemsSold: { $push:  { item: "$item", quantity: "$quantity" } }}}])

        message = json.dumps(allTimeStamp)
        print("message : " + str(message))
        # message = json.dumps({})

        # print("json_request not null" + str(json_request))
        # json_docs = {'error': "false"}
        return message

    else:
        json_docs = {'error': "true"}
        return jsonify(json_doc)


@app.route('/user', methods=['POST', 'GET'], strict_slashes=False)
def user():

    json_request = request.get_json(force=True, silent=True)
    user = mongo.db.user
    if(str(json_request) is None):
        json_docs = {'error': "sync error"}
        return json_docs

    else:
        data = dict()
#        missing_key = False
        for key in UserKey:
            if key in json_request and key != 'device_id':
                data[key] = json_request[key]
            elif key not in json_request:
                #                missing_key = True
                print("something miss")
        print("data" + str(data))
#        if missing_key:
        # file = open('MissingKeyData.txt', 'a')
        # file.write(str(json_request) + '\n')

        user.update({'device_id': json_request['device_id']}, {
                    '$set': data}, upsert=True, multi=True)

        # if(user_data is None):
        #     user.insert(json_request)
        # else:
        #     user.update({ 'device_id': json_request['device_id']},{$set:{'todayMCount': json_request['todayMCount'],'todayNCount':json_request['todayNCount'],'allMCount':json_request['allMCount'],'allNCount':json_request['allNCount'],'total':json_request['total']}}, upsert=True, multi=True)
        return jsonify({'device_id': json_request['device_id']})


@app.route('/search', methods=['GET'], strict_slashes=False)
def index():
    collection = request.args.get('collection')
    field = request.args.get('field')
    user_id = request.args.get('id')
    # default
    user = mongo.db.dump
    print(user_id)
    if collection == 'dump':
        user = mongo.db.dump
    elif collection == 'user':
        user = mongo.db.user
    if(field is None):
        json_docs = []
        data = user.find({'device_id': user_id})
    else:
        json_docs = []
        data = user.find({'device_id': user_id}, {field: 1, '_id': 0})
    for doc in data:
        json_docs.append(doc)
    return '<pre>{}</pre>'.format(json.dumps(json_docs, indent=4, default=json_util.default))


@app.route('/test', methods=['POST', 'GET'], strict_slashes=False)
def hello():
    return "<h1 style='color:blue'>Hello There today is beautiful!</h1>"

# day = 20181127


@app.route('/search_all_detail', methods=['GET'], strict_slashes=False)
def search_hour_of_the_day():
    user_id = request.args.get('id')
    target_hour_of_day = request.args.get('target_hour_of_day', type=int)

    # startDay = day * 10000
    # endDay = (day + 1) * 10000
    # json_array = [[] for i in range(24)]
    json_array = dict()
   # json_array_test = []
    user = mongo.db.dump
    # data = user.find({'device_id': user_id})
    # result = user.find({'device_id':user_id,"Accessibility.readable" :{ '$gte': startHourofDay,'$lte': endHourofDay}},{"Accessibility":1})

    # final = user.find({"Accessibility.readable" :{ '$gte': startHourofDay,'$lte': endHourofDay}},{'device_id':user_id,"Accessibility":{'$elemMatch': {"readable": { '$gte': startHourofDay,'$lte': endHourofDay}}}})

    # final = result.find({'device_id':user_id,"Accessibility.readable" :{ '$gte': startHourofDay,'$lte': endHourofDay}},{"Accessibility":1})
    # items = data.distinct("Accessibility.timestamp")

    # for count, item in enumerate(items, start=0):
    #     if(item>startHourofDay and item<endHourofDay):
    #         print(count, item)

    # final = user.aggregate([{'$unwind': "$Accessibility.readable"}, {'$match': {"Accessibility.readable":{ '$gte': startHourofDay,'$lte': endHourofDay},"device_id": user_id}},
    #     {'$project': {"device_id": 1,
    #     "Accessibility.readable": "$Accessibility.readable","_id":0}}])
    count_array = dict()
    for key in Key:
        target = '$' + str(key)
        readable = str(key) + ".readable"
        # subelement = str(key) + ".$"
        final = user.aggregate([{'$unwind': target}, {'$match': {readable: target_hour_of_day, "device_id": user_id}}, {"$project": {
            key: 1
        }}])
        count = 0
        for doc in final:
            count += 1
            for subkey in doc:
                # print(str(doc[key]))
                if subkey != '_id':
                    if subkey in json_array:
                        json_array[subkey].append(doc[subkey])
                    else:
                        json_array[subkey] = [doc[subkey]]
        #    json_array_test.append(doc)
        # print(str(key))
        strCount = str(key) + 'Count'
        json_array[str(key) + 'Count'] = count
       # json_array_test.append({str(key) + 'Count': count})

    # for key in Key:
    #     target = '$' + str(key)
    #     final = user.aggregate([{'$match': {"device_id": user_id}},
    #                             {'$unwind': target},
    #                             {'$group': {'_id': "$readable", str(key): {'$push': "$$ROOT"}}}
    #                             ])

    # print("data : " + str(json_array))
   # data = json.dumps(json_array, indent=4, default=json_util.default)
    data = json.dumps(json_array)

    return render_template('results.html', user=data)
    # return '<pre>{}</pre>'.format(json.dumps(json_array, indent=4, default=json_util.default))


@app.route('/search_all_count', methods=['GET'], strict_slashes=False)
def search_all_count():
    user_id = request.args.get('id')

    json_array = dict()
   # json_array_test = []
    user = mongo.db.dump

    finalData = dict()
    for key in Key:
        count_target_day = dict()
        count_target_hour = dict()
        target = '$' + str(key)
        readable = str(key) + ".readable"
        # subelement = str(key) + ".$"
        final = user.aggregate([{'$unwind': target}, {'$match': {"device_id": user_id}}, {"$project": {
            key: 1
        }}])
        count = 0
        for doc in final:
            count += 1
            for subkey in doc:
                print("subkey : " + str(subkey))
                if str(subkey) != '_id':
                    for item in doc[subkey]:
                        print("small item : " + str(item))
                        if(item == 'readable'):
                            newDayKey = str(doc[subkey][item] / 100)
                            if newDayKey in count_target_day:
                                count_target_day[newDayKey] += 1
                            else:
                                count_target_day[newDayKey] = 1
                            newHourKey = str(doc[subkey][item])
                            if newHourKey in count_target_hour:
                                count_target_hour[newHourKey] += 1
                            else:
                                count_target_hour[newHourKey] = 1

                            # newDayKey = str(doc[subkey] / 100)
                            # if newDayKey in count_target_day:
                            #     count_target_day[newDayKey] += 1
                            # else:
                            #     count_target_day[newDayKey] = 0
                            # newHourKey = str(doc[subkey])
                            # if newHourKey in count_target_day:
                            #     count_target_hour[newHourKey] += 1
                            # else:
                            #     count_target_hour[newHourKey] = 0

                            #strCount = str(key) + 'Count'
        json_array[str(key) + 'Count'] = count
        count_target_hour['total'] = count
        count_target_day['total'] = count
        # finalData[str(key)] = count_target_day
        fData = merge_two_dicts(count_target_day, count_target_hour)
        finalData[str(key)] = fData
        data = json.dumps(finalData)
    #sdata = json.dumps(count_target_day, indent=4, default=json_util.default)
    # return '<pre>{}</pre>'.format(json.dumps(fData, indent=4, default=json_util.default))
    return render_template('results_count.html', user=data)


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


if __name__ == '__main__':
    app.run(host="172.31.34.26", threaded=True)
