from flask import Blueprint,jsonify,request
from datetime import datetime
from jobwork.utils.common_utils import CommonUtils
from jobwork.models.invoicenumber import InvoiceNumbers
from jobwork.models.invoice import Invoice
from jobwork.models.jobs import Jobs
from jobwork.models.user import User
from jobwork.models.state import StateCollections
from jobwork.models.country import CountryCollections
from jobwork.models.city import CityCollections
from jobwork.models.jobbids import JobBids
from jobwork.models.jobcomments import JobComments
from jobwork.middleware.authentication import authentication

get_invoice = Blueprint('get_invoice',__name__,url_prefix='')

@get_invoice.route('/invoice/year/invoicenumber', methods=['POST'])
def invoice_year_invoicenumber():
    InvoiceNumbers.insert({"invoicenumberid" :CommonUtils.generateRandomNo(InvoiceNumbers ,"invoicenumberid"),
                           "invoicenumber": 0,
                           "financialyear": "2016 - 2017",
                           "startyear" :2016,
                           "endyear" :2017,
                           "createdatetime": datetime.now(),
                           "updatedatetime": datetime.now()
                           })
    return jsonify({"status":"ok"})



@get_invoice.route('/invoice/list', methods=['POST'])
@authentication
def invoice_list():
    userid = int(request.json['userid'])
    token = request.json['token']
    invoiceid=request.json['invoiceid']
    if invoiceid == 1:
        invoiceData = list(Invoice.find({"invoiceid":int(request.json['invoiceid'])},{"_id":0}))
    else:
        invoiceData = list(Invoice.find({"userid":userid},{"_id":0}))

    invoiceAllData = {}
    invoiceArray = []

    if len(invoiceData) > 0:
        for invoiceDataArray in invoiceData:
            # jobsDetail Data
            jobsDetail = Jobs.find_one({"jobid" : int(invoiceDataArray['jobid']),"active":True},{"_id":0})
            # Job Created By User
            createdUserDetail = User.find_one({"userid" : jobsDetail['creatinguserid'], "active":True},{"_id":0})
            # For job Bid and Comments (How many user bid on this job.)
            job_biding_count = JobBids.find({"jobid" : invoiceDataArray['jobid']},{"_id":0}).count()
            job_comment_count = JobComments.find({"jobid" : invoiceDataArray['jobid']},{"_id":0}).count()
            # For User who post this job (How many jobs bid by this user.)
            if createdUserDetail is not None:
                user_biding_count = JobBids.find({"userid" : createdUserDetail['userid']},{"_id":0}).count()
                user_comment_count = JobComments.find({"userid" : createdUserDetail['userid']},{"_id":0}).count()
                # Address Detail for created User
                citydetail = CityCollections.find_one({"cityid":createdUserDetail['addressJSON']['city']},{"_id":0})
                statedetail = StateCollections.find_one({"stateid":citydetail['stateid']},{"_id":0})
                countrydetail = CountryCollections.find_one({"countryid":citydetail['countryid']},{"_id":0})
                address2 = createdUserDetail['addressJSON']['address2']
                address1 = createdUserDetail['addressJSON']['address1']
                if address2 == "":
                    fullAddress = address1+","
                else:
                    fullAddress = address1+", "+address2+","
            else:
                fullAddress = ""
                user_biding_count = 0
                user_comment_count = 0

            # Billing to User
            billingUserDetail = User.find_one({"userid" : invoiceDataArray['userid'], "active":True},{"_id":0})
            # Address Detail for created User
            billingcitydetail = CountryCollections.find_one({"cityid":billingUserDetail['addressJSON']['city']},{"_id":0})
            billingstatedetail = StateCollections.find_one({"stateid":billingcitydetail['stateid']},{"_id":0})
            billingcountrydetail = CountryCollections.find_one({"countryid":billingcitydetail['countryid']},{"_id":0})
            billingaddress2 = billingUserDetail['addressJSON']['address2']
            billingaddress1 = billingUserDetail['addressJSON']['address1']
            if billingaddress2 == "":
                billingfullAddress = billingaddress1+","
            else:
                billingfullAddress = billingaddress1+", "+billingaddress2+","

            createdInfoCollection = {
                                    "createdByuserid" : createdUserDetail['userid'],
                                    "createdByaddressJSON" : createdUserDetail['addressJSON'],
                                    "createdByemail" : createdUserDetail['email'],
                                    "createdByfirstname" : createdUserDetail['firstname'],
                                    "createdBylastname" : createdUserDetail['lastname'],
                                    "createdBymobile" : createdUserDetail['mobile'],
                                    "createdByaddress" : fullAddress,
                                    "createdBycity" : citydetail['city'],
                                    "createdBystate" : statedetail['state'],
                                    "createdBycountry" : countrydetail['country'],
                                    "createdBypincode" : createdUserDetail['addressJSON']['pincode'],
                                    "createdByactive" : createdUserDetail['active'],
                                    "createdByuser_biding_count" : user_biding_count,
                                    "createdByuser_comment_count" : user_comment_count,
                                    "job_biding_count" : job_biding_count,
                                    "user_comment_count" : user_comment_count,
                                    "jobsDetail" : jobsDetail,
                                    "billinguserid" : billingUserDetail['userid'],
                                    "billingaddressJSON" : billingUserDetail['addressJSON'],
                                    "billingemail" : billingUserDetail['email'],
                                    "billingfirstname" : billingUserDetail['firstname'],
                                    "billinglastname" : billingUserDetail['lastname'],
                                    "billingmobile" : billingUserDetail['mobile'],
                                    "billingaddress" : billingfullAddress,
                                    "billingcity" : billingcitydetail['city'],
                                    "billingstate" : billingstatedetail['state'],
                                    "billingcountry" : billingcountrydetail['country'],
                                    "billingpincode" : billingUserDetail['addressJSON']['pincode'],
                                    "billingactive" : billingUserDetail['active'],
                                    }
            invoiceDataArray.update(createdInfoCollection)
            invoiceArray.append(invoiceDataArray)
        return jsonify({"status" : 200, "message" : "Invoice List.", "invoiceAllData":invoiceArray})
    else:
        return jsonify({"status" : 200, "message" : "No Data.", "invoiceAllData":invoiceArray})
