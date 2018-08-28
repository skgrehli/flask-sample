from jobwork.models.user import User
from jobwork.models.jobbids import JobBids
from flask import request,Blueprint,jsonify
from jobwork.middleware import authentication
from jobwork.models.jobs import Jobs
from jobwork.utils.common_utils import CommonUtils
from datetime import datetime
from jobwork.models.notification import Notifications
from jobwork.models.ledger import Ledgers
job_bid=Blueprint('job_bid',__name__,url_prefix='')

@job_bid.route('/job/bid/create/reversebid', methods=['POST'])

def job_bid_create():
    userid=request.json['userid']
    userInfo = User.find_one({"userid": int(userid)}, {"_id": 0})
    if userInfo is not None:
        if userInfo['emailverified'] is False:
            return jsonify({"status": 202, "message": "Email not verified. Please verify your email to bid"})

    jobCollection = Jobs.find_one({"jobid": int(request.json['jobid']), "active": True}, {"_id": 0})
    #if jobCollection['personsselected'] >= jobCollection['personsrequired']:
     #   return jsonify({"status": 203, "message": "Jobber's requirement has already been fulfilled"})

    jobberUser = User.find_one({"userid": jobCollection['creatinguserid']}, {"_id": 0})
    userCollection = User.find_one({"userid": userid}, {"_id": 0})
    if userCollection is not None:
        fullname = userCollection['firstname'] + " " + userCollection['lastname']
        bidderEmail = userCollection['email']
    else:
        fullname = ""
        bidderEmail = None
    if jobberUser is not None:
        jobberfullname = jobberUser['firstname'] + " " + jobberUser['lastname']
        jobberEmail = jobberUser['email']
    else:
        jobberfullname = None
        jobberEmail = None

    if jobCollection is not None:
        if request.json['bidid'] == "":

            check_status = JobBids.find({"jobid": int(request.json['jobid']), "userid": userid, "active": True},
                                        {"_id": 0})

            if check_status.count() == 0:

                reverseBidData = {"reversebidamount": None, "reversebiddatetime": None}
                bidid = CommonUtils.generateRandomNo(JobBids, "bidid")
                JobBids.insert({"jobid": int(request.json['jobid']),
                                "bidid": bidid,
                                "userid": userid,
                                "selected": False,
                                "bidamount": float(request.json['bidamount']),
                                "finalbidamount": None,
                                "bidcomment": request.json['bidcomment'],
                                "createdatetime": datetime.now(),
                                "bidcanceldatetime": "",
                                "bidcancellationreason": "",
                                "status": "pending",
                                "reversebid": reverseBidData,
                                "completionstatus": "pending",
                                "completionremarks": "",
                                "active": True})
                notificationtext = "Your job title " + jobCollection['title'] + " is bid by : " + fullname

                '''registration_id = find_FCM_id(jobCollection['creatinguserid'])
                if (registration_id):
                    data_message = {
                        "body": notificationtext,
                    }

                    result = push_service.notify_single_device(registration_id=registration_id, message_title="New Bid",
                                                               message_body=notificationtext, data_message=data_message,
                                                               click_action="FCM_PLUGIN_ACTIVITY")'''

                Notifications.insert({"notificationid": CommonUtils.generateRandomNo(Notifications, "notificationid"),

                                      "notificationtext": notificationtext,
                                      "notificationtype": "Bid",
                                      "notificationtouserid": int(jobCollection['creatinguserid']),
                                      "notificationfromuserid": userid,
                                      "jobid": jobCollection['jobid'],
                                      "bidid": bidid,
                                      "commentid": -1,
                                      "createddatetime": datetime.now(),
                                      "updatedatetime": datetime.now(),
                                      "isread": False
                                      })
                '''
                # Sending Email
                if jobberEmail is not None:
                    subject = "Bid Created."

                    msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[jobberEmail])
                    msg.html = render_template('/emailTemplates/bid-receive.html', name=jobberfullname,
                                               title=str(jobCollection['title']), bidder=fullname,
                                               amount=int(request.json['bidamount']))
                    mail.send(msg)
                    emailtracks.insert({"emailtrackid": generateRandomNo(emailtracks, "emailtrackid"),
                                        "userid": int(jobCollection['creatinguserid']), "email": jobberEmail,
                                        "subject": subject, "emailtext": msg.html, "createdatetime": datetime.now(),
                                        "updatedatetime": datetime.now()})
                else:
                    print
                    "No email of jobber."  '''

                new_bid = list(JobBids.find({"bidid": bidid}, {"_id": 0}))
                return jsonify({"status": 200, "message": "Successfully created.", "bidUpdate": new_bid})

            else:
                new_bid = list(JobBids.find({"bidid": check_status['bidid']}, {"_id": 0}))
                return jsonify({"status": 200, "message": "bid status intercepted.", "bidUpdate": new_bid})
        else:

            job_bid_detail = JobBids.find_one({"bidid": int(request.json['bidid'])}, {"_id": 0})
            if job_bid_detail is not None:

                if job_bid_detail['status'] == 'pending':

                    finalbidamount = float(request.json['reversebid'])
                    # updating bidamount array and reverse bid array
                    reverseBidData = {"reversebidamount": request.json['reversebid'],
                                      "reversebiddatetime": datetime.now()}

                    JobBids.update({"bidid": int(request.json['bidid'])}, {"$set": {"status": "reversebid",
                                                                                    "bidcomment": request.json[
                                                                                        'bidcomment'],
                                                                                    "reversebid": reverseBidData,
                                                                                    "finalbidamount": finalbidamount
                                                                                    }})

                    commission = float(finalbidamount * 0.1)

                    finalbidamount = float(finalbidamount - commission)

                    Ledgers.insert({"userid": userid,
                                    "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
                                    "amount": float(finalbidamount),
                                    "datetime": datetime.now(),
                                    "type": "escrow",
                                    "jobid": int(jobCollection['jobid']),
                                    "paymentdetailsJSON": "",
                                    "refundinitateddatetime": "",
                                    "refunddetailsJSON": "",
                                    "refundcompletiondatetime": "",
                                    "payingdatetime": "",
                                    "remark": "",
                                    "active": True})

                    Ledgers.insert({"userid": userid,
                                    "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
                                    "amount": float(commission),
                                    "datetime": datetime.now(),
                                    "type": "commission",
                                    "jobid": int(jobCollection['jobid']),
                                    "paymentdetailsJSON": datetime.now(),
                                    "refundinitateddatetime": "",
                                    "refunddetailsJSON": "",
                                    "refundcompletiondatetime": "",
                                    "active": True})

                    notificationtext = "Jobber reverse bid on the job title " + jobCollection[
                        'title'] + " for bidder : " + fullname

                    '''registration_id = find_FCM_id(job_bid_detail['userid'])
                    if (registration_id):
                        data_message = {
                            "body": notificationtext,
                        }

                        result = push_service.notify_single_device(registration_id=registration_id,
                                                                   message_title="Reverse Bid",
                                                                   message_body=notificationtext,
                                                                   data_message=data_message,
                                                                   click_action="FCM_PLUGIN_ACTIVITY")'''

                    Notifications.insert({"notificationid": CommonUtils.generateRandomNo(Notifications, "notificationid"),
                                          "notificationtext": notificationtext,
                                          "notificationtype": "Bid",
                                          "notificationtouserid": int(job_bid_detail['userid']),
                                          "notificationfromuserid": userid,
                                          "jobid": jobCollection['jobid'],
                                          "bidid": int(request.json['bidid']),
                                          "commentid": -1,
                                          "createddatetime": datetime.now(),
                                          "updatedatetime": datetime.now(),
                                          "isread": False
                                          })
                    '''
                    if bidderEmail is not None:

                        subject = "Reverse Bid on Job."
                        msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"),
                                      recipients=[bidderEmail])
                        msg.html = render_template('/emailTemplates/reverse-bid.html', name=bidderfullname,
                                                   title=jobCollection['title'], jobber=jobberfullname,
                                                   amount=int(request.form['payment']))
                        mail.send(msg)
                        emailtracks.insert({"emailtrackid": generateRandomNo(emailtracks, "emailtrackid"),
                                            "userid": finalBid['userid'], "email": bidderEmail, "subject": subject,
                                            "emailtext": msg.html, "createdatetime": datetime.now(),
                                            "updatedatetime": datetime.now()})

                    else:
                        print
                        "No email of bidder."
                    '''
                    update_bid = list(JobBids.find({"bidid": int(request.json['bidid'])}, {"_id": 0}))
                    return jsonify({"status": 200, "message": "Bid Successfully set.", "bidUpdate": update_bid})

                else:
                    update_bid = list(JobBids.find({"bidid": int(request.json['bidid'])}, {"_id": 0}))
                    return jsonify({"status": 200, "message": "status intercepted.", "bidUpdate": update_bid})
            else:
                return jsonify({"status": 200, "message": "Bid not found.", "bidUpdate": []})

    else:
        return jsonify({"status": 402, "message": "Job Not Found.", "bidUpdate": []})


