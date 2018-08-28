from jobwork.models.report import Report
from flask import request,Blueprint,jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.user import User
from jobwork.utils.common_utils import CommonUtils
from datetime import datetime
from jobwork.models.jobcomments import JobComments
from jobwork.models.jobs import Jobs
from jobwork.db_connection import db

jw_report=Blueprint('jw_report',__name__,url_prefix='')


@jw_report.route('/user/report/create', methods=['POST'])
@authentication
def reportuser():
    userid = int(request.json['userid'])
    token = request.json['token']
    touserid = int(request.json['touserid'])

    userreportedJSON = []

    if (userid != None) and (token != None) and (touserid != None) :
        userData = User.find_one({"userid" :touserid} ,{"_id" :0})
        if userData is not None:
            userreportedJSON = userreportedJSON + userData['reportedJSON']
            newReportedJSON = {"reportid" :CommonUtils.generateRandomNo(Report ,"reportid"),
                               "byuserid" : userid,
                               "reportresolved" : False,
                               "reporteddatetime" : datetime.now(),
                               "reportresolveddatetime" : -1,
                               "active" : True}
            userreportedJSON.append(newReportedJSON)
            User.update({ "userid" : touserid }, {"$set" : {"reportedJSON" : userreportedJSON}})

        return jsonify({"status" :200 ,"message" :"Successfully Report Created."})
    else:
        return jsonify({"status" :400 ,"message" :"No data Recevied"})



@jw_report.route('/user/job/report/comment/create', methods=['POST'])
@authentication
def reportcomment():
    userid = int(request.json['userid'])
    token = request.json['token']
    commentid = request.json['commentid']
    reporteddatetime = datetime.now()
    reportresolveddatetime = datetime.now()

    if (userid != None) and (token != None) and (commentid != None) :
        reportedJSON = {"reportid" :CommonUtils.generateRandomNo(Report ,"reportid"), "byuserid" : userid, "reportresolved" : False, "reporteddatetime" : reporteddatetime, "reportresolveddatetime" : reportresolveddatetime, "active" : True}

        commentsreportedJSON = []

        commentsreportedJSON =JobComments.find({"commentid": commentid}, {"_id": 0, "reportedJSON": 1})
        reportData = commentsreportedJSON['reportedJSON']
        temp = []
        temp.append(reportData)
        temp.append(reportedJSON)

        JobComments.update({"commentid": commentid}, {"$set": {"reportedJSON": temp}})

        return jsonify({"status": 200, "message": "Successfully Report Created."})
    else:
        return jsonify({"status": 400, "message": "No Data Recevied."})


@jw_report.route('/user/job/report/create', methods=['POST'])
@authentication
def reportjob():
    userid = int(request.json['userid'])
    token = request.json['token']
    jobid = request.json['jobid']
    message=request.json['message']
    reporteddatetime = datetime.now()
    reportresolveddatetime = datetime.now()

    if (userid != None) and (jobid != None):
        reportedJSON = {"reportid": CommonUtils.generateRandomNo(Report, "reportid"), "byuserid": userid,
                        "reportresolved": False, "reporteddatetime": reporteddatetime,
                        "reportresolveddatetime": reportresolveddatetime, "active": True}

        temp = []
        temp.append(reportedJSON)
        Jobs.update({"jobid": jobid}, {"$set": {"reportedJSON": temp}})
        Report.insert({"reportedby":userid,"jobid":jobid,"message":message,"reporttime":datetime.now(),"action":False})
        return jsonify({"status": 200, "message": "Successfully Report Created.","error":False,"response":[]})
    else:
        return jsonify({"status": 400, "message": "No Data Recevied.","error":True,"response":[]})

@jw_report.route('/user/job/wishlist/create', methods=['POST'])
@authentication
def addjobtowishlist():
    userid = int(request.json['userid'])
    token = request.json['token']
    jobid = request.json['jobid']
    data=db.wishlist.count({"userid":userid,"jobid":jobid})
    print(data)
    if data==0:
        db.wishlist.insert({"userid":userid,"jobid":jobid,"addtime":datetime.now(),"action":False})
        return jsonify({"status": 200, "message": "job added to wishlist", "error": False, "response": 0})
    else:
        return jsonify({"status": 200, "message": "job already in wish list ", "error": False, "response": 1})

@jw_report.route('/user/job/wishlist/remove', methods=['POST'])
@authentication
def removejobtowishlist():
    userid = int(request.json['userid'])
    token = request.json['token']
    jobid = request.json['jobid']
    data=db.wishlist.count({"userid":userid,"jobid":jobid})
    if data==0:
        return jsonify({"status": 200, "message": "job not found in list", "error": False, "response": 0})
    else:
        db.wishlist.remove({"userid": userid, "jobid": jobid})
        return jsonify({"status": 200, "message": "job removed from wish list ", "error": False, "response": 1})
