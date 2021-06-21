from flask import request, jsonify
from flask_restful import Resource
from Technipedia.App.Controlers.Preference.Other import *


def addPrefServices(app):
    app.add_resource(PrefServices, '/api/admin/pref', endpoint='pref.admin')


class PrefServices(Resource):
    def get(self):
        pass

    def post(self):
        attr = request.get_json(cache=False)
        if attr is None or attr == []:
            return jsonify(datas='', status=0, errmsg='Problem of information')
        return registerPref(attr['id_cat'], attr['name'], attr['pref_image'])

    def put(self):
        pass

    def delete(self):
        pass