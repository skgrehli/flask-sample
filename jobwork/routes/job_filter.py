from bson import json_util, ObjectId
import json
from flask import request, Blueprint, make_response, jsonify
from jobwork.db_connection import db
from jobwork.models.user import User
from jobwork.middleware.authentication import authentication

filter=Blueprint('filter', __name__, url_prefix='')

@filter.route('/job/filter', methods=['POST'])
#authentication
def jobFilter():
    try:
        allDataCollections = []
        userid = (request.json['userid'])
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
            origin=True
        else:
            if userid!="":
                userCity=db.user.find_one({"userid":int(userid)},{"_id":0,"addressJSON.city":1})
                cityId=userCity['addressJSON']['city']
                valCity=cityId
                print(cityId)
                cityLocation = db.location.find_one({"cityid": int(cityId)}, {"_id": 0, "gpsJSON": 1})
                cityLat = cityLocation['gpsJSON']['lat']
                cityLng = cityLocation['gpsJSON']["lng"]
                origin=True
            else:
                city = 0
                valCity = {"$ne": city}
                print("no city no user")
                radius=""
                origin=False

        locationList=[]
        print("1")
        if  radius!="" and origin :
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
        #cityList=db.location.find()
        #return jsonify({"status": budgetMin,"lt":budgetMax})
        listd=(jobTypKey,jobTypVal,valLoc,valCity,budgetMin,budgetMax)
        #return jsonify({"back":listd})
        if searchString!="":
            result=db.jobs.find({"description": { "$regex": searchString},jobTypKey:jobTypVal,"locationid":valLoc,"cityid":valCity,"budget":
               {"$gte":budgetMin,"$lte":budgetMax}},{"_id":0}).sort(sortKey,sortVal).skip(page_offset).limit(PageLimit)
        else:
            result = db.jobs.find(
                {jobTypKey: jobTypVal, "locationid": valLoc, "cityid": valCity,
                 "budget":
                     {"$gte": budgetMin, "$lte": budgetMax}}, {"_id": 0}).sort(sortKey, sortVal).skip(
                page_offset).limit(PageLimit)

        count=0
        #return jsonify({"back": list(result)})
        print("3")
        response=dict()
        for data in result:
            #return jsonify({"location": data})
            map=dict()
            if(data['locationid']!=""):
                location_data=db.location.find_one({"locationid":data['locationid']})
            if(data['addressJSON']['state']!=""):
                state=db.state.find_one({"stateid":data['addressJSON']['state']})
            if(data['addressJSON']['country']!=""):
                country = db.country.find_one({"countryid": data['addressJSON']['country']})
            if(data['cityid']!=""):
                city = db.city.find_one({"cityid": data['cityid']})

            map.update({"city":city['city']})
            map.update({"state":state['state']})
            map.update({"country":country['country']})
            map.update({"lon":location_data['location_raw']['lon']})
            map.update({"lat": location_data['location_raw']['lat']})
            map.update({"locationname": location_data['locationname']})
            data.update({"map":map})
            bidcount=db.jobbids.count({"jobid":data['jobid']})
            data.update({"bidcount":bidcount})

            userId =User.find_one({"userid": data['creatinguserid']})
            username = userId['firstname'] + " " + userId['lastname']
            '''
            data.update({"username": username})

            try:
                data.update({"picurl":userId['picurl']})
            except Exception as e:
                data.update({"picurl":"no pic url field in db"})
            '''
            if(radius!=""):
                if(data["locationid"]  in locationList):
                    count = count + 1
                    allDataCollections.append(data)
            else:
                count = count + 1
                allDataCollections.append(data)


        if count is 0:
            return jsonify({"status": 200,"message":"no data","error":True,"response":{}})
        else:
            #return jsonify({"count": count})
            return jsonify({"response":allDataCollections,"status":200,"error":False,"message":count})
    except Exception as e:
        return json.dumps(e, indent=4, default=json_util.default)

@filter.route('/job/pic/update', methods=['POST'])
def updatepic():
    db.jobs.update({},{"$set": {"jobdocs": {"thumbnails": [
        "https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-1/p40x40/11267733_843958002346933_2987868632693693653_n.jpg?_nc_cat=0&oh=313c5268835617d52ab444f9d357c66d&oe=5BF9122F",
        "https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-1/p40x40/11267733_843958002346933_2987868632693693653_n.jpg?_nc_cat=0&oh=313c5268835617d52ab444f9d357c66d&oe=5BF9122F"],
        "doc":["https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-9/11267733_843958002346933_2987868632693693653_n.jpg?_nc_cat=0&oh=8693467a6344c812c57549c05034745b&oe=5C005569",
        "https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-9/11267733_843958002346933_2987868632693693653_n.jpg?_nc_cat=0&oh=8693467a6344c812c57549c05034745b&oe=5C005569"]}}},
        {"upsert": False, "multi": True})
    return jsonify({"done":200})

