class Constants(object):
    API_SECRET_KEY = 'AIzaSyD_-qiKP3SyY1bN5GLtL_lGotvrNPoW6D4'
    DEBUG = True

    STRIPE_API_KEY = 'sk_test_KkCeGZQBHsPMFhumzKA8Jhc4'
    DEFAULT_CHARGE_DESCRIPTION = "SaveonJobs Charge"

    PAYPAL_MODE = 'live'
    PAYPAL_CLIENT_ID = 'Afy9iSDAwQc9Dd36hyHYeEV0s8zH_9k7f2FzHeu-CKLQIl2bB0zlAiMUJWQXRzMW13Z9aqQs7-ujX9_X'
    PAYPAL_CLIENT_SECRET = 'ECsp60F6v1hHCNWHavrTmbzlKglvtS_0JCh8CX7vlkfV89ZSLRE6BLFs7t4xQZA_Ma7Vn3oachtdjOfc'

    ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'gif', 'JPG', 'PNG', 'JPEG', 'BMP', 'bmp', 'gif', 'GIF'}
    ALLOWED_EXTENSIONS_FILE = {'txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'JPG', 'PNG', 'JPEG', 'BMP',
                               'bmp', 'gif', 'GIF'}

    PAGE_LIMIT = 10

    FCM_API_KEY = 'AAAAtudwsIM:APA91bHK-EizhjQr8D1p60liGYW6glt1y9Y5_OIfELjCnyrJm33kFLjQ0cdVwmyh3z2-6NwUo8' \
                  'nxORgQBe3WfNi-0U_CXHHt1Msq93R4QBsvgwvRpjzmU2gxOKwTI9LdU4VYkMlOFbMm'

    # URL path
    URL = "http://jobwork.io:8080/"
    IMAGE_PATH = "static/front_end/images/profile/"
    PORTFOLIO_PATH = "static/front_end/images/portfolio/"
    DOC_PATH = "static/front_end/images/documents/"
    PROFIL_PIC_STATIC_PATH = URL + IMAGE_PATH

    UPLOAD_FOLDER_CATEGORY = 'static/images/category/'
    # Template URL
    # URL_CATEGORY = URL + UPLOAD_FOLDER_CATEGORY

    MSG_ACCOUNT_SID = "AC8e7b0d36484a9abab0d36da692d331d6"  # Your Account SID from www.twilio.com/console
    MSG_AUTH_TOKEN = "ea867a299648e094bb227a4930c5b262"  # Your Auth Token from www.twilio.com/console
    MSG_SEND_FROM = "+16572328646"

    # TODO Email Templates
    ONBOARD_EMAIL_TEMPLATE = '/emailTemplates/email_verification_template.html'
    BID_ACCTEPED_EMAIL_TEMPLATE = '/emailTemplates/Accept-bid.html'
    BID_REVERSE_EMAIL_TEMPLATE = '/emailTemplates/reverse-bid.html'
