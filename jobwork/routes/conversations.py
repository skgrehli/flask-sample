from flask import Blueprint,request,make_response,jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.conversations import Conversations
from jobwork.models.messages import Messages
from jobwork.models.user import User
from jobwork.constants import Constants
from jobwork.models.city import CityCollections
from jobwork.utils.common_utils import CommonUtils
from jobwork.models.jobbids import JobBids
from datetime import datetime,timedelta
from jobwork.models.jobs import Jobs
from jobwork.models.conversations import Conversations
import calendar

user_conversation=Blueprint('user_conversation',__name__,url_prefix='')




@user_conversation.route('/conversation/messages/list', methods=['POST'])
@authentication
def conversation_messages_list():
    #return jsonify({"ok": 1})
    URL=Constants.URL
    imagePath=Constants.IMAGE_PATH
    userid = int(request.json['userid'])
    allMessageData = []
    converstaionCollection = Conversations.find_one({"conversationid":int(request.json['conversationid']),"active":True})
    displayuserCollection = {"displayfullname" : "", "displaycityname" : "", "displaypicurl":"", "displayuserid":"", "conversationid":int(request.json['conversationid'])}

    userDisplayData = Conversations.find_one({"conversationid":int(request.json['conversationid']),"active":True},{"_id":0,"userid1":1,"userid2":1})
    if userDisplayData is not None:
        # messages.update({"conversationid":request.json['conversationid']},{"$set":{"isread" : True}}, True, True)
        messageData = list(Messages.find({"conversationid":request.json['conversationid'], "isread" : False},{"_id":0}))
        if len(messageData) > 0:
            for messageCollection in messageData:
                Messages.update({"createdatetimeinseconds":messageCollection['createdatetimeinseconds']},{"$set":{"isread" : True}})
        else:
            print("No unread Message.")
        if userDisplayData['userid1'] != userid:
            userData = User.find_one({"userid" : userDisplayData['userid1']},{"_id":0})
            if userData is not None:
                cityName = {}
                fullname = userData['firstname'] + " " + userData['lastname']
                if userData['picurl'] != "":
                    picurl = URL+imagePath+userData['picurl']
                else:
                    picurl = URL+imagePath+"user-no-image.jpg"
                if userData['addressJSON']['city'] != "":
                    cityName = CityCollections.find_one({"cityid": userData['addressJSON']['city']},{"_id":0,"city":1})
                else:
                    cityName['city'] = ""
                displayuserCollection = {"displayfullname" : fullname, "displaycityname" : cityName['city'], "displaypicurl":picurl, "displayuserid":userDisplayData['userid1'], "conversationid":int(request.json['conversationid'])}

        if userDisplayData['userid2'] != userid:
            userData = User.find_one({"userid" : userDisplayData['userid2']},{"_id":0})
            if userData is not None:
                fullname = userData['firstname'] + " " + userData['lastname']
                if userData['picurl'] != "":
                    picurl = URL+imagePath+userData['picurl']
                else:
                    picurl = URL+imagePath+"user-no-image.jpg"
                cityName = CityCollections.find_one({"cityid": userData['addressJSON']['city']},{"_id":0,"city":1})
                displayuserCollection = {"displayfullname" : fullname, "displaycityname" : cityName['city'], "displaypicurl":picurl, "displayuserid":userDisplayData['userid2'], "conversationid":int(request.json['conversationid'])}
    else:
        return jsonify({"status":402,"message":"No Data."})

    if converstaionCollection is not None:
        messageData = list(Messages.find({"conversationid":int(request.json['conversationid'])},{"_id":0}).sort("createddatetime", 1))
        if len(messageData) > 0:
            for messageListData in messageData:
                userData = User.find_one({"userid" : int(messageListData['userid'])},{"_id":0})
                if userData is not None:
                    fullname = userData['firstname'] + " " + userData['lastname']
                    if userData['picurl'] != "":
                        picurl = URL+imagePath+userData['picurl']
                    else:
                        picurl = URL+imagePath+"user-no-image.jpg"
                    cityName = CityCollections.find_one({"cityid": userData['addressJSON']['city']},{"_id":0,"city":1})
                    userDataCollection = {"fullname" : fullname, "cityname" : cityName['city'], "picurl":picurl}
                    messageListData.update(userDataCollection)
                allMessageData.append(messageListData)

            return jsonify({"status" : 200, "message" : "Message Data.", "messageListData":allMessageData, "displayuserCollection":displayuserCollection})
        else:
            return jsonify({"status" : 200, "message" : "No Message data Found.", "messageListData":[], "displayuserCollection":displayuserCollection})
    else:
        return jsonify({"status" : 200, "message" : "No Message data Found.", "messageListData":[], "displayuserCollection":displayuserCollection})



@user_conversation.route('/conversation/create', methods=['POST'])
def conversation_create():
    userid = int(request.json['userid'])
    token = request.json['token']

    check_status = JobBids.find({"jobid":int(request.json['jobid']),"userid":userid,"active":True,"status" : { "$in" : ["selectedbyjobber","approvedbybidder"]}}).count()

    if check_status == 1:

        secdatetime = datetime.utcnow() - timedelta(minutes=1)
        jobData = Jobs.find_one({"jobid":int(request.json['jobid']),"active":True,"jobstatus" : {"$ne": "completed"},"expired":False},{"_id":0})

        if jobData is not None:
            if jobData['creatinguserid'] != userid:
                conversationData = Conversations.find_one({"userid1":jobData['creatinguserid'], "userid2":userid, "jobid":jobData['jobid']},{"_id":0})
                if conversationData is None:
                    conversationid = CommonUtils.generateRandomNo(Conversations,"conversationid")
                    Conversations.insert({"userid1":jobData['creatinguserid'],
                                            "userid2":userid,
                                            "lastdatetime":datetime.now(),
                                            "lastmessages":None,
                                            "lastmessagesuserid":None,
                                            "conversationid":conversationid,
                                            "jobid":jobData['jobid'],
                                            "createddatetime":datetime.now(),
                                            "createdatetimeinseconds":calendar.timegm(secdatetime.utctimetuple()),
                                            "updatedatetime":datetime.now(),
                                            "jobexpired":False,
                                            "active":True})

                    conversationList = list(Conversations.find({"conversationid":conversationid},{"_id":0}).sort("createddatetime", -1))

                    return jsonify({"status" : 200, "message" : "Conversation Created.", "conversationList":conversationList})
                else:
                    return jsonify({"status" : 402, "message" : "Conversation already Exist.","conversationData":conversationData['conversationid']})
            else:
                return jsonify({"status" : 402, "message" : "Conversation not on same user.","conversationData":[]})
        else:
            return jsonify({"status" : 402, "message" : "No job data Found.", "conversationList":[]})
    else:
        return jsonify({"status" :402,"message": "status not correct","conversationList":[]})


@user_conversation.route('/conversations/list', methods=['POST'])
def conversations_list():
    userid = int(request.json['userid'])
    token = request.json['token']
    allconversationListData = []
    URL = Constants.URL
    imagePath = Constants.IMAGE_PATH

    conversationData = list(Conversations.find({"$or":[{"userid1":userid},{"userid2":userid}],"active":True},{"_id":0}).sort("lastdatetime", -1))

    if len(conversationData) > 0:
        for conversationListData in conversationData:
            messageUnreadCount = Messages.find({"conversationid":conversationListData['conversationid'], "isread":False},{"_id":0}).count()
            conversationListData.update({"messageUnreadCount":messageUnreadCount})
            # Users Detail
            userData1 = User.find_one({"userid" : int(conversationListData['userid1'])},{"_id":0})
            if userData1 is not None:
                fullname1 = userData1['firstname'] + " " + userData1['lastname']
                cityName1 = {}
                if userData1['picurl'] != "":
                    picurl1 = URL+imagePath+userData1['picurl']
                else:
                    picurl1 = URL+imagePath+"user-no-image.jpg"
                if userData1['addressJSON']['city'] != "":
                    cityName1 = CityCollections.find_one({"cityid": userData1['addressJSON']['city']},{"_id":0,"city":1})
                else:
                    cityName1['city'] = ""
                if conversationListData['userid1'] != userid:
                    lastMessageDetail = {"lastuserfullname" : fullname1, "lastusercityname" : cityName1['city'], "lastuserpicurl":picurl1}
                    conversationListData.update(lastMessageDetail)
                userDataCollection1 = {"fullname1" : fullname1, "cityname1" : cityName1['city'], "picurl1":picurl1}
                conversationListData.update(userDataCollection1)

            userData2 = User.find_one({"userid" : int(conversationListData['userid2'])},{"_id":0})
            if userData2 is not None:
                fullname2 = userData2['firstname'] + " " + userData2['lastname']
                cityName2 = {}
                if userData2['picurl'] != "":
                    picurl2 = URL+imagePath+userData2['picurl']
                else:
                    picurl2 = URL+imagePath+"user-no-image.jpg"
                if userData2['addressJSON']['city'] != "":
                    cityName2 = CityCollections.find_one({"cityid": userData2['addressJSON']['city']},{"_id":0,"city":1})
                else:
                    cityName2['city'] = ""
                if conversationListData['userid2'] != userid:
                    lastMessageDetail = {"lastuserfullname" : fullname2, "lastusercityname" : cityName2['city'], "lastuserpicurl":picurl2}
                    conversationListData.update(lastMessageDetail)
                userDataCollection2 = {"fullname2" : fullname2, "cityname2" : cityName2['city'], "picurl2":picurl2}
                conversationListData.update(userDataCollection2)

            allconversationListData.append(conversationListData)

        return jsonify({"status" : 200, "message" : "Conversation Data.", "conversationListData":allconversationListData})
    else:
        return jsonify({"status" : 200, "message" : "No Conversation data Found.", "conversationListData":[]})

