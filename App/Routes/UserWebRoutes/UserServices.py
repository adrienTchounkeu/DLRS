from flask import request
from flask_restful import Resource

from Technipedia.App.Controlers.User.Other import *


def addUserServices(app):
    app.add_resource(SeeLater, '/api/web/user/seeLater')
    app.add_resource(RegisterFirstStepWeb, '/api/web/user/register_first_step')
    app.add_resource(RegisterFinalStepWeb, '/api/web/user/register_final_step')
    app.add_resource(Recommandations, '/api/web/user/recommend')
    app.add_resource(Connexion, '/api/web/user/connexion')
    app.add_resource(ColdStart, '/api/web/user/cold_start')


class SeeLater(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return listSeeLater(data['id_user'])

    def delete(self):
        data = request.get_json(cache=False)
        return removeSeeLater(data['id_user'], data['id_opp'])

    def put(self):
        data = request.get_json(cache=False)
        return addSeeLater(data['id_user'], data['id_opp'])


class RegisterFirstStepWeb(Resource):
    def post(self):
        attr = request.get_json(cache=False)
        return registerUserFirstStep(attr['firstname'], attr['lastname'], attr['email'], attr['phonenumber'], attr['economicstatus'], attr['password'])


class RegisterFinalStepWeb(Resource):
    def post(self):
        attr = request.get_json(cache=False)
        return registerUserFinalStep(attr['locations'], attr['preferences'], attr['id_user'])


class Recommandations(Resource):
    def post(self):
        attr = request.get_json(cache=False)
        return listRecommandations(attr['id_user'])


class Connexion(Resource):
    def post(self):
        attr = request.get_json(cache=False)
        return checkUser(attr['email'], attr['password'])


class ColdStart(Resource):
    def post(self):
        attr = request.get_json(cache=False)
        return cold_start(attr['id_user'])
