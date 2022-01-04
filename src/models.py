from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
import sys

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    have_favourites = relationship("Favourites")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            # do not serialize the password, its a security breach
        }

    @classmethod
    def get_by_email(cls, email):
        name = cls.query.filter_by(email= email).first()
        return name if name else "User not found :_("

    @classmethod
    def get_all(cls):
        user = cls.query.all()
        return user
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.serialize()

    @classmethod
    def delete_user(cls, email):
        target = cls.query.filter_by(email = email).first()
        db.session.delete(target)
        db.session.commit()


class Favourites(db.Model):
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    have_user = relationship("User")
    have_people = relationship("People")
    have_vehicles = relationship("Vehicles")
    have_planets = relationship("Planets")

    @classmethod
    def get_all(cls):
        favourites=cls.query.all()
        return favourites 

    def create(self):
        db.session.add(self)
        db.session.commit()


class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key = True)
    favourites_id = db.Column(db.Integer, db.ForeignKey("favourites.id"))

    name = db.Column(db.String(20), unique=False, nullable=False)
    height = db.Column(db.String(20), unique=False, nullable=False)
    mass = db.Column(db.String(20), unique=False, nullable=False)
    hair_color = db.Column(db.String(20), unique=False, nullable=False)
    skin_color = db.Column(db.String(20), unique=False, nullable=False)
    eye_color = db.Column(db.String(20), unique=False, nullable=False)
    birth_year = db.Column(db.String(20), unique=False, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    #homeworld = db.Column(db.String(20), unique=False, nullable=False)
    #species = db.Column(db.String(20), unique=False, nullable=False)
    #vehicles = db.Column(db.String(20), unique=False, nullable=False)
    #starships = db.Column(db.String(20), unique=False, nullable=False)
    created = db.Column(db.String(20), unique=False, nullable=False)
    edited = db.Column(db.String(20), unique=False, nullable=False)
    #url = db.Column(db.String(20), unique=False, nullable=False)

#for /people/id

    def to_dict(self):
        return {
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
        }


    @classmethod
    def get_by_id(cls, id):
        people = cls.query.get(id)
        return people
    
    @classmethod
    def get_all(cls):
        people = cls.query.all()
        return people

    def create(self):
        db.session.add(self)
        db.session.commit()


class Vehicles(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key = True)
    favourites_id = db.Column(db.Integer, db.ForeignKey("favourites.id"))

    name = db.Column(db.String, unique=False, nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    manufacturer = db.Column(db.String, unique=False, nullable=False)
    cost_in_credits = db.Column(db.String, unique=False, nullable=False)
    length = db.Column(db.String, unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.String, unique=False, nullable=False)
    crew = db.Column(db.String, unique=False, nullable=False)
    passengers = db.Column(db.String, unique=False, nullable=False)
    cargo_capacity = db.Column(db.String, unique=False, nullable=False)
    consumables = db.Column(db.String, unique=False, nullable=False)
    vehicle_class = db.Column(db.String, unique=False, nullable=False)
    pilots = db.Column(db.String, unique=False, nullable=False)
    created = db.Column(db.String, unique=False, nullable=False)
    edited = db.Column(db.String, unique=False, nullable=False)
    url = db.Column(db.String, unique=False, nullable=False)

class Planets(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key = True)
    favourites_id = db.Column(db.Integer, db.ForeignKey("favourites.id"))

    name = db.Column(db.String, unique=False, nullable=False)
    height = db.Column(db.String, unique=False, nullable=False)
    mass = db.Column(db.String, unique=False, nullable=False)
    hair_color = db.Column(db.String, unique=False, nullable=False)
    skin_color = db.Column(db.String, unique=False, nullable=False)
    eye_color = db.Column(db.String, unique=False, nullable=False)
    birth_year = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)
    homeworld = db.Column(db.String, unique=False, nullable=False)
    species = db.Column(db.String, unique=False, nullable=False)
    vehicles = db.Column(db.String, unique=False, nullable=False)
    starships = db.Column(db.String, unique=False, nullable=False)
    created = db.Column(db.String, unique=False, nullable=False)
    edited = db.Column(db.String, unique=False, nullable=False)
    url = db.Column(db.String, unique=False, nullable=False)