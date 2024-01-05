from flask import Flask, render_template, redirect, url_for, jsonify, request

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import requests

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


import extractData

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokeunotor.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from forms import LoginForm, PokemonForm, RegisterForm
# ------------------------------------------------------- BD ------------------------------------------------ #
from database import User, PokemonCaptured, init_db, db


init_db(app, db)
# ------------------------------------------------------- FIN BD ------------------------------------------------ #
# ------------------------------------------------------- USERS ------------------------------------------------- #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        error = 'Email ou mot de passe incorrecte.'
        return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            error = 'Email déjà pris'
            return render_template('register.html', form=form, error=error)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(id=str(len(User.query.all()) + 1), username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    captured_pokemons = PokemonCaptured.query.filter_by(user_id=current_user.id).all()
    captured_pokemons_ids = [pokemon_captured.pokemon_id for pokemon_captured in captured_pokemons]


    result_pokemons = extractData.listeId(captured_pokemons_ids)
    return render_template('dashboard.html', captured_pokemons=result_pokemons)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
# ------------------------------------------------------- FIN USERS ------------------------------------------------- #


@app.route('/')
def index():
    pokeform = PokemonForm()
    return render_template('index.html', form=pokeform)

@app.route('/pokemon', methods=['GET'])
def pokemonRedirect():
    return redirect("/")

@app.route('/pokemon', methods=['POST'])
def pokemon():
    pokeform = PokemonForm()
    url = extractData.getURLFromName(pokeform.search.data)
    data = extractData.recuperationDonnees(url)

    if not extractData.testDonnees(url):
        return redirect("/pokemon/0")
    return redirect("/pokemon/"+str(extractData.getIdPokemon(data)))

@app.route('/pokemon/<int:id>', methods=['GET'])
def pokemonNumber(id):
    url = extractData.getURLFromName(str(id))

    dico = extractData.getDict(url)

    collection = False
    if current_user.is_authenticated:
        collection = PokemonCaptured.query.filter_by(user_id=current_user.id, pokemon_id=id).first() is not None

    return render_template("affichage.html", id=dico['pokedexId'], nomFR=dico['nomFR'], nomEN=dico['nomEN'],
                           types=dico['types'], sprite=dico['sprite'], stats=dico['stats'], pres = dico['pre'], nexts = dico['next'], resistances = dico['resistances'], collection=collection)



@app.route('/search', methods=['GET'])
def search():
    term = request.args.get('term', '')

    results = extractData.filter_and_sort_pokemon(term)

    return jsonify(results)


@app.route('/add_to_favorites/<int:pokemon_id>', methods=['POST'])
@login_required
def add_to_favorites(pokemon_id):
    if not PokemonCaptured.query.filter_by(user_id=current_user.id, pokemon_id=pokemon_id).first():
        new_favorite = PokemonCaptured(user_id=current_user.id, pokemon_id=pokemon_id)
        db.session.add(new_favorite)
        db.session.commit()
    else:
        db.session.delete(PokemonCaptured.query.filter_by(user_id=current_user.id, pokemon_id=pokemon_id).first())
        db.session.commit()
    return redirect(url_for('pokemonNumber', id=pokemon_id))


if __name__ == '__main__':
    app.run()
