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

URL = Constants.URL
imagePath = Constants.IMAGE_PATH

jw_email=Blueprint('jw_email',__name__,url_prefix='')

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

@jw_email.route('/job/comment/create', methods=['POST'])
def job_comment_create():
    # Check authentications keys
    if request.json.has_key('userid') == False or request.json.has_key('token') == False:
        return jsonify({ "status" :401 ,"message" :"Authentication keys are missing." })

    userid = int(request.json['userid'])
    token = request.json['token']

    # Authenticate credentials
    if authentication(userid ,token) ==  False:
        return jsonify({"status" :400 ,"message" :"Authentication Failed."})

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

        return jsonify({"status" : 200, "message" :"Comments created.", "getNewJobComment" :getNewJobComment})
    else:
        return jsonify({"status" : 200, "message" :"No Job Found.", "getNewJobComment" :[]})



# ********************************************************* Job Comments List +++++++++++++++++++

@jw_email.route('/job/comment/list', methods=['POST'])
def job_comment_list():
    # Check authentications keys
    if request.json.has_key('userid') == False or request.json.has_key('token') == False:
        return jsonify({ "status" :401 ,"message" :"Authentication keys are missing." })

    userid = int(request.json['userid'])
    token = request.json['token']

    # Authenticate credentials
    if authentication(userid ,token) ==  False:
        return jsonify({"status" :400 ,"message" :"Authentication Failed."})

    # jobData = jobs.find({},{"_id":0,"jobid":1})

    jobCommentsList = list(JobComments.find({"jobid" :request.json['jobid'], "active" :True} ,{"_id" :0}))

    return jsonify({"status" : 200, "message" :"Job Comments List.", "jobCommentsList" :jobCommentsList})

