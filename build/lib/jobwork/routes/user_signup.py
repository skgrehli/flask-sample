import datetime

from flask import request, Blueprint, make_response, jsonify, session
from jobwork.constants import Constants
from jobwork.models.user import User
from jobwork.utils.common_utils import CommonUtils
from jobwork.utils.email import EmailUtils
from jobwork.utils.fcm import PushNotificationUtils
from jobwork.utils.signup import SignupUtils

user_signup = Blueprint('user_signup', __name__, url_prefix='')

picPath = Constants.PROFIL_PIC_STATIC_PATH


# noinspection SpellCheckingInspection,PyPep8Naming
@user_signup.route('/google/login', methods=['POST'])
def user_register():
    email = request.json['email']

    if email:
        is_user_exists = User.count({"signupJSON.email": email})
        if is_user_exists == 0:
            mobile, mobileotp = "", ""
            # emailhash = send_email(email)
            emailhash = CommonUtils.getHashValue()

            firstname = request.json['firstname']
            lastname = request.json['lastname']
            usertype = request.json['usertype']
            city = int(request.json['city'])
            location = int(request.json['location'])
            device_token = request.json.get('device_token', "")
            fullname = firstname + " " + lastname
            password = request.json['password'].strip()

            if firstname and lastname and usertype and city:

                salt = CommonUtils.generateRandomName()

                # random.randrange(1000, 9999)

                signupJSON = SignupUtils.get_signup_json(email)

                addressJSON = SignupUtils.get_user_address_json(city)

                proJSON = SignupUtils.get_pro_json()

                paymentdetailsJSON = SignupUtils.get_payment_detail_json()

                if password:
                    password = CommonUtils.password_hash(password, salt)
                token = request.json.get('token', "")
                userid = request.json.get('userid', "")
                if not userid:
                    userid = CommonUtils.generateRandomNo(User, "userid")
                if not token:
                    token = CommonUtils.generateRandomName()

                User.insert({
                    "userid": userid,
                    "email": email,
                    "mobile": mobile,
                    "mobileotp": str(mobileotp),
                    "emailhash": emailhash,
                    "password": password,
                    "salt": salt,
                    "token": token,
                    "usertype": usertype,
                    "firstname": firstname,
                    "lastname": lastname,
                    "device_token": device_token,
                    "signupJSON": signupJSON,
                    "emailverified": False,
                    "mobileverified": False,
                    "isdcode": None,
                    "fbid": "",
                    "fbaccesstoken": "",
                    "isadmin": False,
                    "createddatetime": datetime.datetime.now(),
                    "updateddatetime": datetime.datetime.now(),
                    "addressJSON": addressJSON,
                    "paymentdetailsJSON": paymentdetailsJSON,
                    "skillsJSON": [],
                    "languagesJSON": [],
                    "educationCSV": [],
                    "workplaceCSV": [],
                    "certificateJSON": [],
                    "proJSON": proJSON,
                    "forgotpasswordJSON": [],
                    "gender": "",
                    "dob": "",
                    "locationid": location,
                    "aboutme": "",
                    "picurl": "user-no-image.jpg",
                    "reportedJSON": [],
                    "notificationJSON": [],
                    "socaillogin": False,
                    "facebookpicurl": "",
                    "active": True,
                    "paypal_id": ""
                })

                session['cookiesUserid'] = int(userid)
                session['userValid'] = str(salt)
                session['cookiesToken'] = str(token)
                session['city'] = str(city)
                session['userloginName'] = str(fullname)
                session['location'] = str(location)
                session.permanent = True

                # Onboard Push notification
                PushNotificationUtils.notify_onboard(userid, fullname, device_token)
                # Onboard Email
                EmailUtils.send_onboard_email(userid, email, emailhash, firstname)

                return make_response(jsonify({
                    'status': 200,
                    'message': 'Successfull Register',
                    'userid': userid,
                    'token': token,
                    'city': city,
                    'location': location,
                    "firstname": firstname,
                    "lastname": lastname,
                    "picurl": "user-no-image.jpg",
                    "picPath": picPath
                }), 200)
            else:
                return make_response(jsonify({'status': 202, 'message': 'Data can not be null.'}), 400)
        else:
            return make_response(jsonify({'status': 201, 'message': 'Email already exits.'}), 400)
    else:
        return make_response(jsonify({'status': 202, 'message': 'Data can not be null.'}), 400)
