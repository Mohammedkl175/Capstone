from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date
from flask_sqlalchemy import SQLAlchemy
import os

#database_name = "capstone"
#database_path = "postgresql://{}@{}:{}/{}".format("postgres","localhost","5432",database_name)
database_path = "postgres://lbldiwaxwmeksl:70adfaa7a8d345213d6c0e2c41d26ecd5cecb6f41bf3be147bc198c44d225342@ec2-3-221-243-122.compute-1.amazonaws.com:5432/db01qddj6gjrak"

db = SQLAlchemy()


def setup_db(app,database_path=database_path):
    """binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    """
    drops the database tables and starts fresh
    can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()
    init_record()

def init_record():
    actor1 = Actor('Haneen Tayseer',27,'Female')
    actor1.insert()
    actor2 = Actor('Mohammed Khalil',27,'Male')
    actor2.insert()
    actor3 = Actor('Hussam Khalil',29,'Male')
    actor3.insert()
    actor4 = Actor('Ibrahim Khalil',3,'Male')
    actor4.insert()
    movie1= Movie('Wolf of Wall Street',2013)
    movie1.insert()
    movie2 = Movie('The Shawshank Redemption',1994)
    movie2.insert()

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(256), nullable=False,unique=True)
    release_year = db.Column(Integer, nullable=False)

    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_year": self.release_year
        }

    def long(self):
        return {
            "title": self.title,
            "release_year": self.release_year
        }

    def __repr__(self):
        return "<Movie {} {} {} {} />".format(self.title, self.release_year)


class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(256), nullable=False,unique=True)
    age = Column(Integer, nullable=False)
    gender = db.Column(String(256), nullable=False)

    def __init__(self, name, age,gender):
        self.name = name
        self.age = age
        self.gender=gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender":self.gender
        }

    def __repr__(self):
        return "<Movie {} {} {} />".format(self.name,self.age,self.gender)
