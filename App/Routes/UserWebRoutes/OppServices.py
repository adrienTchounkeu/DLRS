from flask import request, jsonify
from flask_restful import Resource

from Technipedia.App.Controlers.Opportinuity.Other import detailsOpportinuity
from Technipedia.App.Controlers.Opportinuity.Other import listTopOpportunity


def addOppServices(app):
    app.add_resource(OppServices, '/api/web/opp', endpoint='opp.web')
    app.add_resource(detailsServices, '/api/web/opp/details', endpoint='opp.web.opp.details')


class OppServices(Resource):
    def get(self):
        return listTopOpportunity()


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class detailsServices(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return detailsOpportinuity(data['id_opp'], data['id_user'])