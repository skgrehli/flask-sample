from flask import jsonify,request,render_template,Blueprint
from paypalrestsdk import Payment, ResourceNotFound, Sale, Refund
from jobwork.middleware.authentication import authentication
from jobwork.models.transactiontrack import TransactionTrack
from datetime import datetime
from jobwork.models.jobbids import JobBids
from jobwork.models.jobs import Jobs
from jobwork.models.user import User
from jobwork.models.ledger import Ledgers
from jobwork.utils.common_utils import CommonUtils
from pyfcm import FCMNotification
from jobwork.models.notification import Notifications
from flask_mail import Mail,Message
from jobwork.models.emailtrack import EmailTracks
from jobwork.constants import Constants
from twilio.rest import Client
from jobwork.models.messagetrack import MessageTracks

push_service = FCMNotification(api_key="AAAAtudwsIM:APA91bHK-EizhjQr8D1p60liGYW6glt1y9Y5_OIfELjCnyrJm33kFLjQ0cdVwmyh3z2-6NwUo8nxORgQBe3WfNi-0U_CXHHt1Msq93R4QBsvgwvRpjzmU2gxOKwTI9LdU4VYkMlOFbMm")

def find_FCM_id(userid):
	try:
		result = User.find_one({"userid": int(userid)})
		if "device_token" in result:
			return result['device_token']
		else:
			return False
	except Exception as e:
		raise e

jw_paypal_web=Blueprint('jw_paypal_web',__name__,url_prefix='')


msgclient = Client(Constants.MSG_ACCOUNT_SID, Constants.MSG_AUTH_TOKEN)
msgtrckid = CommonUtils.generateRandomNo(MessageTracks, "messagetrackid")


@jw_paypal_web.route('/paypal_payment_test', methods=['GET'])
def test_paypal_payment():
    message = msgclient.messages.create(body="sendText" ,to="+918053023007" ,from_=Constants.MSG_SEND_FROM)

@jw_paypal_web.route('/paypal_payment_web', methods=['POST'])
def job_paypal_payment():
    try :
        if request.json.has_key('userid') == False or request.json.has_key('token') == False:
            return jsonify({ "status" :401 ,"message" :"Authentication keys are missing." })

        userid = int(request.json['userid'])
        token = request.json['token']

        # Authenticate credentials
        if authentication(userid ,token) ==  False:
            return jsonify({"status" :400 ,"message" :"Authentication Failed."})

        pay_id = request.json['payid']
        print (pay_id)

        payment = Payment.find(pay_id)
        print (payment)

        transactions = []
        transaction_amount = {}
        credit_card = {}
        sales_id = 0
        soj_transaction_id = 0
        transactionstatus = ""
        for transaction_details in payment.transactions:
            transaction_amount = {"currency" :transaction_details.amount.currency
                                  ,"total" :transaction_details.amount.total}
            sales_link = transaction_details['related_resources'][0]['sale']['links'][0]['href']
            sales_list = sales_link.split('sale')[1]
            sales_id = sales_list.split('/')[1]
            soj_transaction_id = int(transaction_details.custom)
            transactionstatus = transaction_details.state
        transactions.append(transaction_amount)
        payment_details = {"payment" :payment.id ,"sales_id" :sales_id ,"paymenttype" :payment.payer.payment_method
                           ,"state" :payment.state ,"transaction_details" :transactions}


        if (payment.state == "approved"):

            print (soj_transaction_id)
            TransactionTrack.update({
                "transactionid" : soj_transaction_id} ,{"$set" :{
                "transactionstatus" : transactionstatus,
                "transactionresponse" : payment_details,
                "responsedatetime" : datetime.now()}})

            transactions_details_from_database = TransactionTrack.find_one({"transactionid" :soj_transaction_id}
                                                                           ,{"_id" :0})
            print (transactions_details_from_database)
            bidid = transactions_details_from_database['jobbid']
            jobid = transactions_details_from_database['jobid']

            finalBid = JobBids.find_one({"bidid" : int(bidid)} ,{"_id" :0})

            completionremarks = ""
            completionstatus = ""
            bidcanceldatetime = ""
            bidcancellationreason = ""
            bidselected = False

            if finalBid is not None:

                jobCollection = Jobs.find_one({"jobid" :finalBid['jobid']} ,{"_id" :0})
                if jobCollection is not None:

                    person_selected = jobCollection['personsselected']
                    if person_selected is None :
                        person_selected = 0
                    else:
                        person_selected = int(person_selected)

                    userJobberCollection = User.find_one({"userid" :jobCollection['creatinguserid']} ,{"_id" :0})
                    if userJobberCollection is not None:
                        jobberfullname = userJobberCollection['firstname' ] +"  " +userJobberCollection['lastname']
                        jobberEmail = userJobberCollection['email']
                        jobberMobile = userJobberCollection['mobile']
                    else:
                        jobberfullname = ""
                        jobberEmail = None
                        jobberMobile = None
                    userbidderCollection = User.find_one({"userid" :finalBid['userid']} ,{"_id" :0})
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
                if request.json['status'] == "selectedbyjobber" :
                    if finalBid['status'] == "pending":
                        print (transaction_amount)
                        JobBids.update({"bidid" :int(bidid)} ,{ "$set" : {
                            "selected" : True,
                            "finalbidamount" : int(float(transaction_amount['total'])),
                            "bidcanceldatetime" : bidcanceldatetime,
                            "bidcancellationreason" : bidcancellationreason,
                            "status" : "selectedbyjobber",
                            "completionstatus" : "pending",
                            "completionremarks" : completionremarks
                        }})

                        if (jobCollection['personsrequired'] > person_selected ):
                            if (jobCollection['personsrequired'] == person_selected +1 ):
                                Jobs.update({"jobid" :int(jobid)} ,{"$set" :{
                                    "personsselected" : int(person_selected +1),
                                    "jobstatus" : "allotted"
                                }})
                            else:
                                Jobs.update({"jobid" :int(jobid)} ,{"$set" :{
                                    "personsselected" : int(person_selected +1)
                                }})


                        Totalbidamount = float(finalBid['bidamount'])

                        commission = float(Totalbidamount * 0.1)

                        finalbidamount = float(Totalbidamount - commission)

                        Ledgers.insert({"userid" : userid,
                                        "ledgerid" : CommonUtils.generateRandomNo(Ledgers ,"ledgerid"),
                                        "amount" : float(Totalbidamount ) *(-1),
                                        "datetime" : datetime.now(),
                                        "type" : "ESCROW",
                                        "jobid" : int(jobid),
                                        "jobbidid" : int(bidid),
                                        "paymentdetailsJSON" : payment_details,
                                        "refunddetailsJSON" : "",
                                        "refundcompletiondatetime" : "",
                                        "payingdatetime": "",
                                        "remark" : "",
                                        "active" : True})

                        Ledgers.insert({"userid" : userid,
                                        "ledgerid" : CommonUtils.generateRandomNo(Ledgers ,"ledgerid"),
                                        "amount" : float(commission),
                                        "datetime" : datetime.now(),
                                        "type" : "COMMISSION",
                                        "jobid" : int(jobid),
                                        "jobbidid" : int(bidid),
                                        "paymentdetailsJSON" : "",
                                        "refunddetailsJSON" : "",
                                        "refundcompletiondatetime" : "",
                                        "payingdatetime": "",
                                        "remark" : "",
                                        "active" : True})

                        Ledgers.insert({"userid" : finalBid['userid'],
                                        "ledgerid" : CommonUtils.generateRandomNo(Ledgers ,"ledgerid"),
                                        "amount" : float(finalbidamount),
                                        "datetime" : datetime.now(),
                                        "type" : "PAID",
                                        "jobid" : int(jobid),
                                        "jobbidid" : int(bidid),
                                        "paymentdetailsJSON" : "",
                                        "refunddetailsJSON" : "",
                                        "refundcompletiondatetime" : "",
                                        "payingdatetime": "",
                                        "remark" : "",
                                        "active" : True})

                        notificationtext = "Your Bid on job title ' " +jobCollection['title' ] +"' is accepted by Jobber :  " +jobberfullname

                        registration_id = find_FCM_id(finalBid['userid'])
                        if(registration_id):
                            data_message = {
                                "body" : notificationtext,
                            }

                            result = push_service.notify_single_device(registration_id=registration_id, message_title="Bid Accepted"
                                                                       ,message_body=notificationtext, data_message=data_message, click_action="FCM_PLUGIN_ACTIVITY")

                        Notifications.insert({"notificationid" :CommonUtils.generateRandomNo(Notifications ,"notificationid"),
                                              "notificationtext" :notificationtext,
                                              "notificationtype" :"Bid",
                                              "notificationtouserid" :int(finalBid['userid']),
                                              "notificationfromuserid" :userid,
                                              "jobid" : int(jobid),
                                              "jobbidid" : int(bidid),
                                              "commentid" :-1,
                                              "createddatetime" :datetime.now(),
                                              "updatedatetime" :datetime.now(),
                                              "isread" :False
                                              })
                        if bidderEmail is not None:
                            subject = "Bid Accepted."
                            msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"), recipients=[bidderEmail])
                            msg.html = render_template('/emailTemplates/Accept-bid.html', name= bidderfullname, title= jobCollection['title'] ,jobber=jobberfullname,
                                                       amount=int(float(transaction_amount['total'])))
                            Mail.send(msg)
                            EmailTracks.insert({"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"),
                                                "userid": finalBid['userid'], "email": bidderEmail, "subject": subject,
                                                "emailtext": msg.html, "createdatetime": datetime.now(),
                                                "updatedatetime": datetime.now()})
                        else:
                            print
                            "No email of bidder."

                elif request.json['status'] == "reversebid":
                    job_bid_detail = JobBids.find_one({"bidid": int(bidid)}, {"_id": 0})
                    if job_bid_detail is not None:

                        if job_bid_detail['status'] == 'pending':

                            Totalbidamount = int(float(transaction_amount['total']))
                            # updating bidamount array and reverse bid array
                            reverseBidData = {"reversebidamount": int(float(transaction_amount['total'])),
                                              "reversebiddatetime": datetime.now()}
                            JobBids.update({"bidid": int(bidid)}, {"$set": {"status": "reversebid",
                                                                            "reversebid": reverseBidData,
                                                                            "finalbidamount": Totalbidamount
                                                                            }})

                            commission = float(Totalbidamount * 0.1)

                            finalbidamount = float(Totalbidamount - commission)

                            Ledgers.insert({"userid": userid,
                                            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
                                            "amount": float(Totalbidamount) * (-1),
                                            "datetime": datetime.now(),
                                            "type": "ESCROW",
                                            "jobid": int(jobid),
                                            "jobbidid": int(bidid),
                                            "paymentdetailsJSON": payment_details,
                                            "refunddetailsJSON": "",
                                            "refundcompletiondatetime": "",
                                            "payingdatetime": "",
                                            "remark": "",
                                            "active": True})

                            Ledgers.insert({"userid": userid,
                                            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
                                            "amount": float(commission),
                                            "datetime": datetime.now(),
                                            "type": "COMMISSION",
                                            "jobid": int(jobid),
                                            "jobbidid": int(bidid),
                                            "paymentdetailsJSON": "",
                                            "refunddetailsJSON": "",
                                            "refundcompletiondatetime": "",
                                            "payingdatetime": "",
                                            "remark": "",
                                            "active": True})

                            Ledgers.insert({"userid": finalBid['userid'],
                                            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
                                            "amount": float(finalbidamount),
                                            "datetime": datetime.now(),
                                            "type": "PAID",
                                            "jobid": int(jobid),
                                            "jobbidid": int(bidid),
                                            "paymentdetailsJSON": "",
                                            "refunddetailsJSON": "",
                                            "refundcompletiondatetime": "",
                                            "payingdatetime": "",
                                            "remark": "",
                                            "active": True})

                            notificationtext = "You reverse bid on the job title " + jobCollection[
                                'title'] + " for bidder : " + str(bidderfullname)

                            registration_id = find_FCM_id(job_bid_detail['userid'])
                            if (registration_id):
                                data_message = {
                                    "body": notificationtext,
                                }

                                result = push_service.notify_single_device(registration_id=registration_id,
                                                                           message_title="Reverse Bid",
                                                                           message_body=notificationtext,
                                                                           data_message=data_message,
                                                                           click_action="FCM_PLUGIN_ACTIVITY")

                            Notifications.insert({"notificationid": CommonUtils.generateRandomNo(Notifications, "notificationid"),
                                                  "notificationtext": notificationtext,
                                                  "notificationtype": "Bid",
                                                  "notificationtouserid": int(job_bid_detail['userid']),
                                                  "notificationfromuserid": userid,
                                                  "jobid": int(jobid),
                                                  "jobbidid": int(bidid),
                                                  "commentid": -1,
                                                  "createddatetime": datetime.now(),
                                                  "updatedatetime": datetime.now(),
                                                  "isread": False
                                                  })

                            if bidderEmail is not None:
                                subject = "Reverse Bid on Job."
                                msg = Message(subject, sender=("SAVEonJOBS", "noreply@saveonjobs.com"),
                                              recipients=[bidderEmail])
                                msg.html = render_template('/emailTemplates/reverse-bid.html', name=bidderfullname,
                                                           title=jobCollection['title'], jobber=jobberfullname,
                                                           amount=int(float(transaction_amount['total'])))
                                Mail.send(msg)
                                EmailTracks.insert({"emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"),
                                                    "userid": finalBid['userid'], "email": bidderEmail,
                                                    "subject": subject, "emailtext": msg.html,
                                                    "createdatetime": datetime.now(), "updatedatetime": datetime.now()})
                            else:
                                print("No email of bidder.")

            return jsonify({"status": 200, "message": "Payment Successful"})


    except ResourceNotFound as e:
        # It will through ResourceNotFound exception if the payment not found
        print("Payment Not Found")
        print(e.message)
        return jsonify({"status": 500, "message": e.message})
