from bson import json_util, ObjectId
import json
from flask import request, Blueprint, make_response, jsonify
from jobwork.db_connection import db
from jobwork.middleware.authentication import authentication

filter=Blueprint('filter', __name__, url_prefix='')

@filter.route('/job/filter', methods=['POST'])
#authentication
def jobFilter():
    try:
        allDataCollections = []
        userid = int(request.json['userid'])
        sortBy = int(request.json['sortBy'])
        budgetMin = int(request.json['budgetMin'])
        budgetMax = int(request.json['budgetMax'])
        city = request.json['city']
        location = request.json['location']
        jobtype = request.json['jobtype']
        radius=request.json['radius']
        page_offset = request.json['page_offset']
        searchString=request.json['search']

        PageLimit = 10



        if (jobtype == 0):
            jobTypKey = "$or"
            jobTypVal = [{"online":True},{"online":False}]
        if (jobtype == 1):
            jobTypKey = "online"
            jobTypVal = True
        if (jobtype == 2):
            jobTypKey = "online"
            jobTypVal = False

        if location != "":
            location=int(request.json['location'])
            valLoc=location
        else:
            location=0
            valLoc={"$ne":location}

        if city != "":
            city=int(request.json['city'])
            valCity=city
            cityLocation = db.location.find_one({"cityid": int(city)}, {"_id": 0,"gpsJSON":1})
            cityLat=cityLocation['gpsJSON']['lat']
            cityLng=cityLocation['gpsJSON']["lng"]
            print(cityLat,cityLng)
        else:
            cityCity=0
            valCity={"$ne":city}
            userCity=db.user.find_one({"userid":userid},{"_id":0,"addressJSON.city":1})
            cityId=userCity['addressJSON']['city']
            print(cityId)
            cityLocation = db.location.find_one({"cityid": int(cityId)}, {"_id": 0, "gpsJSON": 1})
            cityLat = cityLocation['gpsJSON']['lat']
            cityLng = cityLocation['gpsJSON']["lng"]

        locationList=[]
        print("1")
        if  radius!="" :
            #locations=list(db.location.find({ "gpsJSON" : { "$near" : [cityLat,cityLng],"$maxDistance":int(request.json['radius'] ) } },{"locationid":1,"_id":0} ))
            locations=list(db.location.find({ "gpsJSON.lnglat" : { "$near" :{ "$geometry" : { "type" : "Point" , "coordinates" : [ cityLng , cityLat ] },"$maxDistance" : int(radius) * 1000 }}}))
            print("2")
            for data in locations:
                locationList.append(data["locationid"])
        #return jsonify({"status": "ok"})

        if(sortBy==0):
            sortKey="publisheddatetime"
            sortVal=-1
        if (sortBy == 1):
            sortKey = "budget"
            sortVal = 1
        if (sortBy == 2):
            sortKey = "budget"
            sortVal = -1
        if (sortBy == 3):
            sortKey = "distance"
            sortVal = -1
        # db.location.find({ gpsJSON : { $near : [43.8492143,-79.0241784],$maxDistance:1  } } )
        cityList=db.location.find()
        #return jsonify({"status": budgetMin,"lt":budgetMax})
        result=db.jobs.find({"description": { "$regex": searchString},jobTypKey:jobTypVal,"locationid":valLoc,"cityid":valCity,"budget":
               {"$gte":budgetMin,"$lte":budgetMax}},{"_id":0}).sort(sortKey,sortVal).skip(page_offset).limit(PageLimit)
        count=0
        print("3")
        response=dict()
        for data in result:
            #return jsonify({"location": data["locationid"],"list":locationList[0]["locationid"]})
            if(radius!=""):
                if(data["locationid"]  in locationList):
                    print(data)
                    count=count+1
                    allDataCollections.append(data)
            else:
                count = count + 1
                allDataCollections.append(data)

        if count is 0:
            return jsonify({"status": 200,"message":"no data","error":True,"response":{}})
        else:
            #return jsonify({"count": count})
            return jsonify({"response":allDataCollections,"status":200,"error":False,"message":""})
    except Exception as e:
        return json.dumps(e, indent=4, default=json_util.default)
