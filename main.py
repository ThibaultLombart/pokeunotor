from flask import Flask, render_template, redirect, url_for

import requests

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

import extractData

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'


class PokemonForm(FlaskForm):
    search = StringField('Barre de Recherche', validators=[DataRequired()])


@app.route('/')
def index():
    pokeform = PokemonForm()
    return render_template('index.html', form=pokeform)

@app.route('/pokemon', methods=['POST'])
def pokemon():
    pokeform = PokemonForm()
    url = extractData.getURLFromName(pokeform.search.data)
    nomFR = extractData.getNomFrPokemon(url)
    nomEN = extractData.getNomEnPokemon(url)
    types = extractData.getTypePokemon(url)
    sprite = extractData.getImageSpritePokemon(url)
    stats = extractData.getStatPokemon(url)
    return render_template("affichage.html", nomFR=nomFR, nomEN=nomEN, types=types, sprite=sprite, stats=stats)



if __name__ == '__main__':
    app.run()
