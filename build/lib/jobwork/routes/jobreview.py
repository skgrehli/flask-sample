from flask import Blueprint,request,make_response,jsonify,render_template
from jobwork.middleware.authentication import authentication
from jobwork.models.jobbids import JobBids
from jobwork.models.jobreviews import JobReviews
from jobwork.models.jobs import Jobs
from jobwork.utils.common_utils import CommonUtils
from jobwork.models.user import User
from flask_mail import Mail, Message
from jobwork.models.emailtrack import EmailTracks

job_review=Blueprint('job_review',__name__,url_prefix='')
from datetime import datetime

@job_review.route('/user/job/review', methods=['POST'])
def user_job_review():
    # Check authentications keys
    userid = int(request.json['userid'])
    token = request.json['token']


    if request.json['bidderJobStatus'] == "verify":
        check_status = JobBids.find \
            ({"jobid" :int(request.json['jobid']) ,"userid" :int(request.json['touserid']) ,"active" :True
             ,"status" : "completed"}).count()
    elif request.json['bidderJobStatus'] == "completed":
        check_status = JobBids.find({"jobid" :int(request.json['jobid']) ,"userid" :userid ,"active" :True
                                     ,"status" : { "$in" : ["selectedbyjobber" ,"approvedbybidder"]}}).count()

    print (check_status)
    if check_status == 1 :

        if request.json['bidderJobStatus'] == "verify":
            bidid = 0
            jobbids_info = JobBids.find_one \
                ({"userid" :int(request.json['touserid']) ,"jobid" :int(request.json['jobid'])} ,{"_id" :0})
            if jobbids_info is not None:
                bidid = jobbids_info['bidid']

        jobReviewsDataCount = JobReviews.find({"userid" : userid ,"jobid" : int(request.json['jobid'])}).count()
        jobCollection = list(Jobs.find({"jobid" :int(request.json['jobid'])}))

        # print jobBidsData['bidid']
        if jobReviewsDataCount == 0:
            jobreviewData = JobReviews.insert({	"userid" : userid,
                                                   "reviewid" : CommonUtils.generateRandomNo(JobReviews ,"reviewid"),
                                                   "jobid" : int(request.json['jobid']),
                                                   "rating" : int(request.json['rating']),
                                                   "comment" : request.json['comment'],
                                                   "touserid" : int(request.json['touserid']),
                                                   "adminaction" : False,
                                                   "active" : True,
                                                   "createdatetime" : datetime.now(),
                                                   "updatedatetime" : datetime.now()
                                                   })

            if request.json['bidderJobStatus'] == "verify":

                jobCollection = Jobs.find_one({"jobid" :int(request.json['jobid'])} ,{"_id" :0})
                if jobCollection is not None:
                    total_paid_task = JobBids.find({"jobid" : int(request.json['jobid']) ,"completionstatus": { "$in" : ["accepted" ,"rejectedaccepted"] }}).count()
                    if total_paid_task != 0:
                        if ( total_paid_task >=  jobCollection['personsrequired']):
                            Jobs.update({"jobid" :int(request.json['jobid'])} ,{"$set" :{
                                "jobstatus" :"paid"
                            }})

                jobBidsData = JobBids.find_one \
                    ({"userid" : int(request.json['touserid']) ,"jobid" : int(request.json['jobid'])} ,{"_id" :0})
                JobBids.update({"bidid" :int(jobBidsData['bidid'])}
                               ,{"$set" : {"status" : "verify" ,"completionstatus" :"accepted"}})

                jobCollection = Jobs.find_one({"jobid" :int(request.json['jobid'])} ,{"_id" :0})
                if jobCollection is not None:
                    userJobberCollection = user.find_one({"userid" :jobCollection['creatinguserid']} ,{"_id" :0})
                    if userJobberCollection is not None:
                        jobberfullname = userJobberCollection['firstname' ] +"  " +userJobberCollection['lastname']
                        jobberEmail = userJobberCollection['email']
                        jobberMobile = userJobberCollection['mobile']
                    else:
                        jobberfullname = ""
                        jobberEmail = None
                        jobberMobile = None
                    userbidderCollection = User.find_one({"userid" :int(request.json['touserid'])} ,{"_id" :0})
                    if userbidderCollection is not None:
                        bidderfullname = userbidderCollection['firstname' ] +"  " +userbidderCollection['lastname']
                        bidderEmail = userbidderCollection['email']
                        bidderMobile = userbidderCollection['mobile']
                    else:
                        bidderfullname = ""
                        bidderEmail = None
                        bidderMobile = None
                else:
                    print ("No jobs")

                if bidderEmail is not None:

                    subject = "Payment released."
                    msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[bidderEmail])
                    msg.html = render_template('/emailTemplates/Payment-released.html', name= bidderfullname, title= str(jobCollection['title']) ,jobber=jobberfullname)
                    Mail.send(msg)
                    EmailTracks.insert({"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"),
                                        "userid": int(request.json['touserid']), "email": bidderEmail,
                                        "subject": subject, "emailtext": msg.html, "createdatetime": datetime.now(),
                                        "updatedatetime": datetime.now()})


                else:
                    print("No email of jobber.")


            else:
                jobBidsData = JobBids.find_one({"userid": userid, "jobid": int(request.json['jobid'])}, {"_id": 0})
                JobBids.update({"bidid": int(jobBidsData['bidid'])}, {"$set": {"status": "completed"}})
                jobCollection = Jobs.find_one({"jobid": int(request.json['jobid'])}, {"_id": 0})
                if jobCollection is not None:
                    total_completed_task = JobBids.find(
                        {"jobid": int(request.json['jobid']), "status": "completed"}).count()
                    print
                    total_completed_task
                    if total_completed_task != 0:
                        if (total_completed_task >= jobCollection['personsrequired']):
                            Jobs.update({"jobid": int(request.json['jobid'])}, {"$set": {
                                "jobstatus": "completed"
                            }})

            updateJobBids = list(JobBids.find({"bidid": int(jobBidsData['bidid'])}, {"_id": 0}))
            return jsonify({"status": 200, "message": "Review Created.", "updateJobBids": updateJobBids})
        else:
            updateJobBids = list(
                JobBids.find({"jobid": int(request.json['jobid']), "userid": userid, "active": True}, {"_id": 0}))
            return jsonify({"status": 200, "message": "Review Data.", "updateJobBids": updateJobBids})

    else:
        updateJobBids = list(
            JobBids.find({"jobid": int(request.json['jobid']), "userid": userid, "active": True}, {"_id": 0}))
        return jsonify({"status": 200, "message": "this bid is not present", "updateJobBids": updateJobBids})
