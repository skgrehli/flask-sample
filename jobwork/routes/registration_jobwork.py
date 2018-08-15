from flask import request,Blueprint,jsonify,Flask,render_template
from jobwork.models.user import User
from jobwork.middleware.authentication import authentication
from jobwork.utils.common_utils import CommonUtils
from jobwork.constants import Constants
from jobwork.models.messagetrack import MessageTracks
from twilio.rest import Client
from datetime import datetime
from bson import json_util, ObjectId
import json
from jobwork.db_connection  import db
from flask_mail import Mail, Message
from jobwork.models.emailtrack import EmailTracks

user_register_jobwork=Blueprint('user_register_jobwork',__name__,url_prefix='')

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

@user_register_jobwork.route('/user/register/jobwork' ,methods=['POST'])
def register():
    try:

        firstname = request.json['fname']
        lastname = request.json['lname']
        email = request.json['email']
        regtype = int(request.json['regtype'])
        mobile = request.json['mobile']
        city = request.json['city']
        skill = request.json['skill']
        state = request.json['state']
        country = request.json['country']
        picurl = request.json['picurl']
        gender = request.json['gender']

        if picurl == '':
            picurl = "default-image.jpg"

        if city != "":
            citylist = db.city.find_one({"city": city}, {"_id": 0, "cityid": 1})
            cityid = citylist['cityid']
        else:
            cityid = ""

        if state != "":
            statelist = db.state.find_one({"state": state}, {"_id": 0, "stateid": 1})
            stateid = statelist['stateid']
        else:
            stateid = ""

        if country != "":
            countrylist = db.country.find_one({"country": country}, {"_id": 0, "countryid": 1})
            countryid = countrylist['countryid']
        else:
            countryid = ""

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
        token = CommonUtils.generateRandomName()

        password = request.json['password']
        password = CommonUtils.password_hash(password, salt)
        sociallogin = False
        emailverified = False
        fbid = ""
        fbaccesstoken = ""
        registeredfrom = "jobwork"

        # return jsonify({"ok":1})
        userdata = list(User.find({"email": email}, {"_id": 0}))
        #userdata=list(User.find_one({"email":email},{"id":0,"emailverified":1}))
        #return jsonify({"ok": len(userdata)})
        #print(userdata[0]['emailverified'])

        if len(userdata)==0:
            print("do resigtration")
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
            reset_password_link = str(URL) + "emailverify__" + str(emailhash)
            subject = "Your SAVEonJOBS.comAccount Email Verification"
            msg = Message(subject, sender=("SAVEonJOBS", "support@jobwork.io"), recipients=[email])
            msg.html = render_template('sample.html', name=firstname,
                                       resetLink=reset_password_link, email=email)
            mail.send(msg)
            #return jsonify({"ok": 1})

            EmailTracks.insert({"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"), "userid": userid, "email": email,
                 "subject": subject, "emailtext": msg.html, "createdatetime": datetime.now(),
                 "updatedatetime": datetime.now()})
            return jsonify({"Status":200,"message":"verification mail sent"})

        elif userdata[0]['emailverified']==False:
                emailhash=CommonUtils.getHashValue()
                userid = CommonUtils.generateRandomNo(User, "userid")
                db.user.remove({"email":email})
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
                reset_password_link = str(URL) + "emailverify__" + str(emailhash)
                subject = "Your SAVEonJOBS.comAccount Email Verification"
                msg = Message(subject, sender=("SAVEonJOBS", "support@jobwork.io"), recipients=[email])
                msg.html = render_template('/emailTemplates/email_verification_template.html', name=firstname,
                                           resetLink=reset_password_link, email=email)
                mail.send(msg)
                EmailTracks.insert(
                    {"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"), "userid": userid,
                     "email": email,
                     "subject": subject, "emailtext": msg.html, "createdatetime": datetime.now(),
                     "updatedatetime": datetime.now()})

                return jsonify({"Status": 200, "message": "verification mail sent"})
        else:
            return jsonify({"status":202,"message":"email already exist"})





    except Exception as e:
        print(e)





