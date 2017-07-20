import os
import urlparse
import psycopg2
from DatabaseConnection import *

def create_appointment_table():
    curs=conn.cursor()
    curs.execute("create table if not exists APPOINTMENT(Id INTEGER,FirstName text,LastName text,EmailAddress text,PhoneNumber text,Date date)")
    conn.commit()

def create_feedback_table():
    curs=conn.cursor()
    curs.execute("create table if not exists FEEDBACK(Id INTEGER,PatientName text,EmailAddress text,PhoneNumber text,feedback text)")
    conn.commit()

def writeFeedback(id,pn,email,phone,fd):
    curs=conn.cursor()
    curs.execute("insert into FEEDBACK values(%s,%s,%s,%s,%s)",(id,pn,email,phone,fd))
    conn.commit()

def view_feedbacks():
    curs=conn.cursor()
    curs.execute("select * from FEEDBACK")
    rows=curs.fetchall()
    return rows

def book_appointment(id,fn,ln,email,pn,date):
    curs=conn.cursor()
    curs.execute("insert into APPOINTMENT values(%s,%s,%s,%s,%s,%s)",(id,fn,ln,email,pn,date))
    conn.commit()

def view_appointments():
    curs=conn.cursor()
    curs.execute("select * from APPOINTMENT")
    rows=curs.fetchall()
    return rows

def appointments_by_date(date):
    curs=conn.cursor()
    curs.execute("select * from APPOINTMENT where date>=%s",(date,))
    appointments=curs.fetchall()
    return appointments

def getFeedback():
    curs=conn.cursor()
    curs.execute("select * from FEEDBACK")
    feedback=curs.fetchall()
    return feedback

def getFeedbacks(a,b):
    curs=conn.cursor()
    curs.execute("select * from FEEDBACK where id between %s and %s",(a,b))
    rows=curs.fetchall()
    return rows

def fetchFeedback(num):
    curs=conn.cursor()
    curs.execute("select * from FEEDBACK where id>%s limit 10",(num,))
    feedbacks=curs.fetchall()
    return feedbacks