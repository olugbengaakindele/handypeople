from app import create_app, db
from app.auth.models import Users, Profiles


if __name__ =="__main__":

    flask_app = create_app("dev")

    with flask_app.app_context():
        db.create_all()

        if not Users.query.filter_by(email = "akin@gmail.com").first():
            Users.create_user("Olugbenga","akin@gmail.com", "secret", 'CYTP')

        if not Profiles.query.filter_by(id = 1).first():
            Profiles.create_profile(
                'Electrician', 
                'I am an eletrician' 
                ,'default.jpg'
                ,'M'
                ,'APT Electricity'
                ,'Olu'
                ,'Femikau'
                ,'Ontario'
                ,'Oshawa'
                ,'902 King street'
                ,'L4B3Ty'
                ,'4025897988'
                ,'T76YUH77787'
                ,'When you create a professional profile.'
                ,1
            )


    flask_app.run(debug=True)