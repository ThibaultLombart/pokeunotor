from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
