#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers_dict = [campers.to_dict(only = ("id", "name", "age")) for campers in Camper.query.all()]

        response = make_response(
            campers_dict, 
            200
        )
        
        return response 
    
    def post(self):

        try:
            new_camper = Camper(
                name=request.json['name'],
                age=request.json['age']
            )

            db.session.add(new_camper)
            db.session.commit()

            new_camper_dict = new_camper.to_dict(only = ("name", "age", "id"))

            response = make_response(
                new_camper_dict,
                201
            )

            return response
        
        except:
            return {"error": "400: Validation error"}, 400
    
api.add_resource(Campers, '/campers')

class CampersById(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id = id).first()

        if camper: 
            camper_dict = camper.to_dict()

            response = make_response(
                camper_dict,
                200
            )

            return response
        
        return {"error": "404: Camper not found"}, 404
    
api.add_resource(CampersById, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        activities_dict = [activities.to_dict(only = ("id", "name", "difficulty")) for activities in Activity.query.all()]

        response = make_response(
            activities_dict, 
            200
        )
        
        return response 
    
api.add_resource(Activities, '/activities')

class AcitivitiesById(Resource):
    def get(self, id):
        activity = Activity.query.filter_by(id = id).first()
        
        activity_dict = activity.to_dict(only = ("id", "name", "difficulty"))

        response = make_response(
            activity_dict,
            200
        )

        return response
    
    def delete(self, id):
        activity = Activity.query.filter_by(id = id).first()
        if activity:

            db.session.delete(activity)
            db.session.commit()

            response = make_response(
                "",
                204
            )

            return response
        
        return {"error": "404: Activity not found"}, 404

    
api.add_resource(AcitivitiesById, '/activities/<int:id>')

class Signups(Resource):
    def get(self):
        signups_dict = [signups.to_dict() for signups in Signup.query.all()]

        response = make_response(
            signups_dict, 
            200
        )
        
        return response 
    
    def post(self):
        try:
            new_signup = Signup(
                time=request.json['time'],
                camper_id=request.json['camper_id'],
                activity_id=request.json['activity_id']
            )

            db.session.add(new_signup)
            db.session.commit()

            new_signup_dict = new_signup.to_dict()

            response = make_response(
                new_signup_dict,
                201
            )

            return response
        except:
            return {"error": "400: Validation error"}, 400

api.add_resource(Signups, '/signups')

    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
