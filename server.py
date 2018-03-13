# server.py
import os, random, requests
import base64, hashlib
from pybitcoin import AddressFetcher
from functools import wraps
from flask import Flask, render_template, request, abort
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

class Keys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True)

    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return '<Key %s>' % (self.id)

def addToDB(obj):
    db.session.add(obj)
    db.session.commit()

def deleteFromDB(obj):
    db.session.delete(obj)
    db.session.commit()

def get_hello():
  greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
  return random.choice(greeting_list)

def generate_hash_key():
    return base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                            random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.form['key'] and request.form['key'] == Keys.query.filter_by(id=1).first().key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

@app.route("/get/price", methods=['GET'])
def get_price():
    coin = request.args.get('coin', 'USD')
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=GRLC&tsyms=' + coin)
    return str(response.json()[coin])


@app.route("/get/bank_balance", methods=['GET'])
def get_bank_balance():
    address = 'GT7gGjmVhh1cKn1oH8HRSRFz61PNTSjfN9'
    response = requests.get('https://garli.co.in/ext/getbalance/' + address)
    return str(response.json())

@app.route("/create/address", methods=['POST'])
@require_appkey
def create_address():
    try:
        tx = request.form['tx']
        gAddress = AddressFetcher().generateGarlicAddress(True)
        wallet = Wallets(tx=tx, public=gAddress[0], private=gAddress[1])
        addToDB(wallet)
    except:
        return "Unexpected error"

    return 'Success'

@app.route("/delete/address", methods=['DELETE'])
@require_appkey
def delete_address():
    try:
        tx = request.form['tx']
        wallet = Wallets.query.filter_by(tx=tx).first()
        deleteFromDB(wallet)
    except:
        return "Unexpected error"

    return 'Success'

@app.route("/get/address/<int:tx>", methods=['GET'])
def get_address(tx):
    try:
        address = Wallets.query.filter_by(tx=tx).first()
        if not address:
            return 'Address from tx:%r not found' % (tx)
        return str(address.public)
    except:
        return 'Unexpected error'

@app.route("/create/user", methods = ['POST'])
@require_appkey
def create_user():
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