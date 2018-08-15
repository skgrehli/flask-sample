from flask import request, Blueprint, make_response, jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.user import User

user_bank = Blueprint('user_bank', __name__, url_prefix='/bank')


@user_bank.route('/fetch', methods=['POST'])
@authentication
def bank_fetch():
    try:
        userid = int(request.json['userid'])
        response = User.find_one({"userid": userid}, {"_id": 0, "paypal_id": 1})
       # response = User.find_one({"userid": userid}, {"_id": 0})
        return make_response(jsonify({"bank_details":response,"status":200}), 200)

    except Exception as e:
        print(e)
        return make_response(jsonify({"status": 500, "message": "Something went wrong, Please try again!"}), 500)


@user_bank.route('/update', methods=['POST'])
@authentication
def bank_update():
    try:
        userid = int(request.json['userid'])

        user_details = User.find_one({"userid": userid}, {"_id": 0})
        bank_details = []
        if user_details:
            User.update({"userid": userid}, {"$set": {"paypal_id": request.json['paypal_id']}})

            bank_details = User.find_one({"userid": userid}, {"_id": 0, "paypal_id": 1})

        return make_response(jsonify({"status": 402, "message": "User not Connected", "bank_details": bank_details}),
                             200)

    except Exception as e:
        return make_response(jsonify({"status": 500, "message": "Something went wrong, Please try again!"}), 500)
