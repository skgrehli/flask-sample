from flask import Blueprint,request,make_response,jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.conversations import Conversations
from jobwork.models.messages import Messages
from jobwork.models.user import User
from jobwork.constants import Constants
from jobwork.models.city import CityCollections
from jobwork.models.jobs import Jobs
from jobwork.models.jobbids import JobBids
from jobwork.models.ledger import Ledgers


dashboard=Blueprint('dashboard',__name__,url_prefix='')
@dashboard.route('/user/dashboard' ,methods=['POST'])
@authentication
def user_dashboard():
    URL = Constants.URL
    imagePath = Constants.IMAGE_PATH
    try :
        dashboardData = {}
        userid = int(request.json['userid'])
        userdata_array = User.find_one({"userid" :userid, "active" :True} ,{"_id" :0})

        if userdata_array is not None:
            # Account Percentage

            if userdata_array['paymentdetailsJSON']['bankaccountname'] != "":
                overallAccountPercentage = 100
            else:
                overallAccountPercentage = 0


            verifyLen = len(userdata_array['proJSON']) - 1
            countVerificationPercentage = 0
            if userdata_array['proJSON']['facebookapproved'] == True:
                countVerificationPercentage = countVerificationPercentage + 1
            if userdata_array['proJSON']['policeverification'] == True:
                countVerificationPercentage = countVerificationPercentage + 1
            if userdata_array['proJSON']['professionalcertificationverified'] == True:
                countVerificationPercentage = countVerificationPercentage + 1
            if userdata_array['proJSON']['mobileverified'] == True:
                countVerificationPercentage = countVerificationPercentage + 1

            if countVerificationPercentage != 0:
                countVerificationPercentage = int(countVerificationPercentage * 100)
                overallVerificationPercentage = float(countVerificationPercentage /verifyLen)
            else:
                overallVerificationPercentage = 0

            # Skills Verfication

            skillsLen = 5
            countSkillsPercentage = len(userdata_array['skillsJSON'])
            if countSkillsPercentage != 0:
                if countSkillsPercentage < skillsLen:
                    countSkillsPercentage = countSkillsPercentage * 100
                    overallSkillsPercentage = float(countSkillsPercentage /skillsLen)
                else:
                    overallSkillsPercentage = 100
            else:
                overallSkillsPercentage = 0

            # Profile Verification

            profileLen = 13
            countProfilePercentage = 0
            if userdata_array['addressJSON']['city'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['addressJSON']['state'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['addressJSON']['country'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['addressJSON']['state'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['addressJSON']['country'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['addressJSON']['state'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['addressJSON']['country'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['firstname'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['lastname'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['locationid'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['email'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['mobile'] != "":
                countProfilePercentage = countProfilePercentage + 1
            if userdata_array['aboutme'] != "":
                countProfilePercentage = countProfilePercentage + 1

            if countProfilePercentage != 0:
                countProfilePercentage = countProfilePercentage * 100
                countProfilePercentage = float(countProfilePercentage /profileLen)
            else:
                countProfilePercentage = 0

            # Jobs Percentage

            jobs_posted = Jobs.find({"creatinguserid" :int(userid)}).count()
            jobs_completed = JobBids.find({"userid" :int(userid) ,"status" :"completed"}).count()

            # Payment percentage
            total_received_amount = 0
            total_paid_refund = 0
            total_commission_refund = 0
            earned_amount = 0
            paid_amount = 0
            total_earning_amount = 0
            total_received_list = Ledgers.find({"userid" :userid ,"type" :"ESCROW"} ,{"_id" :0})
            if total_received_list is not None:
                for total_received_dict in total_received_list:
                    total_received_amount += total_received_dict['amount']

            total_paid_refund_list = Ledgers.find({"userid" :userid ,"type" :"REFUND"} ,{"_id" :0})
            if total_paid_refund_list is not None:
                for total_paid_refund_dict in total_paid_refund_list:
                    total_paid_refund += total_paid_refund_dict['amount']

            paid_amount = (total_received_amount - total_paid_refund ) * (-1)

            total_earning_list = Ledgers.find({"userid" :userid ,"type" :"PAID OUT"} ,{"_id" :0})
            if total_earning_list is not None:
                for total_earning_dict in total_earning_list:
                    total_earning_amount += total_earning_dict['amount']


            earned_amount = total_earning_amount

            # overall Percentage
            overallPercentage = float \
                (overallAccountPercentage + overallVerificationPercentage + overallSkillsPercentage + countProfilePercentage)
            overallPercentage = float(overallPercentage /4)

            print(overallPercentage)

            fullname = userdata_array['firstname'] + ' ' + userdata_array['lastname']
            picurl = URL +imagePath +userdata_array['picurl']
            dashboardData = {"picurl" :picurl ,"jobsPosted" :jobs_posted ,"jobsCompleted" :jobs_completed
                             ,"earnedAmount" :earned_amount ,"paidAmount" :paid_amount
                             ,"overallPercentage": overallPercentage, "accountPercentage": overallAccountPercentage,
                             "verificationPercentage": overallVerificationPercentage,
                             "skillsPercentage": overallSkillsPercentage, "profilePercentage": countProfilePercentage,
                             "fullname": fullname}

            return jsonify({'status': 200, 'message': 'Dashboard Data.', 'dashboardData': dashboardData})
        else:
            return jsonify({'status': 402, 'message': 'No data fouund', 'dashboardData': dashboardData})

    except Exception as e:
        return jsonify({"status": 500, "message": "error"})

