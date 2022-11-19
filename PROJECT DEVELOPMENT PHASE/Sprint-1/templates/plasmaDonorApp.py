from flask import Flask, render_template, request, redirect, url_for, session,g
from flask import *
from turtle import st
#from markupsafe import escape
import os
from flask_session import Session

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;bin:db2;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cds31886;PWD=y3WNXnvFWuv0ByEE",'','')



app = Flask(__name__)
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)

if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value" 
    

@app.route('/')
def index():
    return render_template('/signin.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin',methods=['GET', 'POST'])
def signin():
    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/home',methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/fromsignup', methods = ['POST', 'GET'])
def fromsignup():  


    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
       # pin = request.form['pin']

        sql = "SELECT * FROM SIGNUP_TABLE WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        #enter sign in page from the sign-up page if user already exist--check by email address only
        

        if account:
            #flash("User already exists,please sign in directly..")
            return render_template('signin.html', msg="You are already a member, please login using your details")
        
        #enter dashboard if new user registers for first time

        else:
            insert_sql = "INSERT INTO SIGNUP_TABLE VALUES (?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            #ibm_db.bind_param(prep_stmt, 4, pin)
            ibm_db.execute(prep_stmt) 
            
        #flash("Registration successful..")    
        return render_template('signin.html', msg="Register success..Please login ito app now..")

@app.route('/fromsignin', methods = ['POST', 'GET'])
  
def fromsignin():

    if request.method == 'POST':

        session.pop('user',None)
        #name and confirm password are not in sign in page form
        #name = request.form['name']
        email = request.form['email']
        password = request.form['password']
       # pin = request.form['pin']

        userslist = []
        sql = "SELECT * FROM SIGNUP_TABLE WHERE email=? AND password=?"
        stmt=ibm_db.prepare(conn,sql) 
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        #stmt = ibm_db.exec_immediate(conn, sql) 
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            # print ("The Name is : ",  dictionary)
            userslist.append(dictionary)
            #fetched_name=dictionary[0] ...table colums-- name,email,password
            session['user']=dictionary[0] 
            session['email']=dictionary[1] 
            session['password']=dictionary[2]

            dictionary = ibm_db.fetch_both(stmt)
        if userslist:            
            if g.user:   
                #flash("Login successful..")            
                return render_template('profile.html', user=session['user'],email=session['email'],password=session['password'],msg="Login successful..") 
            
        else:
            sql2 = "SELECT * FROM SIGNUP_TABLE WHERE email =?"
            stmt2 = ibm_db.prepare(conn, sql2)
            ibm_db.bind_param(stmt2,1,email)        
            ibm_db.execute(stmt2)
            account2 = ibm_db.fetch_assoc(stmt2) 
            if account2: 
                #flash("Re-enter password correctly..")                          
                return render_template('signin.html', msg="Wrong Password!!Reneter") 
        #flash("Register before signing in..")    
        return render_template('signup.html', msg="Register now!And then sign in..")


@app.route('/change_password',methods = ['POST', 'GET']) 
  
def change_password(): 
    if request.method == 'POST':

        newpassword = request.form['newpass']
      
        sql = "UPDATE SIGNUP_TABLE SET password=? WHERE email=? "
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,newpassword) 
        ibm_db.bind_param(stmt,2,session['email'])
        
        ibm_db.execute(stmt)
        
        session['password']=newpassword 
        #flash("Password updated successfully!!")    

    
    return render_template('profile.html', user=session['user'],email=session['email'],password=session['password'],msg="Password updated successfully") 
            

@app.before_request 
def before_request():
    g.user=None 

    if 'user' in session:
        g.user=session['user'] 

@app.route('/dropsession') 
def dropsession():
    session.pop('user',None) 
    return render_template('signin.html')


"""Chrissy code"""
"""def data():
  
    if request.method == 'POST':
        form_data = request.form
        if request.form.get('email')=="abc@gmail.com" and request.form.get('password')=="abc":
            session["email"] = request.form.get("email")
            return render_template('dashboard.html',form_data = form_data,error=False)
        
        else:
            return render_template('/signin.html',error=True)
    elif request.method == 'GET':
        if not session.get("email"):
            return f"Access Denied"
        else:
            return render_template('home.html')"""
"""Chrissy code"""