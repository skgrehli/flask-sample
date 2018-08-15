'''
from flask import request,Blueprint,jsonify
from jobwork.models.user import User
from jobwork.middleware.authentication import authentication
from jobwork.utils.common_utils import CommonUtils
from jobwork.constants import Constants
from jobwork.models.messagetrack import MessageTracks
from twilio.rest import Client
from datetime import datetime

user_register=Blueprint('user_register',__name__,url_prefix='')

msgclient = Client(Constants.MSG_ACCOUNT_SID, Constants.MSG_AUTH_TOKEN)
msgtrckid = CommonUtils.generateRandomNo(MessageTracks, "messagetrackid")


@user_register.route('/user/register' ,methods=['POST'])
@authentication
def user_register():
    email = request.json['email']

    if email is not None:
        getemail = User.find({"signupJSON.email" :email}).count()
        if getemail == 0:
            if email == "":
                mobile =request.json['mobile']
                if mobile == "":
                    fbid = request.json['fbid']
                    fbaccesstoken = request.json['fbaccesstoken']
                else:
                    fbid = ""
                    fbaccesstoken = ""
                    mobileotp = CommonUtils.generateOTP()
                    sendText = "Mobile Verify OTP is  " +str(mobileotp)
                    message = msgclient.messages.create(body=sendText ,to=mobile ,from_=Constants.MSG_SEND_FROM)
                    print(message.sid)
                    MessageTracks.insert({"messagetrackid" :CommonUtils.generateRandomNo(MessageTracks ,"messagetrackid")
                                          ,"userid" :jobCollection['creatinguserid'] ,"mobile" :mobile
                                          ,"messagetext" :sendText ,"messagesid" :message.sid
                                          ,"createdatetime" :datetime.now() ,"updatedatetime" :datetime.now()})
            else:
                mobile = ""
                mobileotp = ""
                fbid = ""
                fbaccesstoken = ""
                # emailhash = send_email(email)
                emailhash = CommonUtils.getHashValue()

            firstname = request.json['firstname']
            lastname = request.json['lastname']
            usertype = request.json['usertype']
            city = int(request.json['city'])
            location = int(request.json['location'])

            fullname = firstname +"  " +lastname

            if firstname is not None and lastname is not None and usertype is not None and city is not None:

                salt = CommonUtils.generateRandomName()

                # random.randrange(1000, 9999)

                signupJSON = {	"email" : email,
                                  "mobile" : mobile,
                                  "fbid" : fbid,
                                  "fbaccesstoken" : fbaccesstoken
                                  }

                citydetail = citycollections.find_one({"cityid" :city} ,{"_id" :0})
                statedetail = statecollections.find_one({"stateid" :citydetail['stateid']} ,{"_id" :0})
                countrydetail = countrycollections.find_one({"countryid" :citydetail['countryid']} ,{"_id" :0})
                addressJSON = {"address1" : "",
                               "address2" : "",
                               "city" : city,
                               "state" : citydetail['stateid'],
                               "country" : countrydetail['countryid'],
                               "pincode" : ""
                               }

                proJSON = { "facebookapproved" : False,
                            "policeverification" : False,
                            "mobileverified" : False,
                            "creditcardverified" : False,
                            "professionalcertificationverified" : False,
                            "overallPro" : False
                            }

                paymentdetailsJSON = {	"bankname" : "",
                                          "bankaccountname" : "",
                                          "bankaccountnumber" : "",
                                          "banktransitnumber" : ""
                                          }

                if request.json['password'].strip() != "":
                    password = hashlib.md5(request.json['password'].strip()).hexdigest() + salt

                if request.json.has_key('userid') == False:
                    userid = generateRandomNo(user ,"userid")
                    if request.json.has_key('token') == False:
                        token = generateRandomName()
                        randomNameForFile = ""
                    # if request.json['imageFlag']:
                    # 	randomNameForFile = "image_"+str(int(time.time()))+".jpg"
                    # 	fh = open("static/images/"+randomNameForFile, "wb")
                    # 	fh.write(request.json['image'].decode('base64'))
                    # 	fh.close()

                    user.insert({	"userid" : userid,
                                     "signupJSON": signupJSON,
                                     "email": email,
                                     "emailverified": False,
                                     "emailhash": emailhash,
                                     "mobile": mobile,
                                     "mobileverified": False,
                                     "mobileotp": str(mobileotp),
                                     "isdcode" :None,
                                     "fbid": fbid,
                                     "fbaccesstoken": fbaccesstoken,
                                     "password": password,
                                     "salt": salt,
                                     "token": token,
                                     "usertype": usertype,
                                     "firstname": firstname,
                                     "lastname": lastname,
                                     "isadmin": False,
                                     "createddatetime": datetime.now(),
                                     "updateddatetime": datetime.now(),
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
                                     "dob" :"",
                                     "locationid": location,
                                     "aboutme": "",
                                     "picurl": "user-no-image.jpg",
                                     "reportedJSON": [],
                                     "notificationJSON": [],
                                     "socaillogin": False,
                                     "facebookpicurl": "",
                                     "active": True,
                                     "paypal_id" : ""
                                     })

                    session['cookiesUserid']    = int(userid)
                    session['userValid']		= str(salt)
                    session['cookiesToken']		= str(token)
                    session['city']		        = str(city)
                    session['userloginName']    = str(fullname)
                    session['location']         = str(location)
                    session.permanent = True
                    picPath = UR L +imagePath


                    notificationtext = "Hello  " +str(fullname ) +"  SaveOnJobs welcomes you !!"

                    registration_id = find_FCM_id(userid)
                    i f(registration_id):
                        data_message = {
                            "body" : notificationtext,
                        }

                        result = push_service.notify_single_device(registration_id=registration_id, message_title="Welcome!"
                                                                   ,message_body=notificationtext, data_message=data_message, click_action="FCM_PLUGIN_ACTIVITY")


                    notification = notifications.insert \
                        ({"notificationid" :generateRandomNo(notifications ,"notificationid"),
                                                         "notificationtext" :notificationtext,
                                                         "notificationtype" :"welcome",
                                                         "notificationtouserid" :int(userid),
                                                         "notificationfromuserid" :-1,
                                                         "jobid" :-1,
                                                         "bidid" :-1,
                                                         "commentid" :-1,
                                                         "createddatetime" :datetime.now(),
                                                         "updatedatetime" :datetime.now(),
                                                         "isread" :False
                                                         })

                    # Send email verification

                    reset_password_link = str(URL ) +"emailverify__ " +str(emailhash)

                    subject = "Your SAVEonJOBS.comAccount Email Verification"
                    msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[email])
                    msg.html = render_template('/emailTemplates/email_verification_template.html', name= firstname, resetLink= reset_password_link ,email=email)
                    mail.send(msg)
                    emailtracks.insert({"emailtrackid": generateRandomNo(emailtracks, "emailtrackid"), "userid": userid,
                                        "email": email, "subject": subject, "emailtext": msg.html,
                                        "createdatetime": datetime.now(), "updatedatetime": datetime.now()})

                    # Mobile Verify OTP
                    if mobile != "":
                        sendText = "Mobile Verify OTP is " + str(mobileotp)
                        message = msgclient.messages.create(body=sendText, to=mobile, from_=sendFrom)
                        print(message.sid)
                        messagetracks.insert(
                            {"messagetrackid": generateRandomNo(messagetracks, "messagetrackid"), "userid": userid,
                             "mobile": mobile, "messagetext": sendText, "messagesid": message.sid,
                             "createdatetime": datetime.now(), "updatedatetime": datetime.now()})

                return jsonify({'status': 200, 'message': 'Successfull Register', 'userid': userid,
                                'token': token,
                                'city': city,
                                'location': location,
                                "firstname": firstname,
                                "lastname": lastname,
                                "picurl": "user-no-image.jpg",
                                "picPath": picPath})
            else:
                return jsonify({'status': 202, 'message': 'Data can not be null.'})
        else:
            return jsonify({'status': 201, 'message': 'Email already exits.'})
    else:
        return jsonify({'status': 202, 'message': 'Data can not be null.'})'''


