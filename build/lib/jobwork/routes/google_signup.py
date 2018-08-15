import datetime

from flask_oauthlib.client import OAuth
from jobwork.auth.settings.google import GoogleAuthConst
from flask import request, Blueprint, url_for, session, jsonify
from jobwork.constants import Constants
from jobwork.models.user import User
from jobwork.utils.common_utils import CommonUtils
from jobwork.utils.email import EmailUtils
from jobwork.utils.fcm import PushNotificationUtils
from jobwork.utils.signup import SignupUtils

google_signup = Blueprint('google_signup', __name__, url_prefix='')
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.googleapis.com/oauth2/v1/',
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          consumer_key=GoogleAuthConst.CLIENT_ID,
                          consumer_secret=GoogleAuthConst.CLIENT_SECRET,
                          request_token_params={'scope': ('email', )},
                          )


@google_signup.route('/google/login')
def google_login():
    if 'google_token' in session:
        me = google.get('userinfo?fields=email,name,given_name,family_name,gender,id,picture,verified_email')
        print(me)
        return jsonify({"data": me.data})
    return google.authorize(
        callback=url_for('google_signup.google_authorized', next=request.args.get('next') or request.referrer or None,
                         _external=True))


@google_signup.route('/google/login/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return jsonify({"data": me.data, "next": request.args.get('next')})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# noinspection SpellCheckingInspection
def get_or_create_user(user_data, user_type, google_token):
    email = user_data.get("email", "")
    if email:
        is_user_exists = User.count({"signupJSON.email": email})
        if is_user_exists == 0:
            mobile, mobileotp = "", ""
            # emailhash = send_email(email)
            emailhash = CommonUtils.getHashValue()

            firstname = user_data.get('given_name', "")
            lastname = user_data.get('family_name', "")
            usertype = user_type
            city, location, device_token = "", "", ""
            fullname = user_data.get("name", "")
            password = CommonUtils.generateRandomName()

            if fullname and usertype:

                salt = CommonUtils.generateRandomName()

                # random.randrange(1000, 9999)

                signupJSON = SignupUtils.get_signup_json(email, googleid=user_data.get("id", ""),
                                                         googletoken=google_token)

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

                return {
                    'status': 200,
                    'message': 'Successfull Register',
                    'userid': userid,
                    'token': token,
                    'city': city,
                    'location': location,
                    "firstname": firstname,
                    "lastname": lastname,
                    "picurl": "user-no-image.jpg",
                    "picPath": Constants.PROFIL_PIC_STATIC_PATH
                }
            else:
                return {'status': 400, 'message': 'Data can not be null.'}
        else:
            user = User.find_one({"email": email},
                                 {"_id": 0, "userid": 1, "token": 1, "city": 1, "location": 1, "firstname": 1,
                                  "lastname": 1, "picurl": 1, "picPath": Constants.PROFIL_PIC_STATIC_PATH})
            return {
                'status': 200,
                'message': 'Successfull Register',
            }.update(user)
    else:
        return {'status': 202, 'message': 'Data can not be null.'}
