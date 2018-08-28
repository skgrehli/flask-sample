from functools import wraps
from flask import request, make_response, jsonify
from jobwork.models.user import User


def authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.json.get('userid', False) == False or request.json.get('token', False) == False:
            return make_response(jsonify({"status": 400, "message": "1 Authentication keys are missing."}), 400)
        userid = int(request.json['userid'])
        token = request.json['token']
        result = User.find_one({"userid": int(userid), "token": str(token)})
        if not result:
            return make_response(jsonify({"status": 401, "message": " No mach found.","error":True,"response":[]}), 401)
        else:
            return f(*args, **kwargs)

    return decorated_function
