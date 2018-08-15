from flask import request,Blueprint,jsonify
from jobwork.models.user import User
from jobwork.db_connection import db

remove_account=Blueprint('remove_account',__name__,url_prefix='')

@remove_account.route('/delete/user',methods=['POST'])
def delUser():
    email=request.json['email']

    result=User.find_one({"email":email})
    if result is not None:
        db.user.remove({"email":email})
        return jsonify({"status":200,"msg":"account deleted!"})
    else:
        return jsonify({"status": 201, "msg": "not found!"})




