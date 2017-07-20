from flask import Flask,render_template,request,send_file,g,current_app,url_for,redirect
from flask_googlemaps import Map
import smtplib
import folium
import datetime
from email.mime.text import MIMEText
from flask_paginate import Pagination,get_page_args
import click
from DatabaseCode import *
from DatabaseConnection import *
from math import ceil

click.disable_unicode_literals_warning=True

app=Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'DrskrPortfolio'

try:
    create_appointment_table()
    create_feedback_table()
except:
    pass


pagesList=[]
pagesURLS={}


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/home")
def start():
    return render_template('index.html')


@app.route('/appointment',methods=['GET','POST'])
def appointment():
    if request.method == 'GET':
        return render_template('appointment.html')
    elif request.method == 'POST':
        appointments=view_appointments()
        print(appointments)
        fn = str(request.form.get('firstName'))
        ln = str(request.form.get('lastName'))
        email = str(request.form.get('emailID'))
        pn = request.form.get('phoneNumber')
        dt = request.form.get('dayTime')
        if not appointments:
            id=1
        else:
            id=len(appointments)+1
        book_appointment(id,fn,ln,email,pn,dt)
        try:
            msg = MIMEText(
                'Patient First Name: ' + fn + '\t' + 'Patient Last Name ' + ln + '\n' + 'Email Address ' + email + '\n' +'Phone Number '+pn+'\n'+'Appointment needed time '+dt+'\n',
                'plain', 'utf-8')
            msg['Subject'] = 'Message from ' + fn
            msg['From'] = 'drskr.com'
            from_MailAddress = 'drsivakumarreddy@yahoo.com'
            pwd = 'Srirama1!'
            s = smtplib.SMTP("smtp.mail.yahoo.com:587")
            s.starttls()
            s.login('drsivakumarreddy@yahoo.com', 'Srirama1!')
            s.sendmail('drsivakumarreddy@yahoo.com', 'srushti.gangireddy@gmail.com', msg.as_string())
            s.quit()
        except:
            pass
        print(view_appointments())
        return render_template('index.html')

@app.route('/view_appointment',methods=['GET','POST'])
def view_appointments():
    if request.method=='GET':
        todayDate = datetime.datetime.now().date()
        appointments = appointments_by_date(todayDate)
        return render_template('appointments.html',appointments=appointments)

@app.route('/writeFeedback',methods=['GET','POST'])
def write_feedback():
    if request.method=='GET':
        return render_template('writeFeedback.html')
    elif request.method=='POST':
        name=str(request.form.get('patientName'))
        email=str(request.form.get('emailID'))
        phoneNumber=str(request.form.get('phoneNumber'))
        feedback=str(request.form.get('feedbackText'))
        id=len(view_feedbacks())+1
        writeFeedback(id,name,email,phoneNumber,feedback)
        return render_template('FeedbackSaved.html')

def viewFeedback():
    fdbs=getFeedback()
    length=len(fdbs)
    pages=int(ceil(length/float(15)))
    print(pages)
    if pages==1:
       pass
    else:
        for i in range(1,pages+1):
            print(i)
            pagesList.append(i)
            link='/displayFeedback/'+str(i)
            pagesURLS[i]=link
        print(pagesList)
        print(pagesURLS)

@app.route('/displayFeedback',defaults={'page':1})
@app.route('/displayFeedback/<int:page>')
def displayFeedback(page):
    pageNum=int(page)
    a=(page-1)*15+1
    b=(page)*15
    if len(pagesList) == 0 & len(pagesURLS) == 0:
        viewFeedback()
    feedbacks=getFeedbacks(a,b)
    print(feedbacks)
    return render_template('displayFeedback.html',fds=feedbacks,pages=pagesList,url=pagesURLS)



@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='GET':
        return render_template('index.html')
    elif request.method=='POST':
        name=str(request.form.get('name'))
        email=str(request.form.get('email'))
        subject=str(request.form.get('subject'))
        message=str(request.form.get('message'))
        print(name)
        print(email)
        msg = MIMEText(
            'Guest Message: ' + message + '\n' + 'Email address of guest: ' + email + '\n' + 'Name of Guest: ' + name,
            'plain', 'utf-8')
        msg['Subject'] = 'Message from ' + name
        msg['From'] = 'drskr.com'
        try:
            from_MailAddress = 'drsivakumarreddy@yahoo.com'
            pwd = 'Srirama1!'
            s = smtplib.SMTP("smtp.mail.yahoo.com:587")
            s.starttls()
            s.login('drsivakumarreddy@yahoo.com', 'Srirama1!')
            s.sendmail('drsivakumarreddy@yahoo.com','srushti.gangireddy@gmail.com',msg.as_string())
            s.quit()
        except:
            pass
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
