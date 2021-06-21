from flask import request, jsonify
from flask_restful import Resource
from Technipedia.App.Controlers.User.Other import *
from Technipedia.App.Controlers.Category.Crud import *


def addUserServices(app):
    app.add_resource(AdminServices, '/api/admin', endpoint='admin.admin')


class AdminServices(Resource):
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass