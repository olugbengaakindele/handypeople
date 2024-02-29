from app import db
from datetime import datetime as dt 




class Publication(db.Model):
    __tablename__ = "publication"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

    def __init__(self, name):
        self.name = name 

    def __repr__(self):        
        return f'You have successfullly created {self.name} in the database'

    @classmethod
    def create_publisher(cls, pub_name):
        pub = cls(name = pub_name )
        
        db.session.add(pub)
        db.session.commit()

        return pub



class Books(db.Model):
    __tablename__ = 'book'

    id  = db.Column(db.Integer,primary_key = True )
    title = db.Column(db.String(80), nullable= False)
    pages = db.Column(db.Integer, nullable= False)
    author = db.Column(db.String(80), nullable= False)
    avg_rating = db.Column(db.Float, nullable= False)
    pub_date = db.Column(db.DateTime, default = dt.utcnow() ,nullable= False)
    format = db.Column(db.String(80), nullable= False)
    image = db.Column(db.String(80), nullable= False)
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self,title, pages, author, avg_rating, pub_date, format, image, pub_id ):
        self.title = title
        self.pages = pages
        self.author = author
        self.avg_rating = avg_rating
        self.pub_date = pub_date
        self.format = format
        self.image = image
        self.pub_id = pub_id
    
    def __repr__(self):
        return "You have added a book to a publisher"
    


    



