# server.py
from flask import Flask, render_template


app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

import random, requests

def get_hello():
  greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
  return random.choice(greeting_list)

@app.route("/price/<coin>")
@cross_origin()
def price(coin):
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=GRLC&tsyms=' + coin)
    return str(response.json()[coin])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
@cross_origin()
def hello():
    return get_hello()

if __name__ == "__main__":
    app.run()