from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nazir:123456789@localhost:5432/database'

db = SQLAlchemy(app)

class Persons(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

class PeopleResource(Resource):
    def get(self):
        persons = Persons.query.all()
        result = []
        for person in persons:
            result.append({'id': person.id, 'name': person.name, 'age': person.age})
        return result

    def post(self):
        new_person = Persons(name=request.json['name'], age=request.json['age'])
        db.session.add(new_person)
        db.session.commit()
        return {'id': new_person.id, 'name': new_person.name, 'age': new_person.age}, 201

class PersonResource(Resource):
    def get(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            return {'id': person.id, 'name': person.name, 'age': person.age}
        return {"message": "person not found"}, 404

    def put(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            person.name = request.json['name']
            person.age = request.json['age']
            db.session.commit()
            return {'id': person.id, 'name': person.name, 'age': person.age}
        return {"message": "person not found"}, 404

    def delete(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
            return {"message": "Person deleted successfully"}, 200
        return {"message": "person not found"}, 404

api.add_resource(PeopleResource, '/humans')
api.add_resource(PersonResource, '/humans/<int:person_id>')

if __name__ == '__main__':
    app.run(debug=True)
