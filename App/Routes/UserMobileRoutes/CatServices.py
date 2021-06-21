from flask import request, jsonify
from flask_restful import Resource


def addCatServices(app):
    app.add_resource(CatServices, '/api/mobile/cat', endpoint='cat.mobile')


class CatServices(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass