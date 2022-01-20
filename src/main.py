"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import timedelta

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from utils import generate_sitemap
from models import db, User, Planet, PlanetDetails, PeopleDetails, People, StarshipsDetails, Starship
from admin import setup_admin

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWI_KEY')
jwt = JWTManager(app)



MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email and password:
        user = User.get_by_email(email)

        if user:
            '''check password'''
            access_token = create_access_token(identity=user.to_dict(), expires_delta=timedelta(hours=12))
            return jsonify({'token': access_token}), 200

        return jsonify({'error':'Not found'}), 200

    return jsonify({"msg": "Wrong username or password"}), 401


@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.get_all_starships()

    if starships:
        all_starships = [starship.to_dict() for starship in starships]
        return jsonify(all_starships), 200
    
    return jsonify({'error':'No starships found'}), 200


@app.route('/starship/<int:id>/starshipsdetails', methods=['GET'])
def get_starshipdetails_by_id(id):
    starshipdetails = StarshipsDetails.get_by_id_starshipdetails(id)
    
    if starshipdetails:
        return jsonify(starshipdetails.to_dict()), 200
    
    return jsonify({'error': 'Starship not found'}),


@app.route('/user/<int:id_user>/favourite-starships/<int:id_starship>', methods=['POST'])
@jwt_required()
def add_favstarship(id_user,id_starship):
    token_id = get_jwt_identity()
    print("token",token_id)

    if token_id.get("id") == id_user:
        user = User.get_user_by_id(id_user)
        starship = Starship.get_by_id_starship(id_starship)
        print("user",user)
        print("starship",starship)

        if user and starship:
            add_fav = user.add_fav_starship(starship)
            print(add_fav)
            fav_starships = [starship.to_dict() for starship in add_fav]
            return jsonify(fav_starships), 200

    return jsonify({'error': 'Starship fav not found'}), 404


@app.route('/planets', methods=['GET'])
def get_planet():

    planets= Planet.get_all()

    if planets:
        all_planets= [planet.to_dict() for planet in planets]
        return jsonify(all_planets), 200

    return jsonify({'error':'No planets found'}), 200

@app.route('/planets/<int:id>/detail', methods=['GET'])
def get_planetdetail(id):

    planetdet= PlanetDetails.getby_id(id)

    if planetdet:
    
        return jsonify(planetdet.to_dict()), 200

    return jsonify({'error':'No details found'})

@app.route('/fav/planet/<int:id_planet>', methods=['POST'])
@jwt_required()
def add_favourites(id_planet):
    user= get_jwt_identity()
    print(user)
    
    
    planet=Planet.get_byid(id_planet)

    if user and planet:
        try:
           fav= Favplanet(user_id=user.get("id"),planet_id=id_planet)
           new_fav= fav.create()
           return jsonify(new_fav.to_dict()),200
        except Exception as error:
            print(error)
            return jsonify({"error":"Intern server error"}),500


        
    
    return jsonify ({"error":"Not fav created"}),400


@app.route('/people', methods=['GET'])
def get_all_people():
    peoples = People.get_all_people()

    if peoples: 
        all_People = [people.to_dict() for people in peoples]
        return jsonify(all_People), 200

    return jsonify({'error':'People not found'}), 200


@app.route('/people/<int:id>/peopledetails', methods=['GET'])
def create_all_details():
    create_details = PeopleDetails.get_by_id(id)

    if create_details: 
        return jsonify(create_details.to_dict()), 200
    
    return jsonify({'error': 'Details not found'})

@app.route('/user/<int:id_user>/favourite-people/<int:id_people>', methods=['POST'])
@jwt_required
def add_a_favourite_character(id_user,id_people):
    token_id = get_jwt_identity()
    print ("token",token_id)

    if token_id.get("id") == id_user:
        user = User.get_user_by_id(id_user) 
        people = People.get_by_id_people(id_people)
        print("user",user)
        print ("people",people)

        if user and people: 
            add_favorite_people = user.add_fav_people(people)
            fav_people = [people.to_dict() for people in add_favorite_people]
            return jsonify(fav_people), 200

    return jsonify({"error": "Not found fav"}), 404

#this only runs if `$ python src/main.py` is executed
 #this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
