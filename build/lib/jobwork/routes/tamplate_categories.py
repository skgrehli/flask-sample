from flask import Blueprint,request,make_response,jsonify
from jobwork.middleware.authentication import authentication
from jobwork.models.categories import Categories
from jobwork.models.templates import Templates
from jobwork.constants import Constants

tempcat=Blueprint('tempcat',__name__,url_prefix='')

URL_CATEGORY = Constants.URL + Constants.UPLOAD_FOLDER_CATEGORY


@tempcat.route('/templates/categories/list', methods=['POST'])
def templates_categories_list():
    templatesArray = []
    templatesDic = {}
    categoriesList = list(Categories.find({},{"_id":0,"categoryid":1,"categoryname":1,"categoryimage":1}).sort("categoryname",1))
    templatesList = list(Templates.aggregate([{"$group" : {"_id" : "$categoryid"}}]))
    if len(templatesList) > 0:
        for templatesListData in templatesList:
            categoryName = Categories.find_one({"categoryid":int(templatesListData['_id'])},{"_id":0,"categoryid":1,"categoryname":1,"categoryimage":1})
            ''' no category image in template'''
            if categoryName is not None:
                tempData = list(Templates.find({"categoryid":int(templatesListData['_id'])},{"_id":0}))
                return jsonify({"ok": list(categoryName)})
                print(tempData)
                categoryData = {"categoryname":categoryName['categoryname'], "categoryimage":URL_CATEGORY+categoryName['categoryimage'], "tempData":tempData}
                templatesListData.update(categoryData)
                #return jsonify({"ok": 1})

                templatesArray.append(templatesListData)
        templatesDic['result'] = templatesArray
        return jsonify({"status" : 200, "message" : "Templates Data.", "templatesData":templatesArray, "categoriesList":categoriesList, "URL_CATEGORY":URL_CATEGORY})
    else:
        return jsonify({"status" : 200, "message" : "No Data.", "templatesData":[], "categoriesList":[]})


@tempcat.route('/categories/list/data', methods=['POST'])
def categories_list_data():
	templatesArray = []
	templatesDic = {}
	templatesList = list(Templates.aggregate([{"$group" : {"_id" : "$categoryid"}}]))
	if len(templatesList) > 0:
		for templatesListData in templatesList:
			categoryName = Categories.find_one({"categoryid":int(templatesListData['_id'])},{"_id":0,"categoryid":1,"categoryname":1,"categoryimage":1})
			if categoryName is not None:
				tempDataCollection = list(Templates.find({"categoryid":int(templatesListData['_id'])},{"_id":0, "title":1}))
				exampleName = "eg. "
				countData = 0
				for collections in tempDataCollection:
					if countData == 0:
						exampleName = exampleName +collections['title']
					else:
						exampleName = exampleName +", "+collections['title']
					countData = countData + 1
				categoryData = {"categoryname":categoryName['categoryname'],"categoryimage":URL_CATEGORY+categoryName['categoryimage'],"tempData":exampleName}
				templatesListData.update(categoryData)
				templatesArray.append(templatesListData)
		templatesDic['result'] = templatesArray
		return jsonify({"status" : 200, "message" : "Categories Data.", "templatesData":templatesArray, "URL_CATEGORY":URL_CATEGORY})
	else:
		return jsonify({"status" : 200, "message" : "No Data.", "templatesData":[], "categoriesList":[]})
