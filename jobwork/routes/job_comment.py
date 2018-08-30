from  jobwork.constants import Constants
from flask import request,Blueprint,jsonify
from jobwork.models.user import User
from jobwork.middleware.authentication import authentication
from jobwork.models.jobs import Jobs
from jobwork.utils.common_utils import CommonUtils
from jobwork.models.jobcomments import JobComments
from jobwork.models.notification import Notifications
from datetime import datetime
from pyfcm import FCMNotification
from jobwork.db_connection import db

URL = Constants.URL
imagePath = Constants.IMAGE_PATH

jw_com=Blueprint('jw_com',__name__,url_prefix='')

push_service = FCMNotification(api_key="AAAAtudwsIM:APA91bHK-EizhjQr8D1p60liGYW6glt1y9Y5_OIfELjCnyrJm33kFLjQ0cdVwmyh3z2-6NwUo8nxORgQBe3WfNi-0U_CXHHt1Msq93R4QBsvgwvRpjzmU2gxOKwTI9LdU4VYkMlOFbMm")

def find_FCM_id(userid):
	try:
		result = User.find_one({"userid": int(userid)})
		if "device_token" in result:
			return result['device_token']
		else:
			return False
	except Exception as e:
		raise e

@jw_com.route('/job/comment/create', methods=['POST'])

def job_comment_create():
    # Check authentications keys
    userid = request.json['userid']
    token = request.json['token']
    if userid=="" or token=="":
        return jsonify({"status": 200, "message": "user id or token cannot be empty", "response": [], "error": True})
    userid=int(userid)
    jobData = Jobs.find_one({"jobid" :int(request.json['jobid'])} ,{"_id" :0})
    if jobData is not None:
        userCollection = User.find_one({"userid" :userid} ,{"_id" :0})
        if userCollection is not None:
            fullname = userCollection['firstname' ] +"  " +userCollection['lastname']
            if userCollection['picurl'] != "":
                picurl = URL +imagePath +userCollection['picurl']
            else:
                picurl = URL +imagePath +"user-no-image.jpg"
        else:
            fullname = ""
        commentid = CommonUtils.generateRandomNo(JobComments ,"commentid")
        JobComments.insert({"commentid" : commentid,
                            "jobid" : int(request.json['jobid']),
                            "userid" : userid,
                            "comment" : request.json['comment'],
                            "reportedJSON" : [],
                            "createdatetime" : datetime.now(),
                            "updatedatetime" : datetime.now(),
                            "active" : True ,
                            "picurl" : picurl
                            })

        commentData = list(JobComments.find({"jobid" : int(request.json['jobid'])} ,{"_id" :0 ,"userid" :1}))
        if len(commentData) > 0:
            userArray = []
            for commentCollection in commentData:
                if commentCollection['userid'] != jobData['creatinguserid'] and commentCollection['userid'] != userid:
                    userArray.append(commentCollection['userid'])

            userArrayList = list(set(userArray))

            if jobData['creatinguserid'] != userid:
                notificationtext = fullname +" commented on your job - title  " +jobData['title']

                registration_id = find_FCM_id(jobData['creatinguserid'])
                if(registration_id):
                    data_message = {
                        "body" : notificationtext,
                    }

                    result = push_service.notify_single_device(registration_id=registration_id, message_title="New comment"
                                                               ,message_body=notificationtext, data_message=data_message, click_action="FCM_PLUGIN_ACTIVITY")


                Notifications.insert({"notificationid" :CommonUtils.generateRandomNo(Notifications ,"notificationid"),
                                      "notificationtext" :notificationtext,
                                      "notificationtype" :"Comment",
                                      "notificationtouserid" :int(jobData['creatinguserid']),
                                      "notificationfromuserid" :userid,
                                      "jobid" :jobData['jobid'],
                                      "bidid" :-1,
                                      "commentid" :commentid,
                                      "createddatetime" :datetime.now(),
                                      "updatedatetime" :datetime.now(),
                                      "isread" :False
                                      })
            else:
                print("job created userid and userid is same.")
            for userArrayListData in userArrayList:
                notificationtext = fullname +" commented on your job - title  " +jobData['title']

                registration_id = find_FCM_id(userArrayListData)
                if(registration_id):
                    data_message = {
                        "body" : notificationtext,
                    }

                    result = push_service.notify_single_device(registration_id=registration_id, message_title="New Comment"
                                                               ,message_body=notificationtext, data_message=data_message, click_action="FCM_PLUGIN_ACTIVITY")


                Notifications.insert({"notificationid" :CommonUtils.generateRandomNo(Notifications ,"notificationid"),
                                      "notificationtext" :notificationtext,
                                      "notificationtype" :"Comment",
                                      "notificationtouserid" :int(userArrayListData),
                                      "notificationfromuserid" :userid,
                                      "jobid" :jobData['jobid'],
                                      "bidid" :-1,
                                      "commentid" :commentid,
                                      "createddatetime" :datetime.now(),
                                      "updatedatetime" :datetime.now(),
                                      "isread" :False
                                      })
        else:
            print ("No comment data.")

        print( commentid)

        getNewJobComment = list(JobComments.find({"commentid" :commentid} ,{"_id" :0}))

        print (getNewJobComment)

        return jsonify({"status" : 200, "message" :"Comments created.", "response" :getNewJobComment,"error":False})
    else:
        return jsonify({"status" : 200, "message" :"No Job Found.", "response" :[],"error":True})



# ********************************************************* Job Comments List +++++++++++++++++++

@jw_com.route('/job/comment/list', methods=['POST'])
def job_comment_list():
    # Check authentications keys
    response=[]
    jobid=int(request.json['jobid'])
    jobCommentsList = db.jobcomments.find({"jobid" :jobid, "active" :True} ,{"_id" :0})
    job=Jobs.find_one({"jobid":jobid})
    jobowner=job['creatinguserid']
    for data in jobCommentsList:

        userId=User.find_one({"userid":data['userid']})
        username=userId['firstname']+" "+userId['lastname']
        data.update({"username":username})
        if(data['userid']==jobowner):
            data.update({"jobowner":True})
        else:
            data.update({"jobowner":False})
        response.append(data)
    if len(response)!=0:
        return jsonify({"status" : 200, "message" :"Job Comments List.", "jobCommentsList" :response,"error":False})
    else:
        return jsonify(
            {"status": 200, "message": "Job Comments List empty", "jobCommentsList": [], "error": True})


