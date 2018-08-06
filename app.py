import os
from flask import Flask, request, jsonify

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')



app = Flask(__name__)
CORS(app)

directory = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL


db = SQLAlchemy(app)
ma = Marshmallow(app)


# # DB Model
# from models import *


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    dob = db.Column(db.DateTime, unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.name

class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','age','dob','email')

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)



# Add Person API
@app.route('/person', methods=['POST'])
def add_person():

    new_person = Person(
        name = request.json['name'],\
        age = request.json['age'],\
        dob = request.json['dob'],\
        email = request.json['email'])

    db.session.add(new_person)
    db.session.commit()

    commit = db.session.query(Person).order_by("id DESC").limit(1)
    response = persons_schema.dump(commit)
    # resp = db.session.query(Person).order_by('id').first()

    resp = jsonify(response)
    print(resp)
    # resp = jsonify(request.json)
    # resp.status_code = 200

    return resp


# View All Persons API
@app.route('/person', methods=['GET'])
def get_person():
    all_persons = Person.query.all()
    result = persons_schema.dump(all_persons)
    return jsonify(result.data)




if __name__ == '__main__':
    app.run(debug=True)