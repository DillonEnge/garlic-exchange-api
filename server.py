# server.py
import os, random, requests

from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

def get_hello():
  greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
  return random.choice(greeting_list)

@app.route("/price/<coin>")
def price(coin):
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=GRLC&tsyms=' + coin)
    return str(response.json()[coin])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return get_hello()

if __name__ == "__main__":
    app.run()