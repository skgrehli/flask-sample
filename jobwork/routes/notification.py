from flask import Blueprint,request,make_response,jsonify
from jobwork.models.notification import Notifications
from jobwork.models.user import User
from jobwork.models.jobs import Jobs
from jobwork.middleware.authentication import authentication
from jobwork.constants import Constants
from jobwork.models.city import CityCollections
from jobwork.models.messages import Messages

notification=Blueprint('notification',__name__,url_prefix='')

@notification.route('/notification/list', methods=['POST'])
@authentication
def notification_list():
    URL = Constants.URL
    imagePath = Constants.IMAGE_PATH
    userid = int(request.json['userid'])
    token = request.json['token']
    notificationArray = []

    notificationData = list(Notifications.find({"notificationtouserid":userid},{"_id":0}).sort("createddatetime", -1))
    notificationUnread = list(Notifications.find({"notificationtouserid":userid, "isread":False},{"_id":0}))

    print(notificationData)
    if len(notificationData) > 0:
        for collections in notificationData:
            jobber = {}
            if collections['notificationfromuserid'] != -1:
                jobber = Jobs.find_one({"jobid":int(collections['jobid'])},{"_id":0,"creatinguserid":1})
                userData = User.find_one({"userid" : int(collections['notificationfromuserid'])},{"_id":0})
                if userData is not None:
                    fullname = userData['firstname'] + " " + userData['lastname']
                    if userData['picurl'] != "":
                        picurl = URL+imagePath+userData['picurl']
                    else:
                        picurl = URL+imagePath+"user-no-image.jpg"
                    if userData['addressJSON']['city'] != "":
                        cityNamedata = CityCollections.find_one({"cityid": userData['addressJSON']['city']},{"_id":0,"city":1})
                        cityName = cityNamedata['city']
                    else:
                        cityName = ""
                else:
                    fullname = ""
                    picurl = URL+imagePath+"user-no-image.jpg"
                    cityName = ""
            else:
                fullname = "SAVEonJOBS"
                picurl = URL+"static/front_end/images/logo1.png"
                cityName = ""

            userDataCollection = {"fullname" : fullname, "cityname" : cityName, "picurl":picurl, "jobber":jobber}
            collections.update(userDataCollection)
            notificationArray.append(collections)
        return jsonify({"status" : 200, "message" : "Notification Data.", "notificationArray":notificationArray, "notificationUnread":len(notificationUnread)})
    else:
        return jsonify({"status" : 200, "message" : "No Notification data Found.", "notificationArray":[],"notificationUnread":notificationUnread})


@notification.route('/notification/read', methods=['POST'])
@authentication
def notification_read():
    userid = int(request.json['userid'])
    token = request.json['token']
    notificationData = Notifications.find_one({"notificationid":int(request.json['notificationid'])},{"_id":0})
    if len(notificationData) > 0:
        Notifications.update({"notificationid":int(request.json['notificationid'])},{"$set":{"isread":True}})
        notificationData = list(Notifications.find({"notificationid":int(request.json['notificationid'])},{"_id":0,"isread":1,"notificationid":1}))
        notificationUnread = list(Notifications.find({"notificationtouserid":userid, "isread":False},{"_id":0}))
        return jsonify({"status" : 200, "message" : "Notification Data.", "notificationReadArray":notificationData,"notificationUnread":len(notificationUnread)})
    else:
        return jsonify({"status" : 200, "message" : "No Notification data Found.", "notificationReadArray":[], "notificationUnread":0})


@notification.route('/notification/total/count', methods=['POST'])
@authentication
def notification_total_count():
    # Check authentications keys
    userid = int(request.json['userid'])
    token = request.json['token']
    notificationUnread = list(Notifications.find({"notificationtouserid": userid, "isread": False}, {"_id": 0}))
    messagesUnread = list(Messages.find({"userid": userid, "isread": False}, {"_id": 0}))

    return jsonify({"status": 200, "message": "Notification Data.", "totalmessage_unread_count": len(messagesUnread),
                    "notificationUnread": len(notificationUnread)})
