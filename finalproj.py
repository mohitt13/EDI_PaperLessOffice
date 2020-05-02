"""
author - Mohit.
"""

from flask import Flask, request, redirect, render_template
import io
import PyPDF2
import os
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
root = os.getcwd()


file = "m"
client = pymongo.MongoClient(
        "mongodb+srv://mohit13:vitsucks13@m13-kpbkz.mongodb.net/test?retryWrites=true&w=majority")
db = client.trail
coll = db.test

@app.route('/' , methods=['GET', 'POST'])
def first_page():
    return render_template('first.html')
    


@app.route('/redirect', methods=['GET', 'POST'])
def redirect():
    if request.form['action']=='User':
        return render_template('Frontend.html')
    if request.form['action']=='Admin':
        return render_template('adminfp.html')


@app.route('/newUser',methods=['GET','POST'])
def NewUser():
    if request.form['submit']=='signup':
        name = request.form['name']
        password = request.form['pass']
        aadhar = request.form['aadhar']
        client = pymongo.MongoClient(
        "mongodb+srv://mohit13:vitsucks13@m13-kpbkz.mongodb.net/test?retryWrites=true&w=majority")
        db = client.trail
        user = db.user
        post = {
            "_id":aadhar,
            "name":name,
            "pass":password
        }
        user.insert_one(post)
    elif request.form['submit']=='login':
        return render_template('Frontend.html')
    return render_template('Frontend.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.form['Login']=='login':
        global file
        file = request.form['id']
        return render_template('upload_page.html')
    elif request.form['Login']=='signup':
        return render_template('registration.html')

    return render_template('Frontend.html')


@app.route('/pdf_upload', methods=['GET', 'POST'])
def pdf_upload():
    global coll
    doc =[]
    if request.method == 'POST':
        files = request.files.getlist('file')
        for fileup in files:
            content = fileup.read()

            pdf = PyPDF2.PdfFileReader(io.BytesIO(content))
            count = 0
            text = ""
            num_pages = pdf.numPages
            name = fileup.filename
            while count < num_pages:
                pageObj = pdf.getPage(count)
                count += 1
                text += pageObj.extractText()

            name = name[:-4]
            # uploadfile = open("new.txt","w")
            # uploadfile.write(text)
            # uploadfile.close()
            doc.append(text)
            
        def insertdoc(pt):
            data ={
                "_id":file,
                "docs": pt
            }
            coll.insert_one(data)
        insertdoc(doc)
    return render_template('upload_page.html')


@app.route('/AdminLogin', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        AdminId = request.form['Aid']
    return render_template('adminSp.html')

@app.route('/verify', methods=['GET','POST'])
def verify_user():
    collection = db.user
    if request.form['ud']=='User List':
        data =[]
        for x in collection.find({},{ "_id": 1 , "name":1}):
            data.append(x)

        return render_template('onclick_list.html',data=data)
    elif request.form['ud']=='Verify Documents': 
        return render_template('Fetch.html')

if __name__ == '__main__':
    app.run(debug=True)
