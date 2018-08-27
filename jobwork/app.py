from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from jobwork.routes.bank import user_bank
from jobwork.routes.transactions import user_transaction
from jobwork.routes.facebook_signup import facebook_signup
from jobwork.routes.google_signup import google_signup
from jobwork.routes.jobs import jobs_route
from jobwork.routes.get_otp import user_otp
from jobwork.routes.get_apis import get_route
from jobwork.routes.location import location_route
from jobwork.routes.job_filter import filter
from jobwork.routes.draft import draft_job
from jobwork.routes.my_bids import my_bids
from jobwork.routes.sendDataList import datalist
from jobwork.routes.conversations import user_conversation
from jobwork.routes.dashboard import dashboard
from jobwork.routes.jobreview import job_review
from jobwork.routes.profile_fetch import profile_fetch
from jobwork.routes.notification import notification
from jobwork.routes.skill_list import skill_list
from jobwork.routes.tamplate_categories import tempcat
from jobwork.routes.invoice import get_invoice
from jobwork.routes.report import jw_report
from jobwork.routes.email import jw_email
from jobwork.routes.password import usr_password
from jobwork.routes.user_account import usr_account
from jobwork.routes.paypal import jw_paypal
from jobwork.routes.paypal_web import jw_paypal_web
from jobwork.routes.upload_docs import jw_upload
from jobwork.routes.user_login import user_login
from jobwork.routes.user_register_all import user_register_all
from jobwork.routes.remove_acount import remove_account
from jobwork.routes.registration_jobwork import user_register_jobwork
from jobwork.routes.docs_upload import upload_doc
from jobwork.routes.job_comment import jw_com
from jobwork.routes.job_bid import job_bid
app = Flask(__name__)


# Configurations
app.config.from_object('config')
app.register_blueprint(user_bank)
app.register_blueprint(user_transaction)
app.register_blueprint(facebook_signup)
app.register_blueprint(google_signup)
app.register_blueprint(jobs_route)
app.register_blueprint(user_otp)
app.register_blueprint(location_route)
app.register_blueprint(get_route)
app.register_blueprint(filter)
app.register_blueprint(draft_job)
app.register_blueprint(my_bids)
app.register_blueprint(user_conversation)
app.register_blueprint(dashboard)
app.register_blueprint(datalist)
app.register_blueprint(job_review)
app.register_blueprint(profile_fetch)
app.register_blueprint(notification)
app.register_blueprint(skill_list)
app.register_blueprint(tempcat)
app.register_blueprint(get_invoice)
app.register_blueprint(jw_report)
app.register_blueprint(usr_password)
app.register_blueprint(jw_email)
app.register_blueprint(usr_account)
app.register_blueprint(jw_paypal)
app.register_blueprint(jw_paypal_web)
app.register_blueprint(jw_upload)
app.register_blueprint(jw_com)
app.register_blueprint(job_bid)

app.register_blueprint(user_login)
app.register_blueprint(remove_account)
app.register_blueprint(upload_doc)
app.register_blueprint(user_register_all)



CORS(app)

mail = Mail()

mail.init_app(app)
mail = Mail(app)


@app.after_request
def set_application_json(response):
    if response.mimetype != 'text/html':
        response.mimetype = "application/json"
    return response
