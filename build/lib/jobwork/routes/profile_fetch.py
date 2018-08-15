from flask import Blueprint,request,make_response,jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.user import User
from jobwork.constants import Constants
from jobwork.models.city import CityCollections
from jobwork.models.jobs import Jobs
from jobwork.models.jobreviews import JobReviews
from jobwork.models.locations import Locations
from jobwork.models.userportfolio import UserPortfolio

profile_fetch=Blueprint('profile_fetch',__name__,url_prefix='')

@profile_fetch.route('/user/profile/fetch', methods=['POST'])
@authentication
def user_profile_fetch():
    URL = Constants.URL
    imagePath = Constants.IMAGE_PATH

    try:
        # Check Authentication Key.
        userid = int(request.json['userid'])
        token = request.json['token']
        otherUserId = int(request.json['messageUserid'])



        userdata_array = list(User.find({"userid" :otherUserId, "active" :True} ,{"_id" :0}))

        resultArray ={}
        responseArr =[]
        temp =[]

        reportStatus = False

        if len(userdata_array) > 0 :
            for collectionInfo in userdata_array :
                reportedJSONdata = collectionInfo['reportedJSON']
                if len(reportedJSONdata) > 0:
                    for reportStatusData in reportedJSONdata:
                        # print reportStatusData['byuserid']
                        if reportStatusData['byuserid'] == userid:
                            reportStatus = True
                else:
                    reportStatus = False

                reviewsDataList = list \
                    (JobReviews.find({"touserid" :otherUserId, "adminaction" :True, "active" : True} ,{"_id" :0}))
                reviewsData = []
                if len(reviewsDataList) > 0:
                    for collectionInfoReview in reviewsDataList:
                        userdata = User.find_one({"userid" :collectionInfoReview['userid'] ,"active" :True} ,{"_id" :0})
                        if userdata is not None:
                            fullname = userdata['firstname'] + ' ' + userdata['lastname']
                            if userdata['picurl'] != "":
                                picurl = URL +imagePath +userdata['picurl']
                            else:
                                picurl = URL +imagePath +"user-no-image.jpg"
                        if collectionInfoReview.has_key('jobid'):
                            jobData = Jobs.find_one({"jobid" :collectionInfoReview['jobid'], "active" :True}
                                                    ,{"_id" :0})
                            if jobData is not None:
                                title = jobData['title']
                            else:
                                title = ""
                        editionData = {"fullname" : fullname, "jobtitle" : title, "picurl" : picurl}
                        collectionInfoReview.update(editionData)
                        reviewsData.append(collectionInfoReview)
                else:
                    reviewsData = []

                locationName = ""
                cityName = ""

                if collectionInfo['addressJSON']['city'] != "":
                    citynamedata = CityCollections.find_one({"cityid" :int(collectionInfo['addressJSON']['city'])}
                                                            ,{"_id" :0})
                    cityName = citynamedata['city']
                    countrynamedata = CityCollections.find_one({"countryid" :int(citynamedata['countryid'])}
                                                              ,{"_id" :0})
                    print(countrynamedata)
                    #return jsonify({"ok": 1})
                    countryName = countrynamedata['countryid']

                else:
                    cityName = ""
                    countryName = ""

                if collectionInfo['locationid'] != "":
                    locationNameData = Locations.find_one({"locationid" :int(collectionInfo['locationid'])}
                                                          ,{"_id" :0 ,"locationname" :1 ,"under" :1})
                    if locationNameData is not None:
                        if locationNameData['under'] != "":
                            locationName = str(locationNameData['under'] ) +" -  " +str \
                                (locationNameData['locationname'])
                        else:
                            locationName = str(locationNameData['locationname'])
                else:
                    locationName = ""
                allCityData = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}))
                # allcity = []
                # if len(allCityData) > 0:
                # 	for getAllCityData in allCityData:
                # 		allcity.append({"cityid" : getAllCityData['cityid'], "city" : getAllCityData['city']})
                skillData = collectionInfo['skillsJSON']
                skillNameData = []
                if len(skillData) > 0 :
                    for skillDataCollections in skillData:
                        skillNameData.append(skillDataCollections['skillname'])

                rating = 0 # Rating Initially 0

                userReview = list(JobReviews.find({"touserid" :int(collectionInfo['userid']), "active" :True}
                                                  ,{"_id" :0 ,"rating" :1}))
                if len(userReview) > 0:
                    totalUserReview = len(userReview)
                    if userReview is not None:
                        for userRating in userReview:
                            rating = rating + userRating['rating']

                    tatalRating = int(rating / totalUserReview)
                else:
                    tatalRating = 0

                portfolioData = list(UserPortfolio.find({"userid" :otherUserId ,"active" :True ,} ,{"_id" :0}))
                picurlPath = URL +imagePath +collectionInfo['picurl']
                documentsPath = URL +Constants.DOC_PATH

                portfolioDataPath = URL +Constants.PORTFOLIO_PATH
                updateJSON = {"cityname" :cityName ,"locationName" :locationName ,"countryname" :countryName
                              ,"allcity" :allCityData ,"skillName" :skillNameData ,"reviewsData" :reviewsData
                              ,"portfolioData" :portfolioData, "reportStatus" :reportStatus, "picurlPath" :picurlPath
                              ,"userrating" :tatalRating ,"documentsPath" :documentsPath, "portfolioDataPath" :portfolioDataPath}
                collectionInfo.update(updateJSON)
                responseArr.append(collectionInfo)
            resultArray['data' ] =responseArr
            resultArray['status' ] ="200"
            resultArray['message' ] ="Userdata List."
        else:
            resultArray['data' ] =responseArr
            resultArray['status' ] ="400"
            resultArray['message' ] ="No data in List."

        return jsonify(resultArray)

    except Exception as e:
        print(e)
        return jsonify({"status" :500 })

