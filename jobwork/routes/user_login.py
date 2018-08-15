from flask import request,Blueprint,jsonify,session
from jobwork.models.user import User
import hashlib
from jobwork.constants import Constants
from jobwork.db_connection import db

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
            userdata = User.find_one({"email" :email ,"isadmin" :False ,"active" :True})
            #print (userdata)
            # if userData.count == 0 :
            # 	userdata = user.find_one({"signupJSON.mobile":int(email),"isadmin":False,"active":True})
            if userdata is not None:
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
                    session['location']         = str(result['locationid'])
                    session.permanent = True
                    print (session)
                    picPath = URL +imagePath
                    print (request.cookies)
                    userdata = list(db.user.aggregate([{"$match": {"email": email}},
                                                       {"$lookup": {"from": "country",
                                                                    "localField": "addressJSON.country",
                                                                    "foreignField": "countryid", "as": "countryname"}},
                                                       {"$lookup": {"from": "city", "localField": "addressJSON.city",
                                                                    "foreignField": "cityid", "as": "cityname"}},
                                                       {"$lookup": {"from": "state", "localField": "addressJSON.state",
                                                                    "foreignField": "stateid", "as": "statename"}},
                                                       {"$project": {"firstname": 1, "lastname": 1,
                                                                     "cityname.city": 1, "statename.state": 1,
                                                                     "picurl": 1, "userid": 1, "countryname.country": 1,
                                                                     "addressJSON.address1": 1,
                                                                     "addressJSON.address2": 1,
                                                                     "addressJSON.pincode": 1, "gender": 1,
                                                                     "registeredfrom": 1,"email":1,"token":1,"emailverified":1,

                                                                     "_id": 0}}]))

                    # user = list(User.find({"email": email}, {"_id": 0}))
                    return jsonify({"user": userdata})
                else:
                    return jsonify({'status' :201 ,"response": {}, 'message' : 'Invalid username and Password.',"error": False})
            else:
                return jsonify({'status' :202 ,"response": {}, 'message' : 'Invalid username.',"error": False})
        else:
            return jsonify({'status' :203,"response": {}, 'message' :"Email or Password not be null.","error": False})


    except Exception as e:
        print(e)
        return jsonify({"status" :500 ,"response": {},"message" :"email not verified or all field not field","error": False})
   
