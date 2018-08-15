from flask import request, Blueprint, make_response, jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.user import User
from jobwork.models.messagetrack import MessageTracks
from jobwork.utils.common_utils import CommonUtils
from twilio.rest import Client
from jobwork.constants import Constants
from datetime import datetime

user_otp=Blueprint('user_otp', __name__, url_prefix='')

msgclient = Client(Constants.MSG_ACCOUNT_SID, Constants.MSG_AUTH_TOKEN)
msgtrckid = CommonUtils.generateRandomNo(MessageTracks, "messagetrackid")


@user_otp.route('/getmobileotp', methods=['POST'])
@authentication
def get_otp():
    try:
        userid = int(request.json['userid'])
        token = request.json['token']
       # response = User.find_one({"userid" : userid, "token": token, "mobile":str(request.json['mobile']), "isdcode":int(request.json['isdcode']), "active":True},{"_id":0})
        mobileotp =CommonUtils.generateOTP()

        '''result = User.update({"userid": userid, "token": token, "isdcode": int(request.json['isdcode']),
                              "mobile": str(request.json['mobile'])}, {"$set": {
            "mobileotp": int(mobileotp),
            "mobileverified": False
        }})'''

        sendText = "SAVEonJOBS Mobile Verify OTP is " + str(mobileotp)


        full_mobile_number = "+" + str(request.json['isdcode']) + str(request.json['mobile'])
        time=datetime.now()
        message = msgclient.messages.create(body=sendText, to=full_mobile_number, from_=Constants.MSG_SEND_FROM)

        MessageTracks.insert({"messagetrackid": msgtrckid, "userid": userid,
                              "mobile": full_mobile_number, "messagetext": sendText, "messagesid": message.sid,
                              "createdatetime": datetime.now(), "updatedatetime": datetime.now()})

        return jsonify({'status': 200, 'message': 'OTP send Successfully.'})



    except Exception as e:
        print(e)
        return make_response(jsonify({"status": 500, "message": "Something went wrong, Please try again!"}), 500)



@user_otp.route('/user/verify/mobile/otp', methods=['POST'])
def verify_mobile_otp():
    userid = int(request.json['userid'])
    token = request.json['token']
    findUser = User.find_one({"userid" : userid, "token": token, "mobile":str(request.json['mobile']), "mobileotp":int(request.json['mobileotp']), "isdcode":int(request.json['isdcode']), "mobileverified": False, "active":True})
    if findUser is not None:
        result = User.update({	"userid" : userid, "token": token, "mobile":str(request.json['mobile'])},{"$set":{
                                                                                                                "mobileverified": True
                                                                                                                ,"proJSON.mobileverified":True}})
        sendText = "Your Mobile Number is registered to SAVEonJOBS."
        full_mobile_number = "+"+str(request.json['isdcode'])+str(request.json['mobile'])
        message = msgclient.messages.create(body=sendText,to=full_mobile_number,from_=Constants.MSG_SEND_FROM)
        print(message.sid)
        MessageTracks.insert({"messagetrackid":CommonUtils.generateRandomNo(MessageTracks,"messagetrackid"),"userid":userid,"mobile":full_mobile_number,"messagetext":sendText,"messagesid":message.sid,"createdatetime":datetime.now(),"updatedatetime":datetime.now()})
        userdata = list(User.find({"userid" : userid},{"_id":0}))
        return jsonify({'status':200 , 'message' : 'Verify Successfully.', "userdata":userdata})
    else:
        return jsonify({'status':201 , 'message' : "OTP and Mobile Number doesn't match."})



@user_otp.route('/sendmsg', methods=['POST'])
def senddata():
    message = msgclient.messages.create(body="Hello from Python" ,to=request.json['tonumber'] ,from_=Constants.MSG_SEND_FROM)
    print(message.sid)
    return "success"



