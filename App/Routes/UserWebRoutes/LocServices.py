from flask import request, jsonify
from flask_restful import Resource


def addLocServices(app):
    app.add_resource(LocServices, '/api/web/loc', endpoint='loc.web')


class LocServices(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass