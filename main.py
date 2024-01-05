from flask import Flask, render_template, redirect, url_for, jsonify, request
from unidecode import unidecode
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
    data = extractData.recuperationDonnees(url)

    if not extractData.testDonnees(url):
        return redirect("/pokemon/0")
    return redirect("/pokemon/"+str(extractData.getIdPokemon(data)))

@app.route('/pokemon/<int:id>', methods=['GET'])
def pokemonNumber(id):
    url = extractData.getURLFromName(str(id))

    dico = extractData.getDict(url)

    return render_template("affichage.html", id=dico['pokedexId'], nomFR=dico['nomFR'], nomEN=dico['nomEN'],
                           types=dico['types'], sprite=dico['sprite'], stats=dico['stats'], pres = dico['pre'], nexts = dico['next'], resistances = dico['resistances'])



@app.route('/search', methods=['GET'])
def search():
    term = request.args.get('term', '')

    results = extractData.filter_and_sort_pokemon(term)

    return jsonify(results)



if __name__ == '__main__':
    app.run()
