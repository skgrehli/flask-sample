from flask import request, Blueprint, url_for, session, jsonify,render_template,redirect
from jobwork.models.city import CityCollections
from jobwork.models.locations import Locations
from jobwork.models.user import User
from datetime import datetime

get_route = Blueprint('get_route', __name__, url_prefix='')

@get_route.route('/')
def index():
    city = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}).sort('city' ,1))
    locationData = list(Locations.find({} ,{"_id" :0}).sort('locationname' ,1))
    return render_template("front_saveonjobs/index.html", cities=city ,location=locationData ,access_token="")

@get_route.route('/signout', methods=['POST'])
def signout():
    session.clear()
    return 'success'

@get_route.route('/mobile/signout', methods=['POST'])
def signout_mobile():

    userid = request.json['userid']
    session.clear()

    User.update({"userid": userid}, {"$set" :{"device_token": "", "version": "", "os": ""}})
    return 'success'

@get_route.route('/sessionSignout')
def sessionSignout():
    session.clear()
    # global preivousPath
    # print preivousPath
    return redirect("/")

@get_route.route('/findjobs')
def findjobs():
    city = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}).sort('city' ,1))
    locationData = list(Locations.find({} ,{"_id" :0}).sort('locationname' ,1))
    return render_template("front_saveonjobs/findjobs.html" ,cities=city ,location=locationData)

@get_route.route('/forgotpassword__<hashvalue>')
def forgotpasswordhash(hashvalue):
    userid = ""
    token = ""
    getuserdata = list(User.find({"$and" :[{"forgotpasswordJSON.forgotpasswordhash" : hashvalue}, {"forgotpasswordJSON.forgotpassworduseddatetime" :-1}]}, {"_id" :0}))

    if len(getuserdata) == 1:
        for userdata in getuserdata:
            forgotpassworduseddatetime = datetime.now()
            User.update({"userid" :userdata['userid'] ,"forgotpasswordJSON.forgotpasswordhash" : hashvalue}
                        ,{"$set" :{"forgotpasswordJSON.$.forgotpassworduseddatetime" : forgotpassworduseddatetime}})
            userid = userdata['userid']
            token = userdata['token']

        return render_template("front_saveonjobs/forgot_password.html", userid=userid, token=token)
    else:
        return jsonify({"status" :200 ,"message" :"URL not found."})

@get_route.route('/emailverify__<hashvalue>')
def emailverifyhash(hashvalue):
    getuserdata = User.find_one({"emailhash" : hashvalue, "emailverified" :False}, {"_id" :0})
    if getuserdata is not None:
        User.update({"emailhash" : hashvalue} ,{"$set" :{"emailverified" :True, "updateddatetime" : datetime.now()}})
        return render_template("front_saveonjobs/email_verify.html")
    else:
        return jsonify({"status" :200 ,"message" :"Email already Verified."})

@get_route.route('/jobrelated')
def jobrelated():
    return render_template("jobrelatedpopups.html")


def authenticatedUser():
    try:
        if 'cookiesUserid' in session and 'cookiesToken' in session:
            return True
        else:
            return False
    except:
        return unauthorizedUser()

def unauthorizedUser():
    session['next_url'] = request.path
    session.permanent = True
    return redirect("/sessionSignout")


@get_route.route('/account')
def account():
    if authenticatedUser():
        city = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}))
        locationData = list(Locations.find({} ,{"_id" :0}))
        return render_template("front_saveonjobs/loggedin_new.html" ,cities=city ,location=locationData)
    else:
        return unauthorizedUser()


@get_route.route('/profile')
def profile():
    if authenticatedUser():
        city = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}))
        locationData = list(Locations.find({} ,{"_id" :0}))
        return render_template("front_saveonjobs/profile.html" ,cities=city ,location=locationData)
    else:
        return unauthorizedUser()

@get_route.route('/mytask')
def mytask():
    if authenticatedUser():
        city = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}))
        locationData = list(Locations.find({} ,{"_id" :0}))
        return render_template("front_saveonjobs/my-tasks.html" ,cities=city ,location=locationData ,message='')
    else:
        return unauthorizedUser()

@get_route.route('/contact')
def contact():
    if authenticatedUser():
        city = list(CityCollections.find({} ,{"_id" :0 ,"cityid" :1 ,"city" :1}))
        locationData = list(Locations.find({} ,{"_id" :0}))
        return render_template("front_saveonjobs/contact.html" ,cities=city ,location=locationData)
    else:
        return unauthorizedUser()

@get_route.route('/howitworks')
def Howitworks():
    return render_template("front_saveonjobs/howitworks.html")

@get_route.route('/startupyoursmallbusiness')
def Startupyoursmallbusiness():
    return render_template("front_saveonjobs/Startup_your_small_business.html")

@get_route.route('/trustandquality')
def TrustandQuality():
    return render_template("front_saveonjobs/Trust&insurance.html")

@get_route.route('/howtoearnmoney')
def Howtoearnmoney():
    return render_template("front_saveonjobs/How_to_earn_money.html")

@get_route.route('/usefultips')
def Usefultips():
    return render_template("front_saveonjobs/Useful_tips.html")

@get_route.route('/faqs')
def FAQs():
    return render_template("front_saveonjobs/FAQs.html")

@get_route.route('/aboutus')
def AboutUs():
    return render_template("front_saveonjobs/About.html")

@get_route.route('/contactus')
def ContactUs():
    return render_template("front_saveonjobs/contactUs.html")

@get_route.route('/termsandconditions')
def TermsandConditions():
    return render_template("front_saveonjobs/terms&condition.html")

@get_route.route('/privacypolicy')
def PrivacyPolicy():
    return render_template("front_saveonjobs/Privacyp.html")

@get_route.route('/blog')
def Blog():
    return render_template("front_saveonjobs/terms&condition.html")

@get_route.route('/supportcenter')
def SupportCenter():
    return render_template("front_saveonjobs/Support_Center.html")

@get_route.route('/categorylisting')
def CategoryListing():
    return render_template("front_saveonjobs/category-listing.html")

# Location and City data



