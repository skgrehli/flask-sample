# noinspection SpellCheckingInspection
class SignupUtils(object):
    @classmethod
    def get_signup_json(cls, email, mobile="", fbid="", fbaccesstoken="", googleid="", googletoken=""):
        return {
            "email": email,
            "mobile": mobile,
            "fbid": fbid,
            "fbaccesstoken": fbaccesstoken,
            "googleid": googleid,
            "googletoken": googletoken,
        }

    @classmethod
    def get_user_address_json(cls, city_id):
        if city_id:
            from jobwork.models.city import CityCollections
            citydetail = CityCollections.find_one({"cityid": city_id}, {"_id": 0})
            # statedetail = StateCollections.find_one({"stateid": citydetail['stateid']}, {"_id": 0})
            from jobwork.models.country import CountryCollections
            countrydetail = CountryCollections.find_one({"countryid": citydetail['countryid']}, {"_id": 0})
            return {
                "address1": "",
                "address2": "",
                "city": city_id,
                "state": citydetail['stateid'],
                "country": countrydetail['countryid'],
                "pincode": ""
            }
        else:
            return {
                "address1": "",
                "address2": "",
                "city": "",
                "state": "",
                "country": "",
                "pincode": ""
            }

    @classmethod
    def get_pro_json(cls):
        return {
            "facebookapproved": False,
            "policeverification": False,
            "mobileverified": False,
            "creditcardverified": False,
            "professionalcertificationverified": False,
            "overallPro": False
        }

    @classmethod
    def get_payment_detail_json(cls):
        return {
            "bankname": "",
            "bankaccountname": "",
            "bankaccountnumber": "",
            "banktransitnumber": ""
        }
