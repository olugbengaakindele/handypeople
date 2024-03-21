from flask_wtf import FlaskForm
from wtforms import  FileField,TextAreaField,DateField, SelectField,StringField, SubmitField, PasswordField,EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired,Email,Length,ValidationError
from app.auth.models import Users
from flask_wtf.file import FileField, FileAllowed


def email_check_for_reg(form,field):
    user = Users.query.filter_by(email = field.data).first()
    if user :
        raise ValidationError("Email exist, please login into your account") 


def email_check_for_login(form,field):
    user = Users.query.filter_by(email = field.data).first()
    if not user :
        raise ValidationError("Invalid credentials, please check that email and password are correct") 

class RegistrationForm(FlaskForm):
    name = StringField("What is your name")
    email = EmailField("What is your email", validators=[DataRequired(), Length(5,100),Email(),email_check_for_reg])
    password = PasswordField("Enter a password", validators=[Length(5,20, message="must be 5 to 20 chracters")])
    submit  = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("What is your email", validators=[DataRequired(), Length(5,100),email_check_for_login])
    password = PasswordField("Enter a password")
    stayloggedin = BooleanField("stay logged in?")
    submit  = SubmitField("Login")


class PublisherForm(FlaskForm):
    name = StringField("Publisher Name", validators=[DataRequired(), Length(5,100)])
    submit  = SubmitField("Submit")


class BookForm(FlaskForm):
    name = StringField("Book Title", validators=[DataRequired(), Length(5,100)])
    pages = IntegerField("Number of pages",  validators=[DataRequired()])
    author = StringField("Book Author", validators=[DataRequired(), Length(5,100)])
    rating = IntegerField("Average Rating (1 - 10)")
    pub_date = DateField("Publication Date")
    format = SelectField("Book Format", choices=[("Hard cover","Hard cover"),("Papper back","Papper back")])
    publisher = SelectField("Publisher", choices=[])
    submit  = SubmitField("Submit") 

class VerifyEmailForm(FlaskForm):
    code = StringField("Enter Code", validators=[DataRequired(), Length(5,10)])
    submit  = SubmitField("Submit") 
   
class ProfileEditForm(FlaskForm):
    primary_trade = TextAreaField("Primary Trade", validators=[DataRequired(), Length(5,100)])
    about_me = IntegerField("Number of pages",  validators=[DataRequired()])
    author = StringField("Book Author", validators=[DataRequired(), Length(5,100)])
    profile_picture = IntegerField("Average Rating (1 - 10)")
    sex = DateField("Publication Date")
    business_name = SelectField("Book Format", choices=[("Hard cover","Hard cover"),("Papper back","Papper back")])
    first_name = SelectField("Publisher", choices=[])
    last_name  = SubmitField("Submit") 
    city = StringField("Book Author", validators=[DataRequired(), Length(5,100)])
    province = IntegerField("Average Rating (1 - 10)")
    stree_address = DateField("Publication Date")
    postal_code = SelectField("Book Format", choices=[("Hard cover","Hard cover"),("Papper back","Papper back")])
    phone_number= SelectField("Publisher", choices=[])
    business_license_number  = SubmitField("Submit") 
    more_notes_about_me = IntegerField("Number of pages",  validators=[DataRequired()])

class BasicProfileForm(FlaskForm):
    name = StringField("Your Preferred Name")
    email = EmailField("What is your email", validators=[DataRequired(), Length(5,100),Email(),email_check_for_reg])
    sex = StringField("Your Sex")
    trade = StringField("Your Primary Trade")
    picture= FileField("Update Profile Picture", validators=[FileAllowed(['jpg','png','svg'])] )
    submit  = SubmitField("Update info") 


