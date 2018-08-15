import datetime

from flask import request, make_response, Blueprint, jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.jobbids import JobBids
from jobwork.models.jobs import Jobs
from jobwork.models.ledger import Ledgers
from jobwork.models.user import User
from jobwork.models.transactiontrack import TransactionTrack
from jobwork.utils.common_utils import CommonUtils
from jobwork.utils.email import EmailUtils
from jobwork.utils.fcm import PushNotificationUtils
from paypalrestsdk import Payment, ResourceNotFound

user_transaction = Blueprint('user_transaction', __name__, url_prefix='')

__all__ = ["user_transaction"]


# noinspection SpellCheckingInspection
@user_transaction.route('/create/temp/transaction', methods=['POST'])
@authentication
def temp_transaction():
    try:
        userid = int(request.json['userid'])

        result_transaction = TransactionTrack.find_one(
            {"userid": userid, "jobid": int(request.json['jobid']), "jobbid": int(request.json['jobbid'])})


        if result_transaction:

            created_transactionid = CommonUtils.generateRandomNo(TransactionTrack, "transactionid")
            TransactionTrack.insert({
                "transactionid": created_transactionid,
                "requestdatetime": datetime.datetime.now(),
                "amount": request.json['amount'],
                "transactionstatus": request.json['transactionstatus'],
                "transactionresponse": "",
                "userid": userid,
                "jobid": int(request.json['jobid']),
                "jobbid": int(request.json['jobbid']),
                "responsedatetime": "",
                "type": "manual"
            })

        else:

            created_transactionid = result_transaction['transactionid']

            TransactionTrack.update({
                "transactionid": created_transactionid
            }, {
                "$set": {
                    "requestdatetime": datetime.datetime.now()
                }
            })
        return make_response(jsonify({"status": 200, "transactionid": created_transactionid}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"status": 500, "message": "Something went wrong, Please try again!"}), 500)


# noinspection SpellCheckingInspection
@user_transaction.route('/paypal_payment', methods=['POST'])
@authentication
def paypal_payment():
    try:
        userid = int(request.json['userid'])
        pay_id = request.json['payid']
        print(pay_id)
        payment = Payment.find(pay_id)
        print(payment)
        transactions = []
        transaction_amount = {}
        # credit_card = {}
        sales_id = 0
        soj_transaction_id = 0
        transactionstatus = ""
        # for card_details in payment.payer.funding_instruments:
        # 	if card_details.has_key('credit_card_token'):
        # 		credit_card = {"expire_year":card_details.credit_card_token.expire_year,
        # "type":card_details.credit_card_token.type,"number":card_details.credit_card_token.number,
        # "expire_month":card_details.credit_card_token.expire_month}
        # 	elif card_details.has_key('credit_card'):
        # 		credit_card = {"expire_year":card_details.credit_card.expire_year,
        # "type":card_details.credit_card.type,"number":card_details.credit_card.number,
        # "expire_month":card_details.credit_card.expire_month}
        # transactions.append(credit_card)
        for transaction_details in payment.transactions:
            transaction_amount = {"currency": transaction_details.amount.currency,
                                  "total": transaction_details.amount.total}
            sales_link = transaction_details['related_resources'][0]['sale']['links'][0]['href']
            sales_list = sales_link.split('sale')[1]
            sales_id = sales_list.split('/')[1]
            soj_transaction_id = int(transaction_details.description)
            transactionstatus = int(request.json['transactionid'])
        transactions.append(transaction_amount)
        payment_details = {"payment": payment.id, "sales_id": sales_id, "paymenttype": payment.payer.payment_method,
                           "state": payment.state, "transaction_details": transactions}
        if payment.state == "approved":

            print(soj_transaction_id)
            TransactionTrack.update({
                "transactionid": soj_transaction_id
            }, {
                "$set": {
                    "transactionstatus": transactionstatus,
                    "transactionresponse": payment_details,
                    "responsedatetime": datetime.datetime.now()
                }
            })

            transactions_details_from_database = TransactionTrack.find_one({"transactionid": soj_transaction_id},
                                                                           {"_id": 0})
            print(transactions_details_from_database)

            bidid = transactions_details_from_database['jobbid']
            jobid = transactions_details_from_database['jobid']

            final_bid = JobBids.find_one({"bidid": int(bidid)}, {"_id": 0})

            completionremarks = ""
            # completionstatus = ""
            bidcanceldatetime = ""
            bidcancellationreason = ""
            # bidselected = False
            jobberfullname = ""
            # jobberEmail = None
            # jobberMobile = None
            bidderfullname = ""
            bidder_email = None
            # bidderMobile = None
            person_selected = 0

            if final_bid is not None:

                job_collection = Jobs.find_one({"jobid": final_bid['jobid']}, {"_id": 0})
                if job_collection:
                    try:
                        person_selected = int(job_collection['personsselected'])
                    except ValueError:
                        pass

                    user_jobber_collection = User.find_one({"userid": job_collection['creatinguserid']}, {"_id": 0})
                    if user_jobber_collection is not None:
                        jobberfullname = user_jobber_collection['firstname'] + " " + user_jobber_collection['lastname']
                        # jobberEmail = user_jobber_collection['email']
                        # jobberMobile = user_jobber_collection['mobile']

                    user_bidder_collection = User.find_one({"userid": final_bid['userid']}, {"_id": 0})
                    if user_bidder_collection is not None:
                        bidderfullname = user_bidder_collection['firstname'] + " " + user_bidder_collection['lastname']
                        bidder_email = user_bidder_collection['email']
                        # bidderMobile = user_bidder_collection['mobile']
                else:
                    print("No jobs")
                if request.json['status'] == "selectedbyjobber":
                    if final_bid['status'] == "pending":
                        print(transaction_amount)
                        JobBids.update({
                            "bidid": int(bidid)
                        }, {
                            "$set": {
                                "selected": True,
                                "final_bidamount": int(float(transaction_amount['total'])),
                                "bidcanceldatetime": bidcanceldatetime,
                                "bidcancellationreason": bidcancellationreason,
                                "status": "selectedbyjobber",
                                "completionstatus": "pending",
                                "completionremarks": completionremarks
                            }
                        })

                        if job_collection['personsrequired'] > person_selected:
                            if job_collection['personsrequired'] == person_selected + 1:
                                Jobs.update({"jobid": int(jobid)}, {"$set": {
                                    "personsselected": int(person_selected + 1),
                                    "jobstatus": "allotted"
                                }})
                            else:
                                Jobs.update({"jobid": int(jobid)}, {"$set": {
                                    "personsselected": int(person_selected + 1)
                                }})
                        # Ledger Entries
                        Ledgers.bid_selection_entries(userid, jobid, bidid, final_bid, payment_details)

                        # Push Notification Bid Accepted
                        PushNotificationUtils.notify_bid_accepted(userid, jobid, bidid, job_collection, jobberfullname,
                                                                  final_bid)
                        # Bid Accepted Email
                        EmailUtils.send_bid_accpeted_mail(final_bid['userid'], bidder_email, job_collection['title'],
                                                          bidderfullname, jobberfullname, transaction_amount['total'])

                elif request.json['status'] == "reversebid":
                    job_bid_detail = JobBids.find_one({"bidid": int(bidid)}, {"_id": 0})
                    if job_bid_detail is not None:

                        if job_bid_detail['status'] == 'pending':
                            total_bid_amount = int(float(transaction_amount['total']))
                            # updating bidamount array and reverse bid array
                            reverse_bid_data = {"reversebidamount": int(float(transaction_amount['total'])),
                                                "reversebiddatetime": datetime.datetime.now()}
                            JobBids.update({"bidid": int(bidid)}, {"$set": {"status": "reversebid",
                                                                            "reversebid": reverse_bid_data,
                                                                            "final_bidamount": total_bid_amount
                                                                            }})
                            # Bid Reverse Entried
                            Ledgers.bid_reverse_entries(userid, jobid, bidid, final_bid, payment_details)
                            # Bid Reverse Push Notification
                            PushNotificationUtils.notify_bid_reverse(userid, jobid, bidid, job_collection,
                                                                     bidderfullname, job_bid_detail)
                            # Bid Reverse Email
                            EmailUtils.send_reverse_bid_mail(final_bid['userid'], bidder_email, job_collection['title'],
                                                             bidderfullname, jobberfullname,
                                                             transaction_amount['total'])
        return make_response(jsonify({"status": 200, "message": "Payment Successful"}), 200)
    except ResourceNotFound as e:
        print("Payment Not Found")
        print(str(e))
        return make_response(jsonify({"status": 500, "message": "Something went wrong, Please try again!"}), 500)
    except Exception as e:
        print(str(e))
        return make_response(jsonify({"status": 500, "message": "Something went wrong, Please try again!"}), 500)
