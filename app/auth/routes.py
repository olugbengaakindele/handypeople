# app/auth/routes
from app.auth.forms import *
from app.auth import auth
from flask import render_template, request, flash, redirect, url_for
from app.auth.models import Users
from app.catlog.models import Books
from app.catlog.models import Publication
from app import bcrypt
from flask_login import  login_user, logout_user,login_required, current_user


#  Home page
@auth.route("/home")
def home():
    books = Books.query.all()

    return render_template("home.html",books = books)


# registration page
@auth.route("/register", methods= ['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for("auth.home"))
    name = None
    email = None
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        Users.create_user( name ,email,  password )
        flash("You have successfully created an account with us", "info")
        return redirect(url_for("auth.do_the_login"))
    
    return render_template("reg.html", form = form , name = name , email = email , title ="Register")


@auth.route("/login", methods= ['GET','POST'])
def do_the_login():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for("auth.home"))
     
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

        login_user(user,form.stayloggedin.data )
        return redirect(url_for("auth.home"))
    

    return render_template("login.html", form = form , name = name , email = email)


@auth.route("/admin/publisher", methods= ['GET','POST'])
@login_required
def admin_publisher():
    form = PublisherForm()
    if form.validate_on_submit():
        name = request.form["name"]
        user = Publication.create_publisher(name)
        flash("You have created a publisher")
        return redirect(url_for("auth.admin_publisher"))

    return render_template("publisher_add.html" , form = form)


@auth.route("/admin/books", methods= ['GET','POST'])
@login_required
def admin_books():
    form = BookForm()
    pubs  = Publication.query.all()
    pub_form = [(pb.id, pb.name) for pb in pubs ]
    form.publisher.choices = pub_form

    return render_template("book_add.html" , form = form)





@auth.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("auth.home"))
