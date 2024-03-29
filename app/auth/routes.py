# app/auth/routes
from app.auth.forms import *
from app.auth import auth
from flask import render_template, request, flash, redirect, url_for
from app.auth.models import Users,Profiles, SaveProfilePicture,Trades
from app.catlog.models import Books
from app.catlog.models import Publication
from app import bcrypt, sr, db
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
        Users.create_user( name ,email,  password, code_sent)
        # get user_id so as to create a blank record in profile 
        user_id = Users.query.filter_by(email = email).first().id
        #  create a blank profile info, so that the edit profile 
        Profiles.create_profile('-','-','default.jpg','-','-','-','-','-','-','-','-','-','-'
                                ,'-',user_id,'-','-','-','-','-','-','-','-')

        
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
@auth.route("/setting", methods=['GET','POST'] )
@login_required
def setting():
    form = ProfileEditForm()
    profile = Profiles.query.filter_by(user_id= current_user.id).first()
    
    return render_template("setting.html", form = form, profile = profile)

@auth.route("/setting/edit_basic", methods=['GET','POST'] )
@login_required
def edit_basic():
    form = BasicProfileForm()
    profile = Profiles.query.filter_by(user_id=current_user.id ).first()
    if form.validate_on_submit():
        if form.picture.data:
            filename = SaveProfilePicture(form.picture.data, current_user.email)
            profile.profile_picture = filename
            db.session.commit()
        current_user.name = form.name.data
        db.session.commit()
        return redirect(url_for("auth.setting"))


    return render_template("edit_basic_info.html", form = form, profile = profile)


@auth.route("/setting/edit_contact_info", methods=['GET','POST'] )
@login_required
def edit_contact_info():
    form = ContactProfileForm()
    profile = Profiles.query.filter_by(user_id = current_user.id ).first()
    if form.validate_on_submit():
        
        profile.province = form.province.data
        profile.city = form.city.data
        profile.street_address = form.address.data
        profile.phone_number_1 = form.mobile.data
        profile.business_license_number = form.bizlic.data
      
        db.session.commit()
        return redirect(url_for("auth.setting"))


    return render_template("edit_contact_info.html", form = form, profile = profile)

@auth.route("/setting/edit_about_me", methods=['GET','POST'] )
@login_required
def edit_aboutme_info():
    form = AboutMeProfileForm()
    profile = Profiles.query.filter_by(user_id = current_user.id ).first()
    form.about_me.data = profile.about_me
    form.more_about_me.data = profile.more_notes_about_me    
      
    if form.validate_on_submit():
        print([form.about_me.data, form.more_about_me.data   ])
        profile.about_me = request.form.get('about_me')
        profile.more_notes_about_me = request.form.get('more_about_me')       
      
        db.session.commit()
        return redirect(url_for("auth.setting"))


    return render_template("edit_aboutme_info.html", form = form, profile = profile)


@auth.route("/setting/edit_social_info", methods=['GET','POST'] )
@login_required
def edit_social_info():
    form = SocialProfileForm()
    profile = Profiles.query.filter_by(user_id = current_user.id ).first()
    form.instagram.data = profile.instagram
    form.facebook.data =   profile.facebook    
    form.twitter.data  = profile.twitter_x 
    if form.validate_on_submit():
        
        profile.instagram = request.form.get('instagram')
        profile.facebook = request.form.get('facebook')
        profile.twitter_x = request.form.get('twitter')

        db.session.commit()
        return redirect(url_for("auth.setting"))


    return render_template("edit_social_info.html", form = form, profile = profile, id = profile.city)


@auth.route("/setting/edit_tags", methods=['GET','POST'] )
@login_required
def edit_tags():
    form = TagsProfileForm()
    profile = Profiles.query.filter_by(user_id = current_user.id ).first()
    form.tag_1.choices = [(row.trade, row.trade) for row in Trades.query.all()]
    form.tag_2.choices = [(row.trade, row.trade) for row in Trades.query.all()]
    form.tag_3.choices = [(row.trade, row.trade) for row in Trades.query.all()]
    form.tag_4.choices = [(row.trade, row.trade) for row in Trades.query.all()]
    form.tag_5.choices = [(row.trade, row.trade) for row in Trades.query.all()]

    if form.validate_on_submit():   
        print([form.tag_1.data, form.tag_3.data])     
        profile.tags = form.tag_1.data
        profile.tags_2 = form.tag_2.data       
        profile.tags_3 = form.tag_3.data 
        profile.tags_4 = form.tag_4.data 
        profile.tags_5 = form.tag_5.data 

        db.session.commit()
        return redirect(url_for("auth.setting"))

    return render_template("edit_tags.html", form = form, profile = profile)

@auth.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("auth.home"))

@auth.route("/publishers")
def admin_publisher():
    books = Books.query.all()

    return render_template("home.html",books = books)
