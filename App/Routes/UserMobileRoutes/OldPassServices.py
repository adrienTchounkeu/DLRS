from flask import request, jsonify
from flask_restful import Resource


def addOldPassServices(app):
    app.add_resource(OldPassServices, '/api/mobile/oldpass', endpoint='oldpwd.mobile')


class OldPassServices(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass