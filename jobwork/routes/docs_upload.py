import os
from flask import Flask, request, redirect, url_for,Blueprint,jsonify,render_template
from werkzeug.utils import secure_filename
from jobwork.constants import Constants
from PIL import Image
from datetime import datetime,timedelta
from jobwork.models.jobs import Jobs
from jobwork.models.city import CityCollections
from jobwork.models.state import StateCollections
from jobwork.models.country import CountryCollections
#from jobwork.middleware.authentication import authentication
from jobwork.utils.common_utils import CommonUtils
from jobwork.models.user import User

UPLOAD_FOLDER = '/static/jobdocument/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#APP_ROOT=os.path.dirname(os.path.abspath(__file__))

upload_doc=Blueprint('upload',__name__,url_prefix='')


@upload_doc.route('/upload')
def uploader():
    return render_template('addjob.html')



@upload_doc.route('/upload/file', methods=["GET",'POST'])
def upload_file():
    target=os.path.join(Constants.APP_ROOT,'static/jobdocument/original')
    if request.method == 'POST':
        #file = request.files['file']
        index=0
        userid=request.form['userid']
        #token=request.form['token']
        jobtitle=request.form['jobtitle']
        jobdescription=request.form['description']
        personseleted=request.form['personselected']
        totalbudget=request.form['totalbudget']
        budgettype=request.form['budgettype']
        cityid=request.form['cityid']
        locationid=request.form['locationid']
        draft=request.form['draft']
        date=request.form['date']

        print(jobtitle)
        filelist=[]
        thumblist=[]
        for file in request.files.getlist("file"):

            print(file)
           # f.save(secure_filename(f.filename))
            #filename = secure_filename(file.filename)
            try:

                filename=jobtitle+".jpg"
                destination="/".join([target,filename])
                file.save(destination)
                index=index+1
                im =Image.open(file)
                size=45,45
                im.thumbnail(size,Image.ANTIALIAS)
                background = Image.new('RGBA', size, (255, 255, 255, 0))
                background.paste(
                    im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2))
                )
                tname="static/jobdocument/thumbnail/"+jobtitle+ ".png"
                background.save(tname)
                thumblist.append(tname)

            except Exception as e:
                destination = "/".join([target, file.filename])
                file.save(destination)

            filelist.append(destination)
        return jsonify({"status": 200, "path": filelist})

@upload_doc.route('/add/new/job', methods=["GET",'POST'])
def jobadd():
    if request.method == 'POST':

        try:
            #return "ok"
            # Check authentications keys
            '''
            if request.form['userid'] == "" or request.form['token'] =="":
                
                return jsonify({"status": 401, "message": "Authentication keys are missing."})
            '''
            userid = request.form['userid']
            #return userid
            token = request.form['token']

            # Authenticate credentials
            userInfo = User.find_one({"userid": int(userid)}, {"_id": 0})
            if userInfo is not None:
                if userInfo['emailverified'] is False:
                    return jsonify(
                        {"status": 202, "message": "Email not verified. Please verify your email to enable this feature"})

            jobid = request.form['jobid']

            originaljobid = None
            if (jobid != ""):
                originaljobid = jobid
            draft = request.form['draft']

            title = request.form['title']

            description = request.form['description']

            duedate = request.form['duedate']
            #return jsonify({"ok": 1})

            jobOnline = request.form['jobonline']
            #return "ok"
            print("1")
            city = int(request.form['city'])
            print("2")
            location = int(request.form['location'])
            print("3")
            if duedate == "today":
                duedate = ""
                duedate = datetime.now()
            if duedate == "week":
                duedate = ""
                duedate = datetime.now() + timedelta(days=7)
            if duedate == "certain_day":
                duedate = ""
                format = '%d-%m-%Y %H:%M:%S'
                certaindatetime = request.form['certaindatetime']
                duedate = datetime.strptime(certaindatetime, format)

            citydetail = CityCollections.find_one({"cityid": city}, {"_id": 0})
            statedetail = StateCollections.find_one({"stateid": citydetail['stateid']}, {"_id": 0})
            countrydetail = CountryCollections.find_one({"countryid": citydetail['countryid']}, {"_id": 0})
            addressJSON = {"address1": "",
                           "address2": "",
                           "city": city,
                           "state": citydetail['stateid'],
                           "country": countrydetail['countryid'],
                           "pincode": ""
                           }

            person = request.form['person']
            print("5")
            budgettype = request.form['budgettype']
            print("6")
            budget = float(request.form['budget'])
            print("7")
            if budgettype == "hourly":
                totalhours = int(request.form['hours'])
                totalbudget = int(budget * totalhours)
            else:
                totalhours = -1
                totalbudget = budget
            print("8")
            if draft == False:
                publisheddatetime = datetime.now()
            else:
                publisheddatetime = None

            target = os.path.join(Constants.APP_ROOT, 'static/jobdocument/')
            index = 0
            filelist = []
            thumblist = []
            print("9")
            jobidno = CommonUtils.generateRandomNo(Jobs, "jobid")

            for file in request.files.getlist("file"):
                index = index + 1
                try:

                    filename = str(jobidno)+"_"+str(index) + ".jpg"
                    destination = "original/".join([target, filename])
                    file.save(destination)
                    im = Image.open(file)
                    size = 45, 45
                    im.thumbnail(size, Image.ANTIALIAS)
                    background = Image.new('RGBA', size, (255, 255, 255, 0))
                    background.paste(
                        im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2))
                    )
                    tname = target+"/thumbnail/" +str(jobidno)+"_"+str(index) + ".png"
                    background.save(tname)
                    thumblist.append(tname)

                except Exception as e:
                    fname=str(jobidno)+"_"+str(index)+file.filename
                    destination = "original/".join([target,fname ])
                    file.save(destination)
                    tname = target + "/thumbnail/pdf.png"
                    thumblist.append(tname)

                #thumblist.append(tpath)

                filelist.append(destination)


            #return jsonify({"t":thumblist,"l":filelist})
            print("10")
            jobdocs={}
            jobdocs.update({"thumbnails":thumblist})
            jobdocs.update({"doc":filelist})
            print("11")
            if (request.form['draft_data'] == "false"):
                jobid = jobidno
                result = Jobs.insert({"jobid": jobid,
                                      "title": title,
                                      "description": description,
                                      "creatinguserid": userid,
                                      "duedate": duedate,
                                      "budget": budget,
                                      "budgettype": budgettype,
                                      "totalbudget": totalbudget,
                                      "totalhours": totalhours,
                                      "jobstatus": "pending",
                                      "draft": draft,
                                      "publisheddatetime": publisheddatetime,
                                      "personsrequired": int(person),
                                      "reportedJSON": [],
                                      "active": True,
                                      "cancellationreason": None,
                                      "cityid": city,
                                      "online": jobOnline,
                                      "addressJSON": addressJSON,
                                      "locationid": location,
                                      "personsselected": 0,
                                      "originaljobid": originaljobid,
                                      "adminapprovalforcancellation": None,
                                      "skillid": None,
                                      "tags": None,
                                      "jobdocs":jobdocs,
                                      "updatedatetime": datetime.now(),
                                      "createdatetime": datetime.now(),
                                      "expired": False
                                      })
                return jsonify({'status': 200, 'message': 'Job Created.', 'jobid': jobid})
            else:
                Jobs.update({"jobid": jobid}, {"$set": {"title": title,
                                                        "description": description,
                                                        "creatinguserid": userid,
                                                        "duedate": duedate,
                                                        "budget": budget,
                                                        "budgettype": budgettype,
                                                        "totalbudget": totalbudget,
                                                        "totalhours": totalhours,
                                                        "jobstatus": "pending",
                                                        "draft": draft,
                                                        "publisheddatetime": publisheddatetime,
                                                        "personsrequired": int(person),
                                                        "reportedJSON": [],
                                                        "active": True,
                                                        "cancellationreason": None,
                                                        "cityid": city,
                                                        "online": jobOnline,
                                                        "addressJSON": addressJSON,
                                                        "locationid": location,
                                                        "personsselected": 0,
                                                        "originaljobid": originaljobid,
                                                        "adminapprovalforcancellation": None,
                                                        "skillid": None,
                                                        "tags": None,
                                                        "jobdocs":jobdocs,
                                                        "updatedatetime": datetime.now(),
                                                        "expired": False}})
                return jsonify({'status': 200, 'message': 'Job Updated.', 'jobid': jobid})

        except Exception as e:
            print(e)
            return "error"




