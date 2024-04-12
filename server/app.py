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
        resp_dict = {
            'message':'Welcome to Newsletter RESTful API'
        }
        resp = make_response(resp_dict, 200)
        return resp
    
class Newsletters(Resource):

    def get(self):
        resp_dict = [news.to_dict() for news in Newsletter.query.all()]

        resp = make_response(resp_dict, 200)
        return resp
    
    def post(self):
        new_newsletter = Newsletter(title=request.args.get('title'), body=request.args['body'])
        print(new_newsletter)
        db.session.add(new_newsletter)
        db.session.commit()

        resp_dict = new_newsletter.to_dict()
        print(resp_dict)
        resp = make_response(resp_dict, 201)
        return resp
    
class NewsletterById(Resource):

    def get(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id == id).first()
        if not newsletter:
            resp_dict = {'error': 'Newsletter Not Found!!'}
            return make_response(resp_dict, 400)
        else:
            resp_dict = newsletter.to_dict()
            return make_response(resp_dict, 200)
    
api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
