from jobwork.middleware.authentication import authentication
from jobwork.models.city import CityCollections
from jobwork.models.country import CountryCollections
from  jobwork.models.locations import Locations
from jobwork.models.jobbids import JobBids
from flask import Blueprint,request,make_response,jsonify
from jobwork.models.conversations import Conversations
from jobwork.db_connection import db


datalist=Blueprint('datalist',__name__,url_prefix='')



@datalist.route('/city/name/byid',methods=['POST'])
def city_name_data():
    try:
        cityid = int(request.json['cityid'])

        cityNameData = CityCollections.find_one({"cityid":cityid},{"_id":0,"city":1})
        print(cityNameData)
        if cityNameData is not None:
            city_name = cityNameData['city']
            return jsonify({"status":200, "message":"City Name.", "city_name" : city_name})
        else:
            return jsonify({"status":200, "message":"City Name.", "city_name" : ""})

    except Exception as e:
        return jsonify({"status":500, "message": e.message})


@datalist.route('/location/list',methods=['POST'])
def location_list():
	try:
		cityid = int(request.json['cityid'])
		cityData = list(CityCollections.find({"cityid":cityid},{"_id":0}))
		country = list(CountryCollections.find({"countryid":cityData[0]['countryid']},{"_id":0}))

		locationData = list(Locations.find({"cityid":cityid},{"_id":0}))
		if len(locationData) > 0:
			return jsonify({"status":200, "message":"Location List.", "locationList" : locationData,"country": country})
		else:
			return jsonify({"status":200, "message":"Location List.", "locationList" : locationData, "country" :country})

	except Exception as e:
		return jsonify({"status":500, "message": e.message})


@datalist.route('/city/list',methods=['POST'])
def city_list():
	try:
		cityData = list(CityCollections.find({},{"_id":0}))

		return jsonify({"status":200, "message":"City List.", "cityList" : cityData})

	except Exception as e:
		return jsonify({"status":500, "message": e.message})

@datalist.route('/location/name/byid',methods=['POST'])
def location_name_data():
	try:
		locationid = int(request.json['locationid'])
		locationNameData = Locations.find_one({"locationid":locationid},{"_id":0,"locationname":1,"under":1})
		if locationNameData is not None:
			if locationNameData['under'] != "":
				location_name = locationNameData['under']+" - "+locationNameData['locationname']
			else:
				location_name = locationNameData['locationname']
			return jsonify({"status":200, "message":"Location Name.", "location_name" : location_name})
		else:
			return jsonify({"status":200, "message":"Location Name.", "location_name" : ""})

	except Exception as e:
		return jsonify({"status":500, "message": e.message})


