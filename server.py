#Reference https://rahmanfadhil.com/flask-rest-api/

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/userly.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(1024))

    researcher_uname = db.Column(db.String(16))

    components = db.Column(db.String(4096))
    responses = db.Column(db.String(4096))

    def __repr__(self):
        return '<Form %s>' % self.title

if __name__ == '__main__':
    app.run(debug=True)
