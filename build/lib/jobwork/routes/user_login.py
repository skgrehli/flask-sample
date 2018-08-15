from flask import request,Blueprint,jsonify,session
from jobwork.models.user import User
import hashlib
from jobwork.constants import Constants

user_login=Blueprint('user_login',__name__,url_prefix='')

URL = Constants.URL
imagePath = Constants.IMAGE_PATH

@user_login.route('/user/login' ,methods=['POST'])
def userlogin():
    try:
        email = request.json['email']
        password = request.json['password']

        if email is not None and password is not None:
            salt = ""
            userdata = User.find_one({"signupJSON.email" :email ,"isadmin" :False ,"active" :True})
            print (userdata)
            # if userData.count == 0 :
            # 	userdata = user.find_one({"signupJSON.mobile":int(email),"isadmin":False,"active":True})
            if userdata is not None:
                salt = userdata['salt']
                password = hashlib.md5(password.strip()).hexdigest() + salt
                print (password)
                result = User.find_one({"email" :email , "password" : password})
                if result is not None:
                    fullname = result['firstname' ] +"  " +result['lastname']
                    session['cookiesUserid']    = int(result['userid'])
                    session['userValid']		= result['salt']
                    session['cookiesToken']		= str(result['token'])
                    session['city']		        = str(result['addressJSON']['city'])
                    session['userloginName']    = fullname
                    session['location']         = str(result['locationid'])
                    session.permanent = True
                    print (session)
                    picPath = URL +imagePath
                    print (request.cookies)
                    return jsonify({'status' :200 , 'message' : 'success' , 'userid' : result['userid'] ,
                                    'token' : result['token'] ,
                                    'city' : result['addressJSON']['city'],
                                    'location': result['locationid'],
                                    "firstname" : result['firstname'],
                                    "lastname" : result['lastname'],
                                    "picurl" : result['picurl'],
                                    "picPath" : picPath})
                else:
                    return jsonify({'status' :201 , 'message' : 'Invalid username and Password.'})
            else:
                return jsonify({'status' :202 , 'message' : 'Invalid username.'})
        else:
            return jsonify({'status' :203, 'message' :"Email or Password not be null."})

    except Exception as e:
        return jsonify({"status" :500 ,"message" :"error"})
