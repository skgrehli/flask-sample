import datetime
from flask_oauthlib.client import OAuth
from jobwork.auth.settings.facebook import FacebookAuthConst
from flask import request, Blueprint, url_for, session, jsonify

from jobwork.constants import Constants
from jobwork.models.user import User
from jobwork.utils.common_utils import CommonUtils
from jobwork.utils.email import EmailUtils
from jobwork.utils.fcm import PushNotificationUtils
from jobwork.utils.signup import SignupUtils

facebook_signup = Blueprint('facebook_signup', __name__, url_prefix='')
oauth = OAuth()
facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FacebookAuthConst.APP_ID,
                            consumer_secret=FacebookAuthConst.APP_SECRET,
                            request_token_params={'scope': ('email',)}
                            )


@facebook_signup.route('/facebook/login')
def facebook_login():
    return facebook.authorize(
        callback=url_for('facebook_signup.facebook_authorized',
                         next=request.args.get('next') or request.referrer or None, _external=True))


@facebook_signup.route('/facebook/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me?fields=email,birthday,link,gender,first_name,last_name,name,location')
    print(me)
    return jsonify({"profile": me.data, "next": request.args.get('next')})


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

#token
#username
#email

# noinspection SpellCheckingInspection,PyPep8Naming
def get_or_create_user(user_data, user_type, facebook_token):
    email = user_data.get("email", "")
    if email:
        is_user_exists = User.count({"signupJSON.email": email})
        if is_user_exists == 0:
            mobile, mobileotp = "", ""
            # emailhash = send_email(email)
            emailhash = CommonUtils.getHashValue()

            firstname = user_data.get('first_name', "")
            lastname = user_data.get('last_name', "")
            usertype = user_type
            city, location, device_token = "", "", ""
            fullname = user_data.get("name", "")
            password = CommonUtils.generateRandomName()

            if fullname and usertype:

                salt = CommonUtils.generateRandomName()

                # random.randrange(1000, 9999)

                signupJSON = SignupUtils.get_signup_json(email, fbid=user_data.get("id", ""),
                                                         fbaccesstoken=facebook_token)

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
