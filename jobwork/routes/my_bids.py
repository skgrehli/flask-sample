from jobwork.middleware.authentication import authentication
from jobwork.models.jobs import Jobs
from jobwork.models.jobbids import JobBids
from flask import Blueprint,request,make_response,jsonify
from jobwork.models.conversations import Conversations

my_bids=Blueprint('my_bids',__name__,url_prefix='')

@my_bids.route('/mybids',methods=['POST'])
@authentication
def bids():
    data = []
    userid = int(request.json['userid'])
    type = int(request.json['type'])

    if (type == 0):
        typeKey = "$or"
        typeVal = [{"draft": True}, {"draft": False}]
    elif (type == 1):
        typeKey = "draft"
        typeVal = True
    elif (type == 2):
        typeKey = "draft"
        typeVal = False
    try:

        usersJob=list(JobBids.find({"userid":userid},{"_id":0}))
        count=0
        for df in usersJob:
            #return jsonify({"count": d["jobid"]})
            #jobbids=list(JobBids.find({"jobid":d["jobid"]},{"_id":0}))
            jobdraftdata = list(Jobs.find({"jobid":df["jobid"], typeKey: typeVal}, {"_id": 0}))
            if(len(jobdraftdata)!=0):
                count = count + 1
                for con in jobdraftdata:
                    convertations = list(Conversations.find({"userid1": userid, "userid2": con["creatinguserid"]}, {"_id": 0}))
                    con.update({"conversations": convertations})
                data.append({"job":jobdraftdata})
            #data["job"].update({"bid":jobbids})



        return jsonify({"status":200,"response":"ok","message":count,"data":data,"error":False})
    except Exception as e:
        print(e)
        return jsonify({"error":True,"response":[],"message":"unknown error","status":400})

