from flask import request, jsonify
from flask_restful import Resource

from Technipedia.App.Controlers.Preference.Other import listPrefByCat


def addPrefServices(app):
    app.add_resource(PrefServices, '/api/web/pref', endpoint='pref.web')


class PrefServices(Resource):
    def get(self):
        return listPrefByCat()

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass