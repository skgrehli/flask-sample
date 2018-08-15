import datetime

from flask import request, Blueprint, make_response, jsonify
from jobwork.constants import Constants
from jobwork.middleware.authentication import authentication
from jobwork.models.city import CityCollections
from jobwork.models.country import CountryCollections
from jobwork.models.jobreviews import JobReviews
from jobwork.models.locations import Locations
from jobwork.models.user import User
from jobwork.models.userportfolio import UserPortfolio
from jobwork.utils.common_utils import CommonUtils

user_updates = Blueprint('user_bank', __name__, url_prefix='')


# noinspection SpellCheckingInspection
@user_updates.route('/api/user/update', methods=['POST'])
@authentication
def user_update():
    try:
        userid = int(request.json['userid'])
        token = request.json['token']
        location = request.json['location']
        if location != "":
            location = int(location)

        find_user = User.find_one({"userid": userid, "active": True})

        if find_user is not None:
            skills = request.json['skills']

            print(skills)
            print(type(skills))

            if request.json['dob'] != "":
                birth = request.json['dob']
                print(birth)
                format = '%d-%m-%Y'
                dob = datetime.datetime.strptime(birth, format)
            else:
                dob = ""

            if request.json['city'] != "":
                citydetail = CityCollections.find_one({"cityid": int(request.json['city'])}, {"_id": 0})
                addressJSON = {
                    "address1": request.json['address1'],
                    "address2": request.json['address2'],
                    "city": int(request.json['city']),
                    "state": citydetail['stateid'],
                    "country": citydetail['countryid'],
                    "pincode": request.json['pincode']
                }
            else:
                addressJSON = {
                    "address1": request.json['address1'],
                    "address2": request.json['address2'],
                    "city": "",
                    "state": "",
                    "country": "",
                    "pincode": request.json['pincode']
                }

            if request.json['isdcode'] != "" and request.json['isdcode'] is not None:
                isdcode = int(request.json['isdcode'])
            else:
                isdcode = ""

            # locationData = location.find_one({"cityid" : int(request.json['city'])},{"_id":0,"locationid":1})

            # skillsJSON = []
            # for skillDataJSON in skills:
            # 	stringData = '.*'+skillDataJSON+'.*'
            # 	skillsData = skills.find_one({"skillname" : { "$regex" : skillDataJSON, "$options" : 'i' }},{"_id":0,"skillid":1,"skillname":1})
            # 	if skillsData is not None:
            # 		for skillsCollections in skillsData :
            # 			skillDict = {"skillid" : skillsCollections['skillid'],
            # 						"skillname" : skillsCollections['skillname']}
            # 			skillsJSON.append(skillDict)

            randomNameForFile = ""
            # if request.json['imageFlag']:
            # 	randomNameForFile = "image_"+str(int(time.time()))+".jpg"
            # 	fh = open("static/images/profile/"+randomNameForFile, "wb")
            # 	fh.write(request.json['picurl'].decode('base64'))
            # 	fh.close()

            # languagesJSON = request.json['languagesJSON']
            # educationCSV = request.json['educationCSV']
            # workplaceCSV = request.json['workplaceCSV']
            # certificateJSON = request.json['certificateJSON']
            # reportedJSON = list(report.find({ "userid" : userid, "token" : token }, {"_id":0}))
            if find_user['mobile'] != str(request.json['mobile']):
                User.update({"userid": userid}, {"$set": {
                    "signupJSON.mobile": str(request.json['mobile']),
                    "mobile": str(request.json['mobile']),
                    "mobileverified": False,
                    "proJSON.mobileverified": False
                }})
            if find_user['email'] != str(request.json['email']):
                User.update({"userid": userid}, {"$set": {
                    "signupJSON.email": str(request.json['email']),
                    "email": str(request.json['email']),
                    "emailverified": False
                }})

            result = User.update({"userid": userid}, {"$set": {
                "firstname": request.json['firstname'],
                "lastname": request.json['lastname'],
                "aboutme": request.json['aboutme'],
                "languagesJSON": [],
                "educationCSV": [],
                "workplaceCSV": [],
                "updateddatetime": datetime.datetime.now(),
                "isdcode": isdcode,
                "addressJSON": addressJSON,
                "skillsJSON": skills,
                "gender": request.json['gender'],
                "dob": dob,
                "locationid": location
            }})

            userdata_array = list(User.find({"userid": userid, "active": True}, {"_id": 0}))

            resultArray = {}
            responseArr = []

            if len(userdata_array) > 0:
                for collectionInfo in userdata_array:
                    # cityname = citycollections.find_one({"cityid":collectionInfo['addressJSON']['city']},{"_id":0})
                    # allCityData = list(CityCollections.find({}, {"_id": 0, "cityid": 1, "city": 1}))
                    # allcity = []
                    # if len(allCityData) > 0:
                    # 	for getAllCityData in allCityData:
                    # 		allcity.append({"cityid" : getAllCityData['cityid'], "city" : getAllCityData['city']})

                    location_name = ""
                    if collectionInfo['addressJSON']['city'] != "":
                        citynamedata = CityCollections.find_one({"cityid": collectionInfo['addressJSON']['city']},
                                                                {"_id": 0})
                        city_name = citynamedata['city']
                        countrynamedata = CountryCollections.find_one(
                            {"countryid": collectionInfo['addressJSON']['country']}, {"_id": 0})
                        country_name = countrynamedata['country']
                    else:
                        city_name = ""
                        country_name = ""

                    if collectionInfo['locationid'] != "":
                        location_name_data = Locations.find_one({"locationid": int(collectionInfo['locationid'])},
                                                                {"_id": 0, "locationname": 1, "under": 1})
                        if location_name_data is not None:
                            if location_name_data['under'] != "":
                                location_name = str(location_name_data['under']) + " - " + str(
                                    location_name_data['locationname'])
                            else:
                                location_name = str(location_name_data['locationname'])
                    else:
                        location_name = ""

                    skill_data = collectionInfo['skillsJSON']
                    skillNameData = []
                    if len(skill_data) > 0:
                        for skillDataCollections in skill_data:
                            skillNameData.append(skillDataCollections['skillname'])

                    rating = 0  # Rating Initially 0
                    userReview = list(JobReviews.find({"touserid": collectionInfo['userid'], "active": True},
                                                      {"_id": 0, "rating": 1}))
                    if len(userReview) > 0:
                        totalUserReview = len(userReview)
                        if userReview is not None:
                            for userRating in userReview:
                                rating = rating + userRating['rating']

                            tatalRating = int(rating / totalUserReview)
                    else:
                        tatalRating = 0
                    allCityData = list(CityCollections.find({}, {"_id": 0, "cityid": 1, "city": 1}))
                    picurlPath = Constants.PROFIL_PIC_STATIC_PATH + collectionInfo['picurl']
                    portfolioData = list(UserPortfolio.find({"userid": userid, "active": True,}, {"_id": 0}))
                    documentsPath = Constants.URL + Constants.DOC_PATH
                    portfolioDataPath = Constants.URL + Constants.PORTFOLIO_PATH
                    updateJSON = {"cityname": city_name, "locationName": location_name, "countryname": country_name,
                                  "allcity": allCityData, "skillName": skillNameData, "portfolioData": portfolioData,
                                  "picurlPath": picurlPath, "userrating": tatalRating, "documentsPath": documentsPath,
                                  "portfolioDataPath": portfolioDataPath}
                    collectionInfo.update(updateJSON)

                    responseArr.append(collectionInfo)
                resultArray['data'] = responseArr
            else:
                resultArray['data'] = responseArr

            return make_response(jsonify(
                {'status': 200, 'message': 'Successfull Updated', 'userid': userid, 'token': token,
                 'updateData': responseArr}), 200)
        else:
            return make_response(jsonify(
                {'status': 402, 'message': 'No User Found.', 'userid': userid, 'token': token, 'updateData': []}), 400)

    except Exception as e:
        CommonUtils.print_exception()
        return make_response(jsonify({"status": 500, "message": str(e)}), 500)
