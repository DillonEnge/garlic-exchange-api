# server.py
from flask import Flask, render_template


app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

import random, requests

def get_hello():
  greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej', 'こんにちは']
  return random.choice(greeting_list)

@app.route("/price")
def price():
    response = requests.get('https://garli.co.in/ext/summary')
    return str(response.json()['data'][0]['lastUsdPrice'])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return get_hello()

if __name__ == "__main__":
    app.run()