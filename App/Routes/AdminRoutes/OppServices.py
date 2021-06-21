from flask import request, jsonify
from flask_restful import Resource
from Technipedia.App.Controlers.Opportinuity.Other import *


def addOppServices(app):
    app.add_resource(OppServices, '/api/admin/opp', endpoint='opp.admin')


class OppServices(Resource):
    def get(self):
        pass

    def post(self):
        """jsonData = request.get_json(cache=False)
        attr = {}
        if jsonData is None or jsonData == []:
            return jsonify(result='', status=0, errmsg='Problem of information')
        for key in jsonData:
            attr[key] = jsonData[key]
        if attr.__contains__('id_pref') and attr.__contains__('name') and attr.__contains__('description') and attr.__contains__('name_loc') and attr.__contains__('latitude') and attr.__contains__('longitude'):
            return registerOpp(attr['id_pref'], attr['name'], attr['description'], attr['name_loc'], attr['latitude'], attr['longitude'])
        """
        print(request.form['name'])
        # checking if the file is present or not.
        if 'file' not in request.files:
            return "No file found"

        file = request.files['file']
        print(file.filename)
        file.save("Images/Opportinuities/test.jpg")
        return "file successfully saved"

    def put(self):
        pass

    def delete(self):
        pass


