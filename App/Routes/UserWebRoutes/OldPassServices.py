from flask import request, jsonify
from flask_restful import Resource


def addOldPassServices(app):
    app.add_resource(OldPassServices, '/api/web/oldpass', endpoint='oldpwd.web')


class OldPassServices(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass