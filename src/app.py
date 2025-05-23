"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# @app.route('/user', methods=['GET'])
# def handle_hello():
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }
#     return jsonify(response_body), 200
@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    print(all_people)
    results = list(map(lambda people: people.serialize(), all_people))
    print(results)
    # response_body = {
    #     "msg": "Hello, this is your GET /people response ",
    #     "results": results
    # }
    return jsonify(results), 200             
@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    single_people = People.query.get(people_id)
    print(single_people.serialize())
    return jsonify(single_people.serialize()), 200
@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    print(all_planets)
    results2 = list(map(lambda planet: planet.serialize(), all_planets))
    print(results2)
    # response_body = {
    #     "msg": "Hello, this is your GET /people response ",
    #     "results": results
    # }
    return jsonify(results2), 200
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    single_planet = Planet.query.get(planet_id)
    print(single_planet.serialize())
    return jsonify(single_planet.serialize()), 200
@app.route('/users', methods=['GET'])
def get_all_users():
    all_planets = User.query.all()
    print(all_planets)
    results_planets = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(results_planets), 200
@app.route('/users/favorites', methods=['GET'])
def get_all_favorites():
    all_favorites = Favorites.query.all()
    print(all_favorites)
    results_favorites = list(map(lambda fav: fav.serialize(), all_favorites))
    return jsonify(results_favorites), 200
@app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorites( planet_id):
    print(request)                     
    print(request.json)
    user = User.query.first()   
    planet = Planet.query.get(planet_id)   
    if not planet :
        return jsonify({"error" : "Planet not found"}), 404
    new_fav = Favorites(user_id= user.id, planet_id = planet.id, planet_name = planet.name)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "planet successfully added"}), 200
@app.route('/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_to_favorites(planet_id):
    print(request)                      
    print(request.json)
    user = User.query.first()
    planet = Planet.query.get(planet_id)
    if not planet :
        return jsonify({"error" : "Planet not found"}), 404
    fav_to_delete = Favorites.query.filter_by(user_id= user.id, planet_id = planet.id).first()    # Trova il record di favorite da eliminare
    print("Planet ID:", planet.id)
    if not fav_to_delete :
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav_to_delete)
    db.session.commit()
    return jsonify({"message" : "favorite planet successfully deleted"}), 200
@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def add_people_to_favorites(people_id):
    print(request)                      
    print(request.json)
    user = User.query.first()    
    people = People.query.get(people_id)   
    if not people :
        return jsonify({"error" : "Character not found"}), 404
    new_fav = Favorites(user_id= user.id, people_id = people.id, people_name = people.name)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "character successfully added"}), 200
@app.route('/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_people_to_favorites(people_id):
    print(request)                     
    print(request.json)
    user = User.query.first()
    people = People.query.get(people_id)
    if not people :
        return jsonify({"error" : "people not found"}), 404
    fav_to_delete = Favorites.query.filter_by(user_id= user.id, people_id = people.id).first()    
    print("People ID:", people.id)
    if not fav_to_delete :
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav_to_delete)
    db.session.commit()
    return jsonify({"message" : "favorite people successfully deleted"})
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)