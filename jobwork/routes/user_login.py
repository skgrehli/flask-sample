from flask import request,Blueprint,jsonify,session
from jobwork.models.user import User
import hashlib
from jobwork.constants import Constants
from jobwork.db_connection import db
from jobwork.utils.register_utils import userDataResponse

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

            userdata = User.find_one({"email" :email ,"isadmin" :False})# ,"active" :True,"emailverified":True})
            if userdata['active']==False:
                return jsonify({"status": 205, "response": {}, "message": "your active is not active", "error": True})
            if userdata['emailverified'] == False:
                return jsonify({"status": 206, "response": {}, "message": "your email is not verified", "error": True})

            #print (userdata)
            # if userData.count == 0 :
            # 	userdata = user.find_one({"signupJSON.mobile":int(email),"isadmin":False,"active":True})
            if userdata is not None and userdata['active']==True and userdata['emailverified']==True :
                salt = userdata['salt']
                password = hashlib.md5(password.encode('utf-8')).hexdigest() + salt
                #return jsonify({"ok": 1})

                #print (password)
                result = User.find_one({"email" :email , "password" : password})

                #return jsonify({"ok":1})
                if result is not None:

                    fullname = result['firstname' ] +"  " +result['lastname']
                    session['cookiesUserid']    = int(result['userid'])
                    session['userValid']		= result['salt']
                    session['cookiesToken']		= str(result['token'])
                    session['city']		        = str(result['addressJSON']['city'])
                    session['userloginName']    = fullname
                    #session['location']         = str(result['locationid'])
                    session.permanent = True
                    print (session)
                    picPath = URL +imagePath
                    print (request.cookies)
                    response =userDataResponse(email)
                    return jsonify({"status": 200, "response": response, "message": "", "error": False})
                else:
                    return jsonify({'status' :201 ,"response": {}, 'message' : 'Invalid username and Password.',"error": False})
            else:
                return jsonify({'status' :202 ,"response": {}, 'message' : 'Invalid username.',"error": False})
        else:
            return jsonify({'status' :203,"response": {}, 'message' :"Email or Password not be null.","error": False})


    except Exception as e:
        print(e)
        return jsonify({"status" :500 ,"response": {},"message" :"email not verified or all field not set","error": True})
   
