from app import db,bcrypt
from datetime import datetime as dt
from app import login_manager
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    date_of_reg = db.Column(db.DateTime, default = dt.utcnow())
    email_confirm = db.Column(db.Boolean, default = False)

    @classmethod
    def create_user(cls,user_name, user_email, user_password):
        user = cls(name = user_name, email= user_email.lower(), password = bcrypt.generate_password_hash(user_password).decode('utf-8'))
        
        db.session.add(user)
        db.session.commit()

        return user
    

class Profiles(UserMixin, db.Model):
    __tablename__ = 'tbl_profiles'

    id = db.Column(db.Integer, primary_key = True)
    primary_trade = db.Column(db.String(100), nullable = False)
    about_me = db.Column(db.String(1000), nullable = False)
    profile_picture = db.Column(db.String(100))
    sex = db.Column(db.String(100),nullable =False)
    business_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    street_address = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    email_address =  db.Column(db.String(50))
    phone_number_1 = db.Column(db.String(50))
    business_license_number = db.Column(db.String(50))
    more_notes_about_me = db.Column(db.String(50))
    userd_id = db.Column(db.Integer, db.ForeignKey('tbl_users.id'))

    @classmethod
    def









    @classmethod
    def create_user(cls,user_name, user_email, user_password):
        user = cls(name = user_name, email= user_email.lower(), password = bcrypt.generate_password_hash(user_password).decode('utf-8'))
        
        db.session.add(user)
        db.session.commit()

        return user





    
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


