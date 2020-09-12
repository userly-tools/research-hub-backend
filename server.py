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

if __name__ == '__main__':
    app.run(debug=True)
