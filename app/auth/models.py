from app import db,bcrypt
from datetime import datetime as dt
from app import login_manager
from flask_login import UserMixin
import os

class Users(UserMixin, db.Model):
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(200), nullable = False)
    date_of_reg = db.Column(db.DateTime, default = dt.utcnow())
    email_confirm = db.Column(db.Boolean, default = False)
    code_sent =db.Column(db.String(200))
    code_validate = db.Column(db.String(200), default= 'X')

    def __init__(self, name, email,password,code_sent):
        self.name = name
        self.password = password
        self.email = email
        self.code_sent = code_sent


    def __repr__(self):
        return f'You have created an accocunt'

    @classmethod
    def create_user(cls,user_name, user_email, user_password,code_sent):
        user = cls(name = user_name, email= user_email.lower()
                    , password = bcrypt.generate_password_hash(user_password).decode('utf-8')
                    ,code_sent= bcrypt.generate_password_hash(code_sent).decode('utf-8'))
        db.session.add(user)
        db.session.commit()

        return user
    

class Profiles(UserMixin, db.Model):
    __tablename__ = 'tbl_profiles'

    id = db.Column(db.Integer, primary_key = True)
    primary_trade = db.Column(db.String(100))
    about_me = db.Column(db.String(1000))
    profile_picture = db.Column(db.String(100), default ='default.jpeg')
    sex = db.Column(db.String(100))
    business_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    street_address = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    phone_number_1 = db.Column(db.String(50))
    business_license_number = db.Column(db.String(50))
    more_notes_about_me = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_users.id'))
    tags = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    facebook =  db.Column(db.String(100))
    twitter_x = db.Column(db.String(100))
    tags_2= db.Column(db.String(100))
    tags_3 = db.Column(db.String(100))
    tags_4 = db.Column(db.String(100))
    tags_5 = db.Column(db.String(100))


    @classmethod
    def create_profile(cls, pri_trade,abt_me, profile_picture ,sex, biz_name, f_name,l_name, prov, city, str_add,
                       ps_code,  ph_num1,biz_lic_num, more_notes,user_id, tags, insta, facebook, twitter, tag_2,tag_3,tag_4,tag_5):
        
        user_profile = cls(
                            primary_trade = pri_trade,
                            about_me = abt_me,
                            profile_picture = profile_picture ,
                            sex = sex, 
                            business_name = biz_name, 
                            first_name = f_name,
                            last_name = l_name, 
                            province = prov, 
                            city =city, 
                            street_address = str_add,
                            postal_code = ps_code, 
                            phone_number_1 =ph_num1,
                            business_license_number= biz_lic_num, 
                            more_notes_about_me = more_notes,
                            user_id = user_id,
                            tags = tags,
                            instagram = insta,
                            facebook = facebook,
                            twitter_x = twitter,
                            tags_2 = tag_2,
                            tags_3 = tag_3,
                            tags_4 = tag_4,
                            tags_5 = tag_5

        )

        db.session.add(user_profile)
        db.session.commit()

        return user_profile


class Trades(UserMixin, db.Model):
    __tablename__ = 'tbl_trades'

    id = db.Column(db.Integer, primary_key = True)
    trade = db.Column(db.String(250))

    def __init__(self,trade):
        self.trade = trade

    def _repr__(self):
        return "trade has been created"


    @classmethod
    def create_trade(cls,trade):
        trade = cls(trade =trade)
        
        db.session.add(trade)
        db.session.commit()

        return trade


def SaveProfilePicture(picture, email):

    _,f_ext = os.path.splitext(picture.filename)
    filename = f'{email}{f_ext}' 
    current_dir = os.getcwd()
    # app_folder = os.path.abspath(os.path.join(current_dir, os.pardir))
    app_folder = os.path.join(os.getcwd(),'app','static', 'profile_image')
    file_path = os.path.join(app_folder, filename) 
    picture.save(file_path)

    return filename


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


