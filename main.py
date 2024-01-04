from flask import Flask, render_template, redirect, url_for

import requests

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

import extractData

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'
app.static_folder = 'static'

class PokemonForm(FlaskForm):
    search = StringField('Barre de Recherche', validators=[DataRequired()])


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

    if not extractData.testDonnees(url):
        url = extractData.getURLFromName("missingno")

    dico = extractData.getDict(url)

    return render_template("affichage.html", id=extractData.getIdPokemon(url), nomFR=dico['nomFR'], nomEN=dico['nomEN'], types=dico['types'], sprite=dico['sprite'], stats=dico['stats'])



if __name__ == '__main__':
    app.run()
