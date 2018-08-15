import datetime

from flask_mail import Message
from flask import render_template
from jobwork.constants import Constants
from jobwork.utils.common_utils import CommonUtils


# noinspection SpellCheckingInspection
class EmailUtils(object):
    @classmethod
    def send_mail(cls, subject, sender, recipients, rendered_template):
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.html = rendered_template
        from jobwork.app import mail
        mail.send(msg)
        return

    @classmethod
    def send_onboard_email(cls, userid, email, email_hash, firstname):
        subject = "Your SAVEonJOBS.comAccount Email Verification"
        sender = ("SAVEonJOBS", "noreply@saveonjobs.com")
        recipients = [email]
        reset_password_link = str(Constants.URL) + "/user/emailverify__" + str(email_hash)

        template = render_template(Constants.ONBOARD_EMAIL_TEMPLATE, name=firstname, resetLink=reset_password_link,
                                   email=email)
        cls.send_mail(subject, sender, recipients, template)
        from jobwork.models.emailtrack import EmailTracks
        EmailTracks.insert({
            "emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"),
            "userid": userid,
            "email": email,
            "subject": subject,
            "emailtext": template,
            "createdatetime": datetime.datetime.now(),
            "updatedatetime": datetime.datetime.now()
        })

    @classmethod
    def send_bid_accpeted_mail(cls, userid, bidder_email, job_title, bidder_name, jobber_name, txn_amount):
        if bidder_email:
            subject = "Bid Accepted."
            sender = ("SAVEonJOBS", "noreply@saveonjobs.com")
            recipients = [bidder_email]
            template = render_template(Constants.BID_ACCTEPED_EMAIL_TEMPLATE, name=bidder_name, title=job_title,
                                       jobber=jobber_name, amount=int(float(txn_amount)))
            cls.send_mail(subject, sender, recipients, template)

            from jobwork.models.emailtrack import EmailTracks
            EmailTracks.insert({
                "emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"),
                "userid": userid,
                "email": bidder_email,
                "subject": subject,
                "emailtext": template,
                "createdatetime": datetime.datetime.now(),
                "updatedatetime": datetime.datetime.now()
            })
        else:
            print("No email of bidder.")
        return

    @classmethod
    def send_reverse_bid_mail(cls, userid, bidder_email, job_title, bidder_name, jobber_name, txn_amount):
        if bidder_email:
            subject = "Reverse Bid on Job."
            sender = ("SAVEonJOBS", "noreply@saveonjobs.com")
            recipients = [bidder_email]
            template = render_template(Constants.BID_REVERSE_EMAIL_TEMPLATE, name=bidder_name, title=job_title,
                                       jobber=jobber_name, amount=int(float(txn_amount)))
            cls.send_mail(subject, sender, recipients, template)

            from jobwork.models.emailtrack import EmailTracks
            EmailTracks.insert({
                "emailtrackid": CommonUtils.generateRandomNo(EmailTracks, "emailtrackid"),
                "userid": userid,
                "email": bidder_email,
                "subject": subject,
                "emailtext": template,
                "createdatetime": datetime.datetime.now(),
                "updatedatetime": datetime.datetime.now()
            })
        else:
            print("No email of bidder.")
        return
