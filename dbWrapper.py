import os

class dbWrapper:
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']