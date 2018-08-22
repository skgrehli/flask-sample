import os
from flask import Flask, request, redirect, url_for,Blueprint,jsonify,render_template
from werkzeug.utils import secure_filename
from jobwork.constants import Constants

UPLOAD_FOLDER = '/static/jobdocument/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#APP_ROOT=os.path.dirname(os.path.abspath(__file__))

upload_doc=Blueprint('upload',__name__,url_prefix='')


@upload_doc.route('/upload')
def uploader():
    return render_template('addjob.html')



@upload_doc.route('/upload/file', methods=["GET",'POST'])
def upload_file():
    target=os.path.join(Constants.APP_ROOT,'static/jobdocument/')
    if request.method == 'POST':
        #file = request.files['file']
        index=0
        userid=request.form['userid']
        token=request.form['token']
        jobtitle=request.form['jobtitle']
        jobdescription=request.form['description']
        personseleted=request.form['personselected']
        totalbudget=request.form['totalbudget']
        budgettype=request.form['budgettype']
        cityid=request.form['cityid']
        locationid=request.form['locationid']
        draft=request.form['draft']
        date=request.form['date']

        print(jobtitle)
        for file in request.files.getlist("file"):

            print(file)
           # f.save(secure_filename(f.filename))
            #filename = secure_filename(file.filename)
            filename=jobtitle+".jpg"
            destination="/".join([target,filename])
            file.save(destination)
            index=index+1
        return 'file uploaded successfully'
