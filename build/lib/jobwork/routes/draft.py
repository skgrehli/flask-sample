from jobwork.middleware.authentication import authentication
from jobwork.models.jobs import Jobs
from jobwork.models.jobbids import JobBids
from flask import Blueprint,request,make_response,jsonify
from jobwork.models.conversations import Conversations
from jobwork.db_connection import db
from bson import json_util, ObjectId
import json

draft_job=Blueprint('draft_job',__name__,url_prefix='')

@draft_job.route('/myjobs',methods=['POST'])
@authentication
def draft():
    data=[]
    userid = int(request.json['userid'])
    type = int(request.json['type'])
    expire = int(request.json['expire'])
    active = int(request.json['active'])

    if (expire == 1):
        expKey = "expired"
        expVal = True

    elif (expire == 0):
        expKey = "expired"
        expVal = False
    elif (expire == 2):
        expKey = "$or"
        expVal = [{"expired":True},{"expired":False}]

    if (active == 1):
        actKey = "active"
        actVal = True

    elif (active == 0):
        actKey = "active"
        actVal = False

    elif (active == 2):
        actKey = "$or"
        actVal = [{"expired":True},{"expired":False}]

    if(type==0):
        typeKey="$or"
        typeVal=[{"draft":True},{"draft":False}]
    elif(type==1):
        typeKey="draft"
        typeVal=True
    elif(type==2):
        typeKey="draft"
        typeVal=False

    try:

        jobdraftdata=list( db.jobs.aggregate([{"$match":{"creatinguserid":userid,typeKey:typeVal,actKey:actVal,expKey:expVal}},
        {"$lookup":{"from":"city","localField":"addressJSON.city","foreignField":"cityid","as":"cityname"}},
        {"$lookup":{"from":"state","localField":"addressJSON.state","foreignField":"stateid","as":"statename"}},
        {"$lookup":{"from":"user","localField":"creatinguserid","foreignField":"userid","as":"user"}},
        {"$project":{"cityname.city":1,"title":1,"duedate":1,"statename.state":1,"jobid":1,"user.picurl":1,"budget":1,"_id":0}}]))
        #jobdraftdata=list(Jobs.find({"creatinguserid":userid,typeKey:typeVal},{"_id":0}))
        count=0
        for d in jobdraftdata:
            #return jsonify({"count": d["jobid"]})
            jobcomment=list(db.jobcomments.find({"jobid":d["jobid"]},{"_id":0,"comment":1}))
            jobbids=list(db.jobbids.aggregate([{"$match":{"jobid":d["jobid"]}},
            {"$lookup":{"from":"user","localField":"userid","foreignField":"userid","as":"users"}},
            {"$lookup": {"from": "city", "localField": "addressJSON.city","foreignField": "cityid", "as": "cityname"}},
            {"$lookup":{"from":"state","localField":"addressJSON.state","foreignField":"stateid","as":"statename"}},
            {"$project":{"users.firstname":1,"users.lastname":1,"cityname.city":1,"statename.state":1,"users.picurl":1,"budget":1,"userid":1,"_id":0}}]))
            #jobbids=list(JobBids.find({"jobid":d["jobid"]},{"_id":0}))
            for con in jobbids:
                convertations=list(Conversations.find({"userid1":userid,"userid2":con["userid"]},{"_id":0}))

                con.update({"conversations": convertations})


            d.update({"bids":jobbids})
            d.update({"comments":jobcomment})
            data.append(d)
            #data["job"].update({"bid":jobbids})
            count=count+1
        if jobdraftdata is None:
            return jsonify({"data": "empty"})
        else:
            #return jsonify({"count":count,"data":data})
            return json.dumps(data, indent=4, default=json_util.default)
    except Exception as e:
        print(e)
        return jsonify({"data":"error"})

@draft_job.route('/deletejobs',methods=['POST'])
@authentication
def jobdelete():

    jobid = int(request.json['jobid'])
    try:
        db.jobs.remove({"jobid":jobid})
        return jsonify({"status":"done"})
    except Exception as e:
        print(e)
        return jsonify({"status":"error"})