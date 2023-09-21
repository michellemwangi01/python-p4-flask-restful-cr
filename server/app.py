#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to the Newsletter RESTFul API",
        }
        response = make_response(response_dict, 200)
        return response


api.add_resource(Home, '/')


class Newsletters(Resource):
    def get(self):
        newsletter_dicts = [newsletter.to_dict() for newsletter in Newsletter.query.all()]
        return make_response(newsletter_dicts, 200)

    def post(self):
        new_newsletter = Newsletter(
            title=request.form['title'],
            body=request.form['body']
        )
        db.session.add(new_newsletter)
        db.session.commit()
        return make_response(new_newsletter.to_dict(), 201)


api.add_resource(Newsletters, '/newsletters')


class NewsLetterByID(Resource):
    def get(self, id):
       return make_response(Newsletter.query.filter_by(id=id).first().to_dict(),200)


api.add_resource(NewsLetterByID, '/newsletterbyid/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
