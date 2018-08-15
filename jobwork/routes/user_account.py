
from flask import request,Blueprint,jsonify
from datetime import datetime
from jobwork.models.user import User
from jobwork.middleware.authentication import authentication
usr_account=Blueprint('usr_account',__name__,url_prefix='')




@usr_account.route('/reportData', methods=['POST'])
def reportData():
    try:
        by_userid = request.json['userid']
        to_userid = request.json['to_userid']
        token = request.json['token']
        reporteddatetime = datetime.now()
        reportresolved = False
        reportresolveddatetime = datetime.now()

        temp = []

        temp.append({"by_userid" : by_userid})
        temp.append({"reportresolved" : reportresolved})
        temp.append({"reporteddatetime" : reporteddatetime})
        temp.append({"reportresolveddatetime" : reportresolveddatetime})

        User.update({"userid" : to_userid}, {"$set" : {"reportedJSON" : temp}})
        return jsonify({"status":200,"message":"Successfully Report Created."})
    except Exception as e:
        return jsonify({"status":500,"message":e.message})


@usr_account.route('/save/devicetoken', methods=['POST'])
def save_token():
    userid = int(request.json['userid'])
    token = request.json['token']
    devicetoken = request.json['devicetoken']
    version = request.json['version']
    os = request.json['os']

    User.update({"userid": userid}, {"$set": {"device_token": devicetoken, "version": version, "os": os}})
    return jsonify({"status": 200, "message": "Successfully updated."})
