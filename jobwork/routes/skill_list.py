from flask import Blueprint,request,make_response,jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.skills import Skills

skill_list=Blueprint('skill_list',__name__,url_prefix='')



@skill_list.route('/skills/all/list',methods=['POST'])
@authentication
def skills_all_list():
	userid = int(request.json['userid'])
	token = request.json['token']

	# Authenticate credentials
	skillsList = list(Skills.find({},{"_id":0,"skillid":1,"skillname":1}).sort("skillname",1))

	if len(skillsList) > 0:
		return jsonify({"status" : 200, "message" : "Skills Data.", "skillsList":skillsList})
	else:
		return jsonify({"status" : 200, "message" : "No Data.", "skillsList":[]})


