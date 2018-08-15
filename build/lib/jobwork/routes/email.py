
from flask import request, Blueprint, url_for, session, jsonify,render_template
from jobwork.models.user import User
from jobwork.models.locations import Locations
from datetime import datetime
from jobwork.utils.common_utils import CommonUtils
import hashlib
from jobwork.models.emailtrack import EmailTracks
from flask_mail import Mail, Message
from jobwork.middleware.authentication import authentication
from jobwork.constants import Constants

jw_email = Blueprint('jw_email', __name__, url_prefix='')



URL=Constants.URL


@jw_email.route('/emailverify__<hashvalue>')
def emailverifyhash(hashvalue):
	getuserdata = User.find_one({"emailhash" : hashvalue, "emailverified":False}, {"_id":0})
	if getuserdata is not None:
		User.update({"emailhash" : hashvalue},{"$set":{"emailverified":True, "updateddatetime" : datetime.now()}})
		# userid = getuserdata['userid']
		# token = getuserdata['token']
		return render_template("front_saveonjobs/email_verify.html")
	else:
		return jsonify({"status":200,"message":"Email already Verified."})


@jw_email.route('/user/send/verify/email', methods=['POST'])
@authentication
def verify_email():
	#Check authentications keys
	userid = int(request.json['userid'])
	token = request.json['token']

	email = request.json['email']
	findUser = User.find_one({"userid" : userid, "token": token, "email":request.json['email'], "active":True})
	if findUser is not None:
		emailhash = CommonUtils.getHashValue()
		result = User.update({	"userid" : userid, "token": token, "email":request.json['email']},{"$set":{
																											"emailhash": emailhash
																										}})
		# Send email verification
		reset_password_link = str(URL)+"emailverify__"+str(emailhash)

		subject = "Your SAVEonJOBS.comAccount Email Verification"
		msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[email])
		msg.html = render_template('/emailTemplates/email_verification_template.html', name= findUser['firstname'], resetLink= reset_password_link ,email=email)
		Mail.send(msg)
		EmailTracks.insert({"emailtrackid":CommonUtils.generateRandomNo(EmailTracks,"emailtrackid"),"userid":userid , "email":request.json['email'] , "subject":subject ,"emailtext":msg.html ,"createdatetime":datetime.now(),"updatedatetime":datetime.now()})

		return jsonify({'status':200 , 'message' : 'Send Successfully.'})
	else:
		return jsonify({'status':201 , 'message' : "Email doesn't match."})


@jw_email.route('/user/forgotpassword/email', methods=['POST'])
def user_forgotpassword_email():
    try:
        email = request.json['email']
        if email is not None:
            getuserdata = User.find_one({"email": email, "active": True}, {"_id": 0})

            # data = user.find_one({"$or" : {"email" : email},{"mobile" : mobile}})
            addforgotpasswordJSON = []
            if getuserdata is not None:
                oldJSON = getuserdata['forgotpasswordJSON']
                forgotpassworduseddatetime = -1
                forgopassworddatetime = datetime.now()
                forgotpasswordhash = CommonUtils.getHashValue()
                addforgotpasswordJSON = addforgotpasswordJSON + oldJSON
                addforgotpasswordJSON.append({"forgopassworddatetime": forgopassworddatetime,
                                              "forgotpasswordhash": forgotpasswordhash,
                                              "forgotpassworduseddatetime": forgotpassworduseddatetime
                                              })
                User.update({"email": email}, {"$set": {"forgotpasswordJSON": addforgotpasswordJSON}})

                reset_password_link = str(URL) + "forgotpassword__" + str(forgotpasswordhash)

                subject = "Your SAVEonJOBS Password"
                msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[email])
                msg.html = render_template('/emailTemplates/Reset_password_template.html',
                                           name=getuserdata['firstname'], resetLink=reset_password_link)

                Mail.send(msg)
                EmailTracks.insert(
                    {"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"), "userid": getuserdata['userid'],
                     "email": email, "subject": subject, "emailtext": msg.html, "createdatetime": datetime.now(),
                     "updatedatetime": datetime.now()})
                return jsonify({"status": 200, "message": "Successfully mail sent."})
            else:
                return jsonify({"status": 200, "message": "No data."})
        else:
            return jsonify({"status": 200, "message": "Data is Null."})

    except Exception as e:
        return jsonify({"status": 500, "message": e.message})


