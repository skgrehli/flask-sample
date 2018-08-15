import datetime

from jobwork.constants import Constants
from jobwork.utils.common_utils import CommonUtils
from twilio.rest import Client

msgclient = Client(Constants.MSG_ACCOUNT_SID, Constants.MSG_AUTH_TOKEN)

sendFrom = Constants.MSG_SEND_FROM


# noinspection SpellCheckingInspection
class SmsUtils(object):
    @classmethod
    def send_onboard_sms(cls, userid, mobileotp, mobile):
        sendText = "Mobile Verify OTP is " + str(mobileotp)
        message = msgclient.messages.create(body=sendText, to=mobile, from_=sendFrom)
        print(message.sid)
        from jobwork.models.messagetrack import MessageTracks
        MessageTracks.insert({
            "messagetrackid": CommonUtils.generateRandomNo(MessageTracks, "messagetrackid"),
            "userid": userid,
            "mobile": mobile,
            "messagetext": sendText,
            "messagesid": message.sid,
            "createdatetime": datetime.datetime.now(),
            "updatedatetime": datetime.datetime.now()
        })
