from flask import Flask, render_template

import requests

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'


class PokemonForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    codepostal = StringField('codepostal', validators=[DataRequired(), Length(max=5)])


@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
