from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date
from flask_sqlalchemy import SQLAlchemy
import os

database_name = "capstone"
database_path = "postgresql://{}@{}:{}/{}".format("postgres","localhost","5432",database_name)

db = SQLAlchemy()


def setup_db(app,database_path=database_path):
    """binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    """
    drops the database tables and starts fresh
    can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(256), nullable=False)
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
    name = db.Column(String(256), nullable=False)
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
