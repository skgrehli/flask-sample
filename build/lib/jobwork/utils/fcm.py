import datetime

from jobwork.constants import Constants
from jobwork.utils.common_utils import CommonUtils
from pyfcm import FCMNotification

__all__ = ['push_service']

push_service = FCMNotification(api_key=Constants.FCM_API_KEY)


# noinspection SpellCheckingInspection
class PushNotificationUtils(object):
    @classmethod
    def notify_onboard(cls, userid, fullname, device_token):
        if device_token:
            notificationtext = "Hello " + str(fullname) + "  SaveOnJobs welcomes you !!"
            data_message = {
                "body": notificationtext,
            }

            push_service.notify_single_device(registration_id=device_token,
                                              message_title="Welcome!",
                                              message_body=notificationtext,
                                              data_message=data_message,
                                              click_action="FCM_PLUGIN_ACTIVITY")

            from jobwork.models.notification import Notifications
            Notifications.insert({
                "notificationid": CommonUtils.generateRandomNo(Notifications, "notificationid"),
                "notificationtext": notificationtext,
                "notificationtype": "welcome",
                "notificationtouserid": int(userid),
                "notificationfromuserid": -1,
                "jobid": -1,
                "bidid": -1,
                "commentid": -1,
                "createddatetime": datetime.datetime.now(),
                "updatedatetime": datetime.datetime.now(),
                "isread": False
            })

    @classmethod
    def notify_bid_accepted(cls, userid, jobid, bidid, job_collection, jobberfullname, final_bid):
        notificationtext = "Your Bid on job title '" + job_collection[
            'title'] + "' is accepted by Jobber : " + jobberfullname
        from jobwork.models.user import User
        registration_id = User.find_FCM_id(final_bid['userid'])
        if registration_id:
            data_message = {
                "body": notificationtext,
            }
            push_service.notify_single_device(registration_id=registration_id, message_title="Bid Accepted",
                                              message_body=notificationtext, data_message=data_message)
        # Notification entry
        from jobwork.models.notification import Notifications
        Notifications.insert({
            "notificationid": CommonUtils.generateRandomNo(Notifications, "notificationid"),
            "notificationtext": notificationtext,
            "notificationtype": "Bid",
            "notificationtouserid": int(final_bid['userid']),
            "notificationfromuserid": userid,
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "commentid": -1,
            "createddatetime": datetime.datetime.now(),
            "updatedatetime": datetime.datetime.now(),
            "isread": False
        })

    @classmethod
    def notify_bid_reverse(cls, userid, jobid, bidid, job_collection, bidderfullname, job_bid_detail):
        notificationtext = "You reverse bid on the job title " + job_collection[
            'title'] + " for bidder : " + str(bidderfullname)

        from jobwork.models.user import User
        registration_id = User.find_FCM_id(job_bid_detail['userid'])
        if registration_id:
            data_message = {
                "body": notificationtext,
            }

            push_service.notify_single_device(registration_id=registration_id,
                                              message_title="Reverse Bid",
                                              message_body=notificationtext,
                                              data_message=data_message)

        from jobwork.models.notification import Notifications
        Notifications.insert({
            "notificationid": CommonUtils.generateRandomNo(Notifications, "notificationid"),
            "notificationtext": notificationtext,
            "notificationtype": "Bid",
            "notificationtouserid": int(job_bid_detail['userid']),
            "notificationfromuserid": userid,
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "commentid": -1,
            "createddatetime": datetime.datetime.now(),
            "updatedatetime": datetime.datetime.now(),
            "isread": False
        })
