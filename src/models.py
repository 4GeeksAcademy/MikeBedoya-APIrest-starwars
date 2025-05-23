from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref='user')
    def __repr__(self):
        return '<User %r>' % self.email
    def serialize(self):
        return {
            "id": self.id,         
            "email": self.email,
           
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref='people')
    def __repr__(self):                                                 
        return '<People %r>' % self.name
    def serialize(self):
        return {                                             
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color" : self.eye_color,
            "hair_color" : self.hair_color
        }
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref='planet')
    def __repr__(self):                                                   
        return '<Planet %r>' % self.name
    def serialize(self):
        return {                                                    
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population" : self.population,
            "terrain" : self.terrain
        }
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    people_name = db.Column(db.String(120), nullable=True)
    planet_name = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    def __repr__(self):                                                    
        return '<Favorites %r>' % self.id
    def serialize(self):
        return {                                                         
            "id": self.id,
            "people_name": self.people.name if self.people else None,
            "planet_name": self.planet.name if self.planet else None
        }
