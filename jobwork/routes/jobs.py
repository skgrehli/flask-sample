from flask import request, Blueprint, jsonify,render_template
from jobwork.constants import Constants
from jobwork.models.city import CityCollections
from jobwork.models.jobbids import JobBids
from jobwork.models.jobs import Jobs
from jobwork.models.locations import Locations
from jobwork.models.user import User
from jobwork.utils.common_utils import CommonUtils
from jobwork.middleware.authentication import authentication
from datetime import datetime,timedelta
from jobwork.models.state import StateCollections
from jobwork.models.country import CountryCollections

jobs_route = Blueprint('jobs_route', __name__, url_prefix='')


@jobs_route.route('/findjobs')
def findjobs():
	city = list(CityCollections.find({},{"_id":0,"cityid":1,"city":1}).sort('city',1))
	locationData = list(Locations.find({},{"_id":0}).sort('locationname',1))
	return render_template("front_saveonjobs/findjobs.html",cities=city,location=locationData)

# noinspection PyPep8Naming,SpellCheckingInspection
@jobs_route.route('/job/details',methods=['POST'])
def jobDetails():
    jobid=request.json['jobid']
    job=list(Jobs.find_one({"jobid":jobid},{"_id":0}))
    if job is not None:
        return jsonify({"detail":job})
    else:
        return jsonify({"message":"no job found with this id"})

@jobs_route.route('/jobset', methods=['POST'])
def jobset():
	resultd = Jobs.find({})

	if resultd is not None:
		for result in resultd:
			currentdata = datetime.now()
			if result['duedate'] < currentdata:
				jobUpdate = Jobs.update({"jobid":result['jobid'], "draft":False},{"$set":{"expired":True}})




	return 'success'


@jobs_route.route('/job/all/list', methods=['POST'])
def job_all_list():
    try:
        allDataCollections = []

        sortDataAccording = request.json['sortDataAccording']
        city = request.json.get('city', "")
        location = request.json.get('location', "")
        radius = request.json.get('radius', "")
        jobType = request.json.get('jobType', "")
        budgetMin = request.json.get('budgetMin', "")
        budgetMax = request.json.get('budgetMax', '')
        searchstring = request.json.get('searchstring', '')
        page_offset = request.json.get('page_offset', 0)
        result = []
        lat = 0
        lng = 0
        job_location = []
        filterstring = {"active": True, "draft": False, "jobstatus": {"$in": ["pending", "reversebid"]}}
        sort_filter = []
        distance_filter_string = {"active": True, "draft": False, "jobstatus": {"$in": ["pending", "reversebid"]}}
        distance_job = []

        startCity = "252347228"

        if len(searchstring) != 0:
            stringData = '.*' + searchstring + '.*'

            getall = []  # for OR
            conditionOR = {
                '$options': 'i',
                '$regex': stringData
            }  # regex condition
            serchdatainarray = {
                'title': conditionOR
            }  # for title
            singleget = {
                "description": conditionOR
            }  # for description
            getall.append(serchdatainarray)
            getall.append(singleget)
            filterstring['$or'] = getall

        filterstring['expired'] = False
        distance_filter_string['expired'] = False
        mapCoordinate = {}
        cityResult = CityCollections.find_one({"cityid": int(startCity)}, {"_id": 0})
        if cityResult is not None:
            lat = cityResult['gpsJSON']['lat']
            lng = cityResult['gpsJSON']['lng']
            mapCoordinate = {"lat": lat, "lng": lng}

        if radius != "":
            if location != "":
                location_result = Locations.find_one({"locationid": int(location)}, {"_id": 0})
                if location_result is not None:
                    lat = location_result['gpsJSON']['lat']
                    lng = location_result['gpsJSON']['lng']
                    mapCoordinate = {"lat": lat, "lng": lng}
                    print(mapCoordinate)
                location_gps_result = Locations.find({"gpsJSON.lnglat": {
                    "$near": {"$geometry": {"type": "Point", "coordinates": [lng, lat]},
                              "$maxDistance": int(radius) * 1000}}})
                if location_gps_result is not None:
                    for location_gps in location_gps_result:
                        job_location.append(int(location_gps['locationid']))

            elif city != "":
                city_result = CityCollections.find_one({"cityid": int(city)}, {"_id": 0})
                if city_result is not None:
                    lat = city_result['gpsJSON']['lat']
                    lng = city_result['gpsJSON']['lng']
                    mapCoordinate = {"lat": lat, "lng": lng}
                    print(mapCoordinate)
                city_gps_result = Locations.find({"gpsJSON.lnglat": {
                    "$near": {"$geometry": {"type": "Point", "coordinates": [lng, lat]},
                              "$maxDistance": int(radius) * 1000}}})
                if city_gps_result is not None:
                    for city_gps in city_gps_result:
                        job_location.append(int(city_gps['locationid']))
            elif mapCoordinate:
                city_gps_result = Locations.find({"gpsJSON.lnglat": {
                    "$near": {"$geometry": {"type": "Point",
                                            "coordinates": [mapCoordinate.get("lng"), mapCoordinate.get("lat")]},
                              "$maxDistance": int(radius) * 1000}}})
                if city_gps_result is not None:
                    for city_gps in city_gps_result:
                        job_location.append(int(city_gps['locationid']))
            print(job_location)

        if jobType != "allJobs":
            filterstring.update({"online": jobType})
            distance_filter_string.update({"online": jobType})

        if budgetMin or budgetMax:
            budget_filter = {"budget": {}}
            if budgetMin:
                budget_filter['budget']['$gte'] = int(budgetMin)
            if budgetMax:
                budget_filter['budget']['$lte'] = int(budgetMax)
            filterstring.update(budget_filter)
            distance_filter_string.update(budget_filter)

        if job_location:
            if city:
                filterstring.update({"cityid": int(city), "locationid": {"$in": job_location}})
            else:
                filterstring.update({"cityid": int(startCity), "locationid": {"$in": job_location}})
        else:
            if location:
                filterstring.update({"locationid": int(location)})
            if city:
                filterstring.update({"cityid": int(city)})
            else:
                filterstring.update({"cityid": int(startCity)})

        print(type(location))
        print(filterstring)

        if sortDataAccording == "" or sortDataAccording == "recent":
            sort_filter.append(("publisheddatetime", -1))
        elif sortDataAccording == "price_asc":
            sort_filter.append(("budget", 1))
        elif sortDataAccording == "distance":
            dist_centre = location if location else city if city else "252347228"
            dist_city_result = Locations.find_one({"locationid": int(dist_centre)}, {"_id": 0})
            if dist_city_result:
                dist_lat = dist_city_result['gpsJSON']['lat']
                dist_lng = dist_city_result['gpsJSON']['lng']
                mapCoordinate = {"lat": dist_lat, "lng": dist_lng}
                print(mapCoordinate)
                radius = radius if radius else 50000
                distance_gps_result = Locations.aggregate([{"$geoNear": {
                    "near": {"type": "Point", "coordinates": [dist_lng, dist_lat]}, "maxDistance": radius * 1000,
                    "spherical": True, "distanceField": "distance"}}])
                if distance_gps_result is not None:
                    for distance_job_location in distance_gps_result:
                        distance_job.append({"locationid": distance_job_location['locationid'],
                                             "distance": distance_job_location['distance']})
            distance_job = sorted(distance_job, key=lambda k: k['distance'])

            if city:
                distance_filter_string.update({"cityid": int(city), "locationid": int(dist_centre)})
                distance_result = Jobs.find(distance_filter_string, {"_id": 0}).skip(page_offset).limit(
                    Constants.PAGE_LIMIT)
                if distance_result:
                    for distance in distance_result:
                        result.append(distance)
            else:
                for distance in distance_job:
                    distance_filter_string.update({"cityid": int(dist_centre), "locationid": distance['locationid']})
                    print(distance_filter_string)
                    distance_result = Jobs.find(distance_filter_string, {"_id": 0}).skip(page_offset).limit(
                        Constants.PAGE_LIMIT)
                    if distance_result:
                        for dist in distance_result:
                            result.append(dist)

        else:
            sort_filter.append(("budget", -1))

        if sortDataAccording != "distance":
            result = Jobs.find(filterstring, {"_id": 0}).sort(sort_filter).skip(page_offset).limit(Constants.PAGE_LIMIT)
            print(result.count())

        if result:
            for resultData in result:
                # Job bidding Detail
                jobBids = list(JobBids.find({"jobid": resultData['jobid']}, {"_id": 0}))
                if resultData.get('creatinguserid', None):
                    if resultData['creatinguserid']:
                        userData = User.find_one({"userid": int(resultData['creatinguserid'])}, {"_id": 0})
                        if userData:
                            fullname = userData['firstname'] + " " + userData['lastname']
                            if resultData['cityid']:
                                cityName = CityCollections.find_one({"cityid": resultData['cityid']},
                                                                    {"_id": 0, "city": 1})
                                cityName = cityName['city']
                            else:
                                cityName = ""
                            if userData.get('picurl', ""):
                                picurl = Constants.PROFIL_PIC_STATIC_PATH + userData['picurl']
                            else:
                                picurl = Constants.PROFIL_PIC_STATIC_PATH + "user-no-image.jpg"

                            location_name = ""
                            if resultData['cityid'] and resultData['locationid']:
                                jobMapResult = Locations.find_one({"locationid": int(resultData['locationid'])},
                                                                  {"_id": 0})
                                location_name = jobMapResult['locationname'] + " - " + jobMapResult['under']

                            else:
                                if not resultData['cityid']:
                                    jobMapCity = 252347228
                                else:
                                    jobMapCity = int(resultData['cityid'])
                                jobMapResult = CityCollections.find_one({"cityid": jobMapCity}, {"_id": 0})

                            jobMapCoordinate = {}
                            if jobMapResult is not None:
                                lat = jobMapResult['gpsJSON']['lat']
                                lng = jobMapResult['gpsJSON']['lng']
                                jobMapCoordinate = {"lat": lat, "lng": lng}

                            MapResult = CityCollections.find_one({"cityid": int(resultData['cityid'])}, {"_id": 0})
                            if MapResult is not None:
                                city_lat = MapResult['gpsJSON']['lat']
                                city_lng = MapResult['gpsJSON']['lng']
                                mapCoordinate = {"lat": city_lat, "lng": city_lng}

                            userDataCollection = {"fullname": fullname, "cityname": cityName,
                                                  "locationname": location_name, "picurl": picurl,
                                                  "totalJobBids": len(jobBids), "jobMapCoordinate": jobMapCoordinate,
                                                  "mapCoordinate": mapCoordinate}
                            resultData.update(userDataCollection)
                            allDataCollections.append(resultData)

            return jsonify({"status": 200, "message": "Job List.", "allTask": allDataCollections,
                            "countData": len(allDataCollections)})
        else:
            return jsonify(
                {"status": 200, "message": "No data.", "allTask": result, "countData": len(allDataCollections)})
    except Exception as e:
        CommonUtils.print_exception()
        return jsonify({"status": 500, "message": str(e)})


@jobs_route.route('/job/add', methods=['POST'])
@authentication
def createJob():
    try:
        userid = int(request.json['userid'])
        token = request.json['token']
        userInfo = User.find_one({"userid": int(userid)}, {"_id": 0})
        if userInfo is not None:
            if userInfo['emailverified'] is False:
                return jsonify(
                    {"status": 202, "message": "Email not verified. Please verify your email to enable this feature"})

        jobid = request.json['jobid']

        originaljobid = None
        if (jobid != ""):
            originaljobid = jobid

        draft = request.json['draft']

        title = request.json['title']
        description = request.json['description']

        duedate = request.json['duedate']
        jobOnline = request.json['jobOnline']
        city = int(request.json['city'])
        location = int(request.json['location'])
        if duedate == "today":
            duedate = ""
            duedate = datetime.now()
        if duedate == "week":
            duedate = ""
            duedate = datetime.now() + timedelta(days=7)
        if duedate == "certain_day":
            duedate = ""
            format = '%d-%m-%Y %H:%M:%S'
            certaindatetime = request.json['certaindatetime']
            duedate = datetime.strptime(certaindatetime, format)

        citydetail = CityCollections.find_one({"cityid": city}, {"_id": 0})
        statedetail = StateCollections.find_one({"stateid": citydetail['stateid']}, {"_id": 0})
        countrydetail = CountryCollections.find_one({"countryid": citydetail['countryid']}, {"_id": 0})
        addressJSON = {"address1": "",
                       "address2": "",
                       "city": city,
                       "state": citydetail['stateid'],
                       "country": countrydetail['countryid'],
                       "pincode": ""
                       }

        person = request.json['person']
        budgettype = request.json['budgettype']
        budget = float(request.json['budget'])
        if budgettype == "hourly":
            totalhours = int(request.json['hours'])
            totalbudget = int(budget * totalhours)
        else:
            totalhours = -1
            totalbudget = budget

        if draft == False:
            publisheddatetime = datetime.now()
        else:
            publisheddatetime = None

        if (request.json['draft_data'] == False):
            jobid = CommonUtils.generateRandomNo(Jobs, "jobid")
            result = Jobs.insert({"jobid": jobid,
                                  "title": title,
                                  "description": description,
                                  "creatinguserid": userid,
                                  "duedate": duedate,
                                  "budget": budget,
                                  "budgettype": budgettype,
                                  "totalbudget": totalbudget,
                                  "totalhours": totalhours,
                                  "jobstatus": "pending",
                                  "draft": draft,
                                  "publisheddatetime": publisheddatetime,
                                  "personsrequired": int(person),
                                  "reportedJSON": [],
                                  "active": True,
                                  "cancellationreason": None,
                                  "cityid": city,
                                  "online": jobOnline,
                                  "addressJSON": addressJSON,
                                  "locationid": location,
                                  "personsselected": 0,
                                  "originaljobid": originaljobid,
                                  "adminapprovalforcancellation": None,
                                  "skillid": None,
                                  "tags": None,
                                  "updatedatetime": datetime.now(),
                                  "createdatetime": datetime.now(),
                                  "expired": False
                                  })
            return jsonify({'status': 200, 'message': 'Job Created.', 'jobid': jobid})
        else:
            Jobs.update({"jobid": jobid}, {"$set": {"title": title,
                                                    "description": description,
                                                    "creatinguserid": userid,
                                                    "duedate": duedate,
                                                    "budget": budget,
                                                    "budgettype": budgettype,
                                                    "totalbudget": totalbudget,
                                                    "totalhours": totalhours,
                                                    "jobstatus": "pending",
                                                    "draft": draft,
                                                    "publisheddatetime": publisheddatetime,
                                                    "personsrequired": int(person),
                                                    "reportedJSON": [],
                                                    "active": True,
                                                    "cancellationreason": None,
                                                    "cityid": city,
                                                    "online": jobOnline,
                                                    "addressJSON": addressJSON,
                                                    "locationid": location,
                                                    "personsselected": 0,
                                                    "originaljobid": originaljobid,
                                                    "adminapprovalforcancellation": None,
                                                    "skillid": None,
                                                    "tags": None,
                                                    "updatedatetime": datetime.now(),
                                                    "expired": False}})
            return jsonify({'status': 200, 'message': 'Job Updated.', 'jobid': jobid})

    except Exception as e:
        return jsonify({'status': 500, 'message': "error"})
