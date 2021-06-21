from flask import request, jsonify
from flask_restful import Resource


def addPrefServices(app):
    app.add_resource(PrefServices, '/api/mobile/pref', endpoint='pref.mobile')


class PrefServices(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass