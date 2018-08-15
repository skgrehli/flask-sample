
from jobwork.models.user import User
from jobwork.db_connection import db



def userDataResponse(email):
    #return jsonify({"ok": "k"})
    user = list(User.find({"email": email}, {"_id": 0}))


    response = dict()
    response.update({'userid': user[0]['userid']})
    response.update({'firstname': user[0]['firstname']})
    response.update({'lastname': user[0]['lastname']})
    response.update({'gender': user[0]['gender']})
    #response.update({'addressJSON': user[0]['addressJSON']})
    response.update({'registeredfrom': user[0]['registeredfrom']})
    response.update({'email': user[0]['email']})
    response.update({'picurl': user[0]['picurl']})
    response.update({'token': user[0]['token']})

    if user[0]['addressJSON']['city'] != '':
        city=list(db.city.find({"cityid":user[0]['addressJSON']['city']},{"_id":0}))
        response.update({"city":city[0]['city']})
    else:
        response.update({"city":""})


    if user[0]['addressJSON']['state'] != '':
        state = list(db.state.find({"stateid": user[0]['addressJSON']['state']}, {"_id": 0}))

        response.update({"state": state[0]['state']})
    else:
        response.update({"state": ""})

    if user[0]['addressJSON']['country'] != '':
        country = list(db.country.find({"countryid": user[0]['addressJSON']['country']}, {"_id": 0}))

        response.update({"country": country[0]['country']})
    else:
        response.update({"country": ""})
    #return response

    response.update({'address1':user[0]['addressJSON']['address1']})
    response.update({'address2': user[0]['addressJSON']['address2']})
    response.update({'pincode': user[0]['addressJSON']['pincode']})


    response.update({'registeredfrom': user[0]['registeredfrom']})
    response.update({'emailverified': user[0]['emailverified']})
    return response



