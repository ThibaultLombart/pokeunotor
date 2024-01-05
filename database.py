from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, db):
    with app.app_context():
        db.init_app(app)
        db.create_all()

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    captured_pokemons = db.relationship('PokemonCaptured', backref='trainer', lazy=True)
class PokemonCaptured(db.Model):
    user_id = db.Column(db.String, db.ForeignKey('user.id'),primary_key=True)
    pokemon_id = db.Column(db.Integer, primary_key=True)

