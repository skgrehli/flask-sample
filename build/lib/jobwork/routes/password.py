from flask import request, Blueprint, url_for, session, jsonify,render_template
from jobwork.models.user import User
from jobwork.models.locations import Locations
from datetime import datetime
from jobwork.utils.common_utils import CommonUtils
import hashlib
from jobwork.models.emailtrack import EmailTracks
from flask_mail import Mail, Message
from jobwork.middleware.authentication import authentication

usr_password = Blueprint('usr_password', __name__, url_prefix='')

@usr_password.route('/forgotpassword__<hashvalue>')
def forgotpasswordhash(hashvalue):
	userid = ""
	token = ""
	getuserdata = list(User.find({"$and":[{"forgotpasswordJSON.forgotpasswordhash" : hashvalue}, {"forgotpasswordJSON.forgotpassworduseddatetime":-1}]}, {"_id":0}))
	if len(getuserdata) == 1:
		for userdata in getuserdata:
			forgotpassworduseddatetime = datetime.now()
			User.update({"userid":userdata['userid'],"forgotpasswordJSON.forgotpasswordhash" : hashvalue},{"$set":{"forgotpasswordJSON.$.forgotpassworduseddatetime" : forgotpassworduseddatetime}})
			userid = userdata['userid']
			token = userdata['token']

		return render_template("front_saveonjobs/forgot_password.html", userid=userid, token=token)
	else:
		return jsonify({"status":200,"message":"URL not found."})






@usr_password.route('/user/forgotpassword/set' ,methods=['POST'])
def user_forgotpassword_set():
    try:
        email = request.json['email']
        if request.json is not None:
            if request.json['hashData'] != "" and request.json['email'] != "" and request.json['password'] != "":
                getuserdata = User.find_one \
                    ({"forgotpasswordJSON.forgotpasswordhash" : request.json['hashData'] ,"email" :request.json['email']}, {"_id" :0})
                if getuserdata is not None:
                    salt = getuserdata['salt']
                    if request.json['password'].strip() != "":
                        password = hashlib.md5(request.json['password'].strip()).hexdigest() + salt
                        User.update({"userid" :getuserdata['userid'] ,"email" :request.json['email']}
                                    ,{"$set" :{"password" : password}})



                        subject = "Your SAVEonJOBS password has changed"
                        msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[email])
                        msg.html = render_template('/emailTemplates/password_changed.html', name= getuserdata['firstname' ] +"  " +getuserdata['lastname'] )
                        Mail.send(msg)
                        EmailTracks.insert({"emailtrackid" :CommonUtils.generateRandomNo(EmailTracks ,"emailtrackid")
                                            ,"userid" :getuserdata['userid'] , "email" :email , "subject" :subject
                                            ,"emailtext": msg.html, "createdatetime": datetime.now(),
                                            "updatedatetime": datetime.now()})
                        return jsonify({"status": 200, "message": "Password Successfully changed."})
                else:
                    return jsonify({"status": 402, "message": "No user is found."})
            else:
                return jsonify({"status": 402, "message": "Data is empty."})
        else:
            return jsonify({"status": 402, "message": "No Data."})
    except Exception as e:
        return jsonify({"status": 500, "message": e.message})


# *********************************************************  Change Password ++++++++

@usr_password.route('/password/change', methods=['POST'])
@authentication
def change_password():
    try:
        userid = int(request.json['userid'])
        token = request.json['token']
        password = request.json['password']

        userdata = User.find_one({"userid": userid, "active": True}, {"_id": 0})
        if userdata is not None:
            salt = userdata['salt']
            if request.json['password'].strip() != "":
                password = hashlib.md5(request.json['password'].strip()).hexdigest() + salt

            User.update({"userid": userid}, {"$set": {"password": password}})

            return jsonify({"status": 200, "message": "Password Successfully changed."})
        else:
            return jsonify({"status": 202, "message": "No user is found."})
    except Exception as e:
        return jsonify({"status": 500, "message": e.message})


