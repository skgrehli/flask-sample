from jobwork.constants import Constants

UPLOAD_FOLDER_PROFILE = 'static/front_end/images/profile/'
UPLOAD_FOLDER_DOC = 'static/front_end/images/documents/'
UPLOAD_FOLDER_PORTFOLIO = 'static/front_end/images/portfolio/'
UPLOAD_FOLDER_CATEGORY = 'static/images/category/'

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

MAIL_SERVER = "jobwork.io"
MAIL_PORT = 25
MAIL_DEBUG = True
MAIL_USE_TLS = True
MAIL_USERNAME = 'info@jobwork.io'
MAIL_PASSWORD = 'Jobwork@123'
MAIL_DEFAULT_SENDER = ("SAVEonJOBS", "info@jobwork.io")

URL_CATEGORY = Constants.URL + UPLOAD_FOLDER_CATEGORY

SECRET_KEY = 'AIzaSyD_-qiKP3SyY1bN5GLtL_lGotvrNPoW6D4'
