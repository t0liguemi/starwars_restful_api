from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Character, Planet, Starship, Film,Pilot,CharFeature,PlanetFeature,StarshipFeature
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/user", methods=["POST"])
def create_user():
    user = User()
    username = request.json.get("username")
    if username is not None or username != "":
        found_user = User.query.filter_by(username=username).first() #Cuando no encuentra nada devuelve None
        if found_user is not None:
            return jsonify({
                "message": "Username exists already"
            }), 400
    user.username = username
    email = request.json.get("email")
    if email is not None or email != "":
        found_email = User.query.filter_by(email=email).first() #Cuando no encuentra nada devuelve None
        if found_email is not None:
            return jsonify({
                "message": "Email already in use"
            }), 400
    user.email = email
    password = request.json.get("password")
    if password is None or password == "":
        return jsonify({"message": "Invalid password"})
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 200

@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:

        return jsonify({"message": "No user found on that ID"}), 404
    db.session.delete(user)
    db.session.commit()

    return jsonify({"User "+str(user.username)+"deleted"}) 

@app.route("/user/get/<int:user_id>")
def get_user_by_id(user_id):
    user = User.query.get(user_id) #Cuando no consigue nada devuelve None

    if user is not None:
        return jsonify(user.to_dict()), 200

    return jsonify({"message":"User not found"}), 404

@app.route("/user")
def get_all_users():
    users = User.query.all()
    users = list(map(lambda user: user.to_dict(), users ))
    return jsonify(users), 200
    
@app.route("/character", methods=["POST"])
def create_character():
    character = Character()
    name = request.json.get("name")
    if name is not None or name != "":
        found_character = Character.query.filter_by(name=name).first() #Cuando no encuentra nada devuelve None
        if found_character is not None:
            return jsonify({
                "message": "Character exists already"
            }), 400
    character.name = name
    character.height = request.json.get("height")
    character.mass = request.json.get("mass")
    character.hair_color = request.json.get("hair_color")
    character.skin_color = request.json.get("skin_color")
    character.eye_color = request.json.get("eye_color")
    character.birth_year = request.json.get("birth_year")
    character.gender = request.json.get("gender")

    db.session.add(character)
    db.session.commit()

    return jsonify(character.to_dict()), 200

@app.route('/pilot', methods=['POST'])
def create_pilot():
    pilot=Pilot()
    pilot.starship_id=request.json.get('starship_id')
    pilot.character_id=request.json.get('character_id')
    db.session.add(pilot)
    db.session.commit()

@app.route("/character/get/<int:char_id>")
def get_character_by_id(char_id):
    character = Character.query.get(char_id) #Cuando no consigue nada devuelve None

    if character is not None:
        return jsonify(character.to_dict()), 200

    return jsonify({
                "message": "Character not found"
            }), 404

@app.route("/planet", methods=["POST"])
def create_planet():
    planet = Planet()
    name = request.json.get("name")
    if name is not None or name != "":
        found_planet = Planet.query.filter_by(name=name).first() #Cuando no encuentra nada devuelve None
        if found_planet is not None:
            return jsonify({
                "message": "Planet exists already"
            }), 400
    planet.name = name
    planet.rotation_period = request.json.get("rotation_period")
    planet.orbital_period = request.json.get("orbital_period")
    planet.diameter = request.json.get("diameter")
    planet.climate = request.json.get("climate")
    planet.gravity = request.json.get("gravity")
    planet.terrain = request.json.get("terrain")
    planet.population = request.json.get("population")


    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.to_dict()), 200

@app.route("/planet/get/<int:planet_id>")
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id) #Cuando no consigue nada devuelve None

    if planet is not None:
        return jsonify(planet.to_dict()), 200

    return jsonify({
                "message": "Planet not found"
            }), 404

@app.route("/planet")
def get_all_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.to_dict(), planets))
    return jsonify(planets), 200

@app.route("/starship", methods=["POST"])
def create_starship():
    starship = Starship()
    name = request.json.get("name")
    if name is not None or name != "":
        found_starship = Starship.query.filter_by(name=name).first() #Cuando no encuentra nada devuelve None
        if found_starship is not None:
            return jsonify({
                "message": "Starship exists already"
            }), 400
    starship.name = name
    starship.model = request.json.get("model")
    starship.manufacturer = request.json.get("manufacturer")
    starship.cost_in_credits = request.json.get("cost_in_credits")
    starship.length = request.json.get("length")
    starship.max_atm_speed = request.json.get("max_atm_speed")
    starship.crew = request.json.get("crew")
    starship.passengers = request.json.get("passengers")
    starship.cargo_capacity = request.json.get("cargo_capacity")
    starship.starship_class = request.json.get("starship_class")

    db.session.add(starship)
    db.session.commit()

    return jsonify(starship.to_dict()), 200

@app.route("/starship/get/<int:starship_id>")
def get_starship_by_id(starship_id):
    starship = Starship.query.get(starship_id) #Cuando no consigue nada devuelve None

    if starship is not None:
        return jsonify(starship.to_dict()), 200

    return jsonify({
                "message": "Starship not found"
            }), 404

@app.route("/starship")
def get_all_starships():
    starships = Starship.query.all()
    starships = list(map(lambda starship: starship.to_dict(), starships ))
    return jsonify(starships), 200

@app.route("/film", methods=["POST"])
def create_film():
    film = Film()
    title = request.json.get("title")
    if title is not None or title != "":
        found_film = Film.query.filter_by(title=title).first() #Cuando no encuentra nada devuelve None
        if found_film is not None:
            return jsonify({
                "message": "Film exists already"
            }), 400
    film.title = title
    film.director = request.json.get('director')
    film.producer = request.json.get('producer')
    film.release_date = request.json.get('release_date')

    db.session.add(film)
    db.session.commit()

    return jsonify(film.to_dict()), 200

@app.route("/film")
def get_all_films():
    films = Film.query.all()
    films = list(map(lambda film: film.to_dict(), films ))
    return jsonify(films), 200

@app.route("/film/get/<int:film_id>")
def get_film_by_id(film_id):
    film = Film.query.get(film_id) #Cuando no consigue nada devuelve None

    if film is not None:
        return jsonify(film.to_dict()), 200

    return jsonify({
                "message": "Film not found"
            }), 404

@app.route('/character_feature', methods=['POST'])
def feature_character():
    feature=CharFeature()
    feature.film_id=request.json.get('film_id')
    feature.character_id=request.json.get('character_id')
    db.session.add(feature)
    db.session.commit()

@app.route('/planet_feature', methods=['POST'])
def feature_planet():
    feature=PlanetFeature()
    feature.film_id=request.json.get('film_id')
    feature.planet_id=request.json.get('planet_id')
    db.session.add(feature)
    db.session.commit()

@app.route('/starship_feature', methods=['POST'])
def feature_starship():
    feature=StarshipFeature()
    feature.film_id=request.json.get('film_id')
    feature.starship_id=request.json.get('starship_id')
    db.session.add(feature)
    db.session.commit()

if __name__ == '__main__':
    app.run(host="localhost", port=5000)