from flask import request, jsonify
from flask_restful import Resource
from Technipedia.App.Controlers.Category.Other import listCat, listOpportinuitiesOfCat


def addCatServices(app):
    app.add_resource(CatServices, '/api/web/cat', '/api/web/cat/<id_cat>', endpoint='catServices.web')


class CatServices(Resource):
    def get(self):
        return listCat()


    def post(self):
        data = request.get_json(cache=False)
        print(data)
        return listOpportinuitiesOfCat(data['id_cat'], data['id_user'])


    def put(self):
        pass

    def delete(self):
        pass