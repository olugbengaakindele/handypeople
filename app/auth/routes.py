# app/auth/routes
from app.auth.forms import *
from app.auth import auth
from flask import render_template, request, flash, redirect, url_for
from app.auth.models import Users,Profiles
from app.catlog.models import Books
from app.catlog.models import Publication
from app import bcrypt, sr
from flask_login import  login_user, logout_user,login_required, current_user
from flask_mail import  Message
from app import mail
from flask import current_app  as app
from itsdangerous import URLSafeTimedSerializer
import os
from app.auth.bespokeFunc import *



#  Home page
@auth.route("/home")
def home():
    books = Books.query.all()

    return render_template("home.html",books = books)


# registration page
@auth.route("/register", methods= ['GET','POST'])
def register():
    
    name = None
    email = None
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        code_sent = get_random_string(5)
        Users.create_user( name ,email,  password, code_sent,)

        # generate token to send to email
        # sr = URLSafeTimedSerializer(os.environ['e_data_password'])
        # token = sr.dumps(email , salt = 'email_confirm')
        # msg = Message('Confirm Email' , sender = app.config['MAIL_USERNAME'], recipients=[email])
        # link = url_for('auth.confirm_email', token = token, external= True)
        # msg.body = 'Your links is {}'.format(link)
        # mail.send(msg)
        # sendEmail(email, code_sent)
        

        flash("An email has been sent to you , please confirm by clicking on the link.", "info")
        return redirect(url_for("auth.do_the_login"))
    
    return render_template("reg.html", form = form , name = name , email = email , title ="Register")


# @auth.route("/confirm_email/<token>")
# def confirm_email(token):
#     email = sr.loads(token, salt = 'email_confirm', max_age = 10)

#     return f"Yur link is ready"
    

@auth.route("/login", methods= ['GET','POST'])
def do_the_login():
    
    name = None
    email = None
    form = LoginForm()

    if form.validate_on_submit():
        user_email = request.form['email']
        passwd = request.form['password']
        user = Users.query.filter_by(email = user_email).first()
        #  check is email exist and pasword match
        if not (user and bcrypt.check_password_hash(user.password, passwd) ):
       
            flash("Invalid credentials, please try again")

            return redirect(url_for("auth.do_the_login"))
        
        # elif user and bcrypt.check_password_hash(user.password, passwd) and user.email_confirm == False:
        #     flash("Enter the code sent to your email")
        #     return redirect(url_for("auth.confirm_email"),user_email=user_email)

        else:
            login_user(user,form.stayloggedin.data )
            return redirect(url_for("auth.home"))
    

    return render_template("login.html", form = form , name = name , email = email)


# @auth.route("/confirm_email", methods= ['GET','POST'])
# def confirm_email():
#     form = VerifyEmailForm()
# #     user = Users.query.filter_by(email = email).first()
# #     if form.validate_on_submit():
# #         email_code = request.form['code']
# #     #    if   bcrypt.check_password_hash(user.code_sent , user.code_validate)

# #     #     if form.validate_on_submit():
# #     #         user_email = request.form['email']

    
#     return render_template("confirm_email.html" , form = form)


#  Home page
@auth.route("/setting")
def home():
    books = Books.query.all()

    return render_template("setting.html",books = books)


@auth.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("auth.home"))
