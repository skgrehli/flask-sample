from jobwork.models.city import CityCollections
from jobwork.models.locations import Locations
from jobwork.utils.common_utils import CommonUtils
from datetime import datetime
from flask import request,Blueprint
from geopy.geocoders import Nominatim

location_route = Blueprint('location_route', __name__, url_prefix='')

@location_route.route('/addCity', methods=['POST'])
def addCity():
    CityCollections.insert({"city" :"Vancouver" ,"countryid" : 647010771 ,"stateid" : 719887913
                            ,"cityid" : CommonUtils.generateRandomNo(CityCollections ,"cityid"), "active" : True
                            ,"createddatetime" : datetime.now(), "updateddatetime" : datetime.now()
                            ,"gpsJSON" : {"lat" : 49.246292 ,"lng" : -123.116226 ,"lnglat" : [-123.116226 ,49.246292]
                                        ,"radius" : ""}})
    return "success"

@location_route.route('/subLocation', methods=['POST'])
def subLocattion():
    geolocator = Nominatim()
    cityname = request.json['cityname']
    for citydata in cityname:
        city_string = citydata['name' ] +", canada"
        locationdata = geolocator.geocode(city_string)
        Locations.update({"locationid" : citydata['locationid'] ,"cityid" : citydata['cityid']} ,{"$set" :
            {"gpsJSON" : {"lat" : locationdata.latitude ,"lng" : locationdata.longitude
                        ,"lnglat" : [locationdata.longitude ,locationdata.latitude] ,"radius" : ""}
            ,"location_raw" :locationdata.raw}})
    return "succeess"
