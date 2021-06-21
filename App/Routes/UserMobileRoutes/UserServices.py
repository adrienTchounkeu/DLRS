from flask import request
from flask_restful import Resource

from Technipedia.App.Controlers.Category.Other import listCatMobile, listCatPrefMobile
from Technipedia.App.Controlers.User.Other import *


def addUserServices(app):
    app.add_resource(UserServices, '/api/mobile/user', endpoint='user.mobile')
    app.add_resource(UserLogin, '/mobile/login')  # pour le login
    app.add_resource(UserSignUpFirst, '/mobile/signup/step1')
    app.add_resource(UserSignUpSecond, '/mobile/signup/step2')
    app.add_resource(UserSignUpThird, '/mobile/signup/step3')
    app.add_resource(UserSignUpFour, '/mobile/signup/step4')
    app.add_resource(listCategory, '/mobile/signup/listCategory')
    app.add_resource(listCatPref, '/mobile/signup/listCatPrefMobile')

    app.add_resource(RecommendUsers, '/api/mobile/user/recommend', endpoint='user.mobile.recommend')


class UserLogin(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return checkUserMobile(data['email'], data['password'])


class UserSignUpFirst(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return registerUserFirstStep_android(data['name'], data['username'], data['email'], data['phonenumber'],
                                             data['password'])


class UserSignUpSecond(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return registerUserSecondStepMobile(data['email'], data['code'])


class UserSignUpThird(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return registerUserThirdStepMobile(data['uid'], data['latitude'], data['longitude'], data['place'])


class UserSignUpFour(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return registerUserFourthStepMobile(data)


class listCategory(Resource):
    def get(self):
        return listCatMobile()


class listCatPref(Resource):
    def post(self):
        data = request.get_json(cache=False)
        return listCatPrefMobile(data)


class RecommendUsers(Resource):
    def post(self):
        data = request.get_json(cache=False)
        print(data)
        return recommendUser(data['uid'])
#

class UserServices(Resource):
    def get(self):
        pass

    def post(self):
        attr = request.get_json(cache=False)
        if attr.__contains__('name') and attr.__contains__('surname') and attr.__contains__(
                'email') and attr.__contains__('phoneNumber') and attr.__contains__('password'):
            return registerUserFirstStep(attr['name'], attr['surname'], attr['email'], attr['phoneNumber'],
                                         attr['password'])
        elif attr.__contains__('email') and attr.__contains__('password'):
            return checkUser(attr['email'], attr['password'])

    def put(self):
        pass

    def delete(self):
        pass
