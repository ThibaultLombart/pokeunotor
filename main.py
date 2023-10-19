from flask import Flask, render_template, redirect, url_for

import requests

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

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
    return pokeform.search.data


if __name__ == '__main__':
    app.run()
