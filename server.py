# server.py
import os, random, requests

from pybitcoin import AddressFetcher
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

class Wallets(db.Model):
    __tablename__ = "Wallets"
    id = db.Column(db.Integer, primary_key=True)
    tx = db.Column(db.Integer, unique=True)
    public = db.Column(db.String(60))
    private = db.Column(db.String(120), unique=True)

    def __init__(self, tx, public, private):
        self.tx = tx
        self.public = public
        self.private = private

    def __repr__(self):
        return '<Tx %s, Public %r>' % (self.tx, self.public)

def addToDB(obj):
    db.session.add(obj)
    db.session.commit()

def deleteFromDB(obj):
    db.session.delete(obj)
    db.session.commit()

def get_hello():
  greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
  return random.choice(greeting_list)

@app.route("/price?coin=<coin>")
def price(coin):
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=GRLC&tsyms=' + coin)
    return str(response.json()[coin])

@app.route("/transaction/<int:tx>")
def address(tx):
    try:
        gAddress = AddressFetcher.generateGarlicAddress(True)
        wallet = Wallets(tx=tx, public=gAddress[0], private=gAddress[1])
        addToDB(wallet)
    except e:
        return "Unexpected error"

    return 'Success'

@app.route("/get/transaction/<int:tx>")
def getAddress(tx):
    try:
        transaction = Wallets.query.filter_by(tx=tx).first()
        return transaction
    except:
        return 'Unexpected error'

@app.route("/create/user", methods = ['POST'])
def createUser():
    try:
        name = request.form['name']
        email = request.form['email']
        user = User(name, email)
        print(user)
        addToDB(user)
    except:
        print('An attribute was not found.')
        return 'failure'

    return 'success'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return get_hello()

if __name__ == "__main__":
    app.run(port=8080)