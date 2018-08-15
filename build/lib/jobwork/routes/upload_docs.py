from flask import request,jsonify,Blueprint
from datetime import datetime,timedelta
from jobwork.middleware.authentication import authentication
from jobwork.models.user import User
from jobwork.constants import Constants
import calendar
from werkzeug.utils import secure_filename
import os
from jobwork.utils.common_utils import CommonUtils
from jobwork.models.certificate import Certificate
from jobwork.models.userportfolio import UserPortfolio

URL = Constants.URL
imagePath = Constants.IMAGE_PATH


def allowed_file_image(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in Constants.ALLOWED_EXTENSIONS_IMAGE

def allowed_file_doc_pdf(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in Constants.ALLOWED_EXTENSIONS_FILE


jw_upload=Blueprint('jw_upload',__name__,url_prefix='')

@jw_upload.route('/user/update/pic/doc/certificate/portfolio/upload',methods=['POST'])
@authentication
def user_update_image():
	try :
		userid = int(request.form['userid'])
		token = request.form['token']

		secdatetime 			= datetime.utcnow() - timedelta(minutes=1)
		createdatetimeinseconds = calendar.timegm(secdatetime.utctimetuple())

		findUser = User.find_one({"userid" : userid, "token": token, "active":True})
		certificateJSON = findUser['certificateJSON']

		if findUser is not None:
			print (request.form['type'])
			# Profile Pic Upload
			if request.form['type'] == "profileimage":
				file = request.files['myimage']
				fileNameContain = str(userid) + str(findUser['salt']) + "profile_" + str(createdatetimeinseconds)
				if file and allowed_file_image(file.filename):
					print (file.filename)
					filename = secure_filename(file.filename)
					ext = file.filename.rsplit('.', 1)[1]
					filename = fileNameContain + "." + ext
					file.save(os.path.join(jw_upload.config['UPLOAD_FOLDER_PROFILE'], filename))
					User.update({ 'userid':userid,'token':token},{"$set":{'picurl':filename}})
					profilePic = URL+imagePath+filename
					message={'status':200, 'message':'Image successfully uploaded', "profilePic":profilePic}

			# Police Documents Upload
			if request.form['type'] == "police":
				file = request.files['myimage']
				fileNameContain = str(userid) + str(findUser['salt']) + "police_" + str(createdatetimeinseconds)
				if file and (allowed_file_image(file.filename) or allowed_file_doc_pdf(file.filename)):
					filename = secure_filename(file.filename)
					ext = file.filename.rsplit('.', 1)[1]
					filename = fileNameContain + "." + ext
					file.save(os.path.join(jw_upload.config['UPLOAD_FOLDER_DOC'], filename))
					proDocuments = URL+Constants.DOC_PATH+filename
					certificateJSONDATA = {"type":ext, "certificateid":CommonUtils.generateRandomNo(Certificate,"certificateid"),"certificateimageurl":filename,"certificatestatus":"pending","certificatecaption":request.form['certificatecaption'],"ispoliceverification":True}
					certificateJSON.append(certificateJSONDATA)
					User.update({ 'userid':userid,'token':token},{"$set":{'certificateJSON':certificateJSON}})
					message={'status':200, 'message':'Image successfully uploaded', "certificateJSON":certificateJSON}

			# Pro Documents Uploads
			if request.form['type'] == "certificateimage":
				file = request.files['myimage']
				fileNameContain = str(userid) + str(findUser['salt']) + "pro_docs_" + str(createdatetimeinseconds)
				if file and (allowed_file_image(file.filename) or allowed_file_doc_pdf(file.filename)):
					filename = secure_filename(file.filename)
					ext = file.filename.rsplit('.', 1)[1]
					filename = fileNameContain + "." + ext
					file.save(os.path.join(jw_upload.config['UPLOAD_FOLDER_DOC'], filename))
					proDocuments = URL+Constants.DOC_PATH
					certificateJSONDATA = {"type":ext, "certificateid":CommonUtils.generateRandomNo(Certificate,"certificateid"),"certificateimageurl":filename,"certificatestatus":"pending","certificatecaption":request.form['certificatecaption'],"ispoliceverification":False}
					certificateJSON.append(certificateJSONDATA)
					User.update({ 'userid':userid,'token':token},{"$set":{'certificateJSON':certificateJSON}})
					message={'status':200, 'message':'Image successfully uploaded', "certificateJSON":certificateJSON}

			# Portfolio Images Uploads
			if request.form['type'] == "portfolioimage":
				file = request.files['myimage']
				fileNameContain = str(userid) + str(findUser['salt']) + "portfolio_" + str(createdatetimeinseconds)
				if file and allowed_file_image(file.filename):
					filename = secure_filename(file.filename)
					ext = file.filename.rsplit('.', 1)[1]
					filename = fileNameContain + "." + ext
					file.save(os.path.join(jw_upload.config['UPLOAD_FOLDER_PORTFOLIO'], filename))
					portfolioDataPath = URL+Constants.PORTFOLIO_PATH
					UserPortfolio.insert({"portfolioid":CommonUtils.generateRandomNo(UserPortfolio,"portfolioid"),
											"portfolioimage":filename,
											"userid":userid,
											"active":True,
											"createddatetime":datetime.now(),
											"updatedatetime":datetime.now()})
					portfolioData = list(UserPortfolio.find({"userid":userid,"active":True,},{"_id":0}))
					message={'status':200, 'message':'Image successfully uploaded', "portfolioData":portfolioData, "portfolioDataPath":portfolioDataPath}

			User.update({"userid" : userid, "token": token, "active":True},{"$set":{"updateddatetime":datetime.now()}})

			return jsonify(message)
		else:
			return jsonify({"status":402,"message":"No User found."})

	except Exception as e:
		return jsonify({"status":500,"message":e.message})



