from flask import request,Blueprint
import smtplib,os,hashlib,time,random,string
import http.cookies
from datetime import datetime,timedelta

'''
jw_cookies=Blueprint('jw_cookies',__name__,url_prefix='')
expiration = datetime.now() + timedelta(days=100)
@jw_cookies.route('/set', methods=['POST'])
def setCookies():
	http.cookies["session"] = random.randint(1000000000)
	http.cookies["session"]["domain"] = ".jayconrod.com"
	http.cookies["session"]["path"] = "/"
	http.cookies["session"]["expires"] = \
	expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

	return ''


@jw_cookies.route('/get', methods=['POST'])
def getCookies():
	name = request.cookies.get('name')
	cookiesLastname = request.cookies.get('cookiesLastname')
	return 'Cookies Name is ' + name + ' ' + cookiesLastname

@jw_cookies.route('/getcookies', methods=['POST'])
def see():
	print cookie.output()
	print request.cookies
	print session
	print len(session)
	# data = request.cookies
	return "data"


@jw_cookies.route('/cookiestesting', methods=['POST'])
def cookiesTest():
	settingCookies
	# assign a value
	settingCookies['raspberrypi']='Hello world'
	# set the xpires time
	settingCookies['raspberrypi']['expires']=1*1*3*60*60

	# print the header, starting with the cookie
	print settingCookies
	print "Content-type: text/html\n"

	# empty lines so that the browser knows that the header is over
	print ""
	print ""

	# now we can send the page content
	print """
	<html>
	    <body>
	        <h1>The cookie has been set</h1>
	    </body>
	</html> """

	return "success"

@jw_cookies.route('/cookiestestingretrive', methods=['POST'])
def cookiesTestRetrive():

	print "Content-type: text/html\n\n"

	print """
	<html>
	<body>
	<h1>Check the cookie</h1>
	"""

	if 'HTTP_COOKIE' in os.environ:
	    cookie_string=os.environ.get('HTTP_COOKIE')
	    settingCookies=Cookie.SimpleCookie()
	    settingCookies.load(cookie_string)
	    print settingCookies

	    try:
	        data=settingCookies['raspberrypi'].value
	        print "cookie data: "+data+"<br>"
	    except KeyError:
	        print "The cookie was not set or has expired<br>"


	print """
	</body>
	</html>

	"""
	return "success"

@jw_cookies.route('/getCook', methods=['POST'])
def getCook():
	if 'HTTP_COOKIE' in os.environ:
		print (os.environ['HTTP_COOKIE'])
		cookies = os.environ['HTTP_COOKIE']
		print (cookies)
		cookies = cookies.split('; ')
		handler = {}

	# print r.cookies
	# if r.status_code == 200:
	# 	for cookie in r.cookies:
	# 		print(cookie)

	return "success" '''
