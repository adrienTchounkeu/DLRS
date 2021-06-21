from flask import request, jsonify
from flask_restful import Resource
from Technipedia.App.Controlers.Category.Other import *


def addCatServices(app):
    app.add_resource(CatServices, '/api/admin/cat', endpoint='cat.admin')


class CatServices(Resource):
    def get(self):
        pass

    def post(self):
        attr = request.get_json(cache=False)
        if attr is None or attr == []:
            return jsonify(datas='', status=0, errormsg='Problem of information')
        return registerCat(attr['name'], attr['pref_image'])

    def put(self):
        pass

    def delete(self):
        pass