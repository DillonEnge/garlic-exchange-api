# server.py
import os, random, requests

from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(80), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

def get_hello():
  greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
  return random.choice(greeting_list)

@app.route("/price/<coin>")
def price(coin):
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=GRLC&tsyms=' + coin)
    return str(response.json()[coin])

@app.route("/create/user", methods = ['POST'])
def createUser():
    if 'name' in request.form.values()
    print(request.form.values['name'])
    return 'success'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return get_hello()

if __name__ == "__main__":
    app.run()