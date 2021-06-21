from flask import request, jsonify
from flask_restful import Resource


def addOppServices(app):
    app.add_resource(OppServices, '/api/mobile/opp', endpoint='opp.mobile')


class OppServices(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
