#models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email":self.email,
            "username": self.username
        }


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    fav_character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    fav_planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    fav_starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"))
    fav_film_id = db.Column(db.Integer, db.ForeignKey("film.id"))
    def to_dict(self):
        return {
            'fav_character_id':self.fav_character_id,
            'fav_planet_id':self.fav_planet_id,
            'fav_starship_id':self.fav_starship_id,
            'fav_film_id':self.fav_film_id
        }

class CharFeature(db.Model):
    __tablename__='char_feature'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.ForeignKey('character.id'))
    film_id = db.Column(db.ForeignKey('film.id'))

    def to_dict(self):
        return {
            'character_id':self.character_id,
            'film_id':self.film_id
        }

class PlanetFeature(db.Model):
    __tablename__='planet_feature'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.ForeignKey('planet.id'))
    film_id = db.Column(db.ForeignKey('film.id'))
    def to_dict(self):
        return {
            'planet_id':self.planet_id,
            'film_id':self.film_id
        }

class StarshipFeature(db.Model):
    __tablename__='starship_feature'
    id = db.Column(db.Integer, primary_key=True)
    starship_id = db.Column(db.ForeignKey('starship.id'))
    film_id = db.Column(db.ForeignKey('film.id'))

    def to_dict(self):
        return {
            'starship_id':self.starship_id,
            'film_id':self.film_id
        }

class Pilot(db.Model):
    __tablename__='pilot'
    id = db.Column(db.Integer, primary_key=True)
    starship_id = db.Column(db.ForeignKey('starship.id'))
    character_id = db.Column(db.ForeignKey('character.id'))
    def to_dict(self):
        return {
            'character_id':self.character_id,
            'starship_id':self.starship_id
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(250))
    filmFeature = db.relationship("CharFeature", backref="film")
    piloted = db.relationship('Pilot', backref="character")
    homeworld_id= db.Column(db.ForeignKey("planet.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color":self.hair_color,
            'skin_color':self.skin_color,
            'eye_color':self.eye_color,
            'birth_year':self.birth_year,
            'gender':self.gender,
            'piloted':self.piloted,
            'homeworld':self.homeworld_id,
            'films': [feature.film_id for feature in self.filmFeature]

        }  


class Planet(db.Model):
    __tablename__='planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    gravity = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    population = db.Column(db.Integer)
    residents = db.relationship('Character', backref='homeworld')
    filmFeature = db.relationship("PlanetFeature", backref="film")

    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            'rotation_period':self.rotation_period,
            'orbital_period':self.orbital_period,
            'diameter':self.diameter,
            'climate':self.climate,
            'gravity':self.gravity,
            'terrain':self.terrain,
            'population':self.population,
            'films': [feature.film_id for feature in self.filmFeature]
        }  

class Starship(db.Model):
    __tablename__='starship'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)   
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    cost_in_credits = db.Column(db.Integer)
    length = db.Column(db.Integer)
    max_atm_speed = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)
    starship_class = db.Column(db.String(250))
    pilots = db.relationship('Pilot',backref='starship')
    filmFeature = db.relationship("StarshipFeature", backref="film")


    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            'model':self.model,
            'manufacturer':self.manufacturer,
            'cost_in_credits':self.cost_in_credits,
            'length':self.length,
            'max_atm_speed':self.max_atm_speed,
            'crew':self.crew,
            'passengers':self.passengers,
            'cargo_capacity':self.cargo_capacity,
            'starship_class':self.starship_class,
            'films': [feature.film_id for feature in self.filmFeature]
        }  

class Film(db.Model):
    __tablename__='film'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    director = db.Column(db.String(250))
    producer = db.Column(db.String(250))
    release_date = db.Column(db.Integer)
    characters = db.relationship('CharFeature',backref='film')
    planets = db.relationship('PlanetFeature',backref='film')
    starships = db.relationship('StarshipFeature',backref='film')

    def to_dict(self):
        return {
            "id": self.id,
            'title' : self.title,
            'director':self.director,
            'producer':self.producer,
            'release_date':self.release_date,
            'characters': [character.character_id for character in self.characters],
            'planets': [planet.planet_id for planet in self.planets],
            'starships': [starship.starship_id for starship in self.starships]
        }  