from flask import request,Blueprint,jsonify,Flask,render_template
from jobwork.models.user import User
from jobwork.middleware.authentication import authentication
from jobwork.utils.common_utils import CommonUtils
from jobwork.utils.register_utils import userDataResponse
from jobwork.constants import Constants
from jobwork.models.messagetrack import MessageTracks
from twilio.rest import Client
from datetime import datetime
from bson import json_util, ObjectId
import json
from jobwork.db_connection  import db
from flask_mail import Mail, Message
from jobwork.models.emailtrack import EmailTracks


user_register_all=Blueprint('user_register_all',__name__,url_prefix='')

msgclient = Client(Constants.MSG_ACCOUNT_SID, Constants.MSG_AUTH_TOKEN)
msgtrckid = CommonUtils.generateRandomNo(MessageTracks, "messagetrackid")


URL=Constants.URL
app=Flask(__name__)
mail=Mail()
app.config["MAIL_SERVER"] = "jobwork.io"
app.config["MAIL_PORT"] = 25
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = 'support@jobwork.io'  ## CHANGE THIS
app.config["MAIL_PASSWORD"] = 'jobwork@123'
app.config["MAIL_DEFAULT_SENDER"] = ("SAVEonJOBS", "support@jobwork.io")

mail.init_app(app)
mail = Mail(app)


@user_register_all.route('/user/register' ,methods=['POST'])

def register():

    try:
        firstname=request.json['fname']
        lastname=request.json['lname']
        email=request.json['email']
        regtype=int(request.json['regtype'])
        mobile = request.json['mobile']
        cityid = request.json['city']
        skill = request.json['skill']
        stateid = request.json['state']
        countryid = request.json['country']
        picurl = request.json['picurl']
        gender=request.json['gender']
        locationid=request.json['locationid']

        if locationid!="":
            locationid=int(locationid)

        if picurl=='':
            picurl="default-image.jpg"
        '''
        if city!="":
            citylist=db.city.find_one({"city":city},{"_id":0,"cityid":1})
            cityid=citylist['cityid']
        else:
            cityid=""

        if state!="":
            statelist=db.state.find_one({"state":state},{"_id":0,"stateid":1})
            stateid=statelist['stateid']
        else:
            stateid=""

        if country!="":
            countrylist=db.country.find_one({"country":country},{"_id":0,"countryid":1})
            countryid=countrylist['countryid']
        else:
            countryid=""
'''
        addressJSON = {
            "address1": request.json['address1'],
            "address2": request.json['address2'],
            "city": cityid,
            "state": stateid,
            "country": countryid,
            "pincode": request.json['pincode']
        }
        salt = CommonUtils.generateRandomName()
        emailhash = CommonUtils.getHashValue()
        token=CommonUtils.generateRandomName()

        if regtype==0:
            password=request.json['password']
            password = CommonUtils.password_hash(password, salt)
            sociallogin = False
            emailverified=False
            fbid=""
            fbaccesstoken=""
            registeredfrom="jobwork"

        else:
            password=""
            sociallogin=True
            emailverified=True
            fbid = request.json['fbid']
            fbaccesstoken = request.json['fbaccesstoken']
            if regtype==1:
                registeredfrom="facebook"
            elif regtype==2:
                registeredfrom="gmail"
        #return jsonify({"ok":1})
        userdata = list(User.find({"email": email}, {"_id": 0}))

        if User.count({"email":email}) ==0 :
            userid = CommonUtils.generateRandomNo(User, "userid")
            User.insert({"userid": userid,
                         "signupJSON": "",
                         "email": email,
                         "emailverified": emailverified,
                         "emailhash": emailhash,
                         "mobile": mobile,
                         "mobileverified": False,
                         "mobileotp": "",
                         "isdcode": None,
                         "fbid": fbid,
                         "fbaccesstoken": fbaccesstoken,
                         "password": password,
                         "salt": salt,
                         "token": token,
                         "firstname": firstname,
                         "lastname": lastname,
                         "isadmin": False,
                         "createddatetime": datetime.now(),
                         "updateddatetime": datetime.now(),
                         "addressJSON": addressJSON,
                         "paymentdetailsJSON": [],
                         "skillsJSON": skill,
                         "languagesJSON": [],
                         "educationCSV": [],
                         "workplaceCSV": [],
                         "certificateJSON": [],
                         "proJSON": [],
                         "forgotpasswordJSON": [],
                         "gender": gender,
                         "dob": "",
                         "locationid": locationid,
                         "aboutme": "",
                         "picurl": picurl,
                         "reportedJSON": [],
                         "notificationJSON": [],
                         "socaillogin": sociallogin,
                         "facebookpicurl": "",
                         "active": True,
                         "paypal_id": "",
                         "registeredfrom":registeredfrom
                         })
            if regtype != 0:
                response=userDataResponse(email)
                # user = list(User.find({"email": email}, {"_id": 0}))
                return  jsonify({"status":200,"response": response,"message":"","error":False,"registedfrom":registeredfrom})
            else:
                emailhash = CommonUtils.getHashValue()
                result = User.update({"userid": userid, "token": token, "email": request.json['email']}, {"$set": {
                    "emailhash": emailhash
                }})
                # Send email verification
                reset_password_link = str(URL) + "emailverify/" + str(emailhash)

                subject = "Your jobwork.io Account Email Verification"
                msg = Message(subject, sender=("JobWork", "support@jobwork.io"), recipients=[email])
                msg.html = render_template('/emailTemplates/email_verification_template.html',
                                           name=firstname, resetLink=reset_password_link, email=email)
                mail.send(msg)
                EmailTracks.insert(
                    {"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"), "userid": userid,
                     "email": request.json['email'], "subject": subject, "emailtext": msg.html,
                     "createdatetime": datetime.now(), "updatedatetime": datetime.now()})

            return jsonify(
                    {"status": 200, "response": {}, "message": "verification mail sent", "error": True, "registedfrom": registeredfrom})

        elif userdata[0]['emailverified'] == False:
            emailhash = CommonUtils.getHashValue()
            userid = CommonUtils.generateRandomNo(User, "userid")
            db.user.remove({"email": email})
            User.insert({"userid": userid,
                         "signupJSON": "",
                         "email": email,
                         "emailverified": emailverified,
                         "emailhash": emailhash,
                         "mobile": mobile,
                         "mobileverified": False,
                         "mobileotp": "",
                         "isdcode": None,
                         "fbid": fbid,
                         "fbaccesstoken": fbaccesstoken,
                         "password": password,
                         "salt": salt,
                         "token": token,
                         "firstname": firstname,
                         "lastname": lastname,
                         "isadmin": False,
                         "createddatetime": datetime.now(),
                         "updateddatetime": datetime.now(),
                         "addressJSON": addressJSON,
                         "paymentdetailsJSON": [],
                         "skillsJSON": skill,
                         "languagesJSON": [],
                         "educationCSV": [],
                         "workplaceCSV": [],
                         "certificateJSON": [],
                         "proJSON": [],
                         "forgotpasswordJSON": [],
                         "gender": gender,
                         "dob": "",
                         "locationid": locationid,
                         "aboutme": "",
                         "picurl": picurl,
                         "reportedJSON": [],
                         "notificationJSON": [],
                         "socaillogin": sociallogin,
                         "facebookpicurl": "",
                         "active": True,
                         "paypal_id": "",
                         "registeredfrom": registeredfrom
                         })
            if regtype != 0:
                response=userDataResponse(email)
                return  jsonify({"status":200,"response": response,"message":"existed now updated","error":False,"registedfrom":registeredfrom})
            else:
                emailhash = CommonUtils.getHashValue()
                result = User.update({"userid": userid, "token": token, "email": request.json['email']}, {"$set": {
                    "emailhash": emailhash
                }})
                # Send email verification
                reset_password_link = str(URL) + "emailverify/" + str(emailhash)

                subject = "Your jobwork.io Account Email Verification"
                msg = Message(subject, sender=("JobWork", "support@jobwork.io"), recipients=[email])
                msg.html = render_template('/emailTemplates/email_verification_template.html',
                                           name=firstname, resetLink=reset_password_link, email=email)
                mail.send(msg)
                EmailTracks.insert(
                    {"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"), "userid": userid,
                     "email": request.json['email'], "subject": subject, "emailtext": msg.html,
                     "createdatetime": datetime.now(), "updatedatetime": datetime.now()})

            return jsonify(
                    {"status": 200, "response": {}, "message": "mail id exist but not verified yet verification mail sent", "error": True, "registedfrom": registeredfrom})


        elif regtype!=0:
            verify=False

            user = list(User.find({"email": email}, {"_id": 0}))

            if regtype==1 and user[0]['registeredfrom']=="facebook":
                verify=True

            elif regtype == 2 and user[0]['registeredfrom'] == "gmail":
                verify = True

            else:
                message="account already registered from " + user[0]['registeredfrom']
                return jsonify({"status":200,"messsage":message,"registedfrom":user[0]['registeredfrom'],"response": {},"error":True})
                #user = list(User.find({"email": email}, {"_id": 0}))
            if verify==True:


                #print(userdata[0]['cityname'][0])
                response=userDataResponse(email)
                print((response))
                return jsonify({"status":200,"response": response,"message":"","error":False,"registedfrom":user[0]['registeredfrom']})
        else:
            return jsonify({"status":200,"messsage":"email id already used","response": {},"error":True,"registedfrom":userdata[0]['registeredfrom']})
    except Exception as  e:
        return json.dumps(e, indent=4, default=json_util.default)

