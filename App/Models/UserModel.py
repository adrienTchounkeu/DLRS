from datetime import date, datetime
from neomodel import *
from passlib.apps import custom_app_context as pwd_context

from Technipedia.App.Models.LocalisationModel import Localisation
from Technipedia.App.Models.OldPasswordModel import OldPassword
from Technipedia.App.Models.OldPasswordModel import OldPassword
from Technipedia.App.Models.OpportinuityModel import Opportinuity
from Technipedia.App.Models.PreferenceModel import Preference


class similarity(StructuredRel):
    distance = FloatProperty()


class UserNoteRel(StructuredRel):
    ratings = FloatProperty(default=0)

    def convert(self):
        data = {}
        data['id'] = self.id
        data['ratings'] = self.ratings
        return data


class UserLaterRel(StructuredRel):
    date = DateProperty(default=date.today())

    def convert(self):
        data = {}
        data['id'] = self.id
        data['date'] = self.date
        return data


class UserPredRel(StructuredRel):
    pred = FloatProperty(default=0)

    def convert(self):
        data = {}
        data['id'] = self.id
        data['pred'] = self.pred
        return data


class UserHistoryRel(StructuredRel):
    date = DateTimeProperty(default=datetime.now())
    ratings_implicite = FloatProperty(default=0)

    def convert(self):
        data = {}
        data['id'] = self.id
        data['date'] = self.date
        data['ratings_implicite'] = self.ratings_implicite
        return data


class DiscussionRel(StructuredRel):
    date = DateTimeProperty()

    def convert(self):
        data = {}
        data['id'] = self.id
        data['date'] = self.date
        return data


class User(StructuredNode):
    uid = UniqueIdProperty()
    bool_auth = BooleanProperty(default=False)
    code_auth = StringProperty()
    email = StringProperty()
    name = StringProperty()
    username = StringProperty()
    password = StringProperty()
    phoneNumber = StringProperty()
    economicstatus = StringProperty()
    profil_search = ArrayProperty(StringProperty())
    user_image = StringProperty()
    id_user_for_pred = IntegerProperty()
    locates = RelationshipTo(Localisation, 'LOCATES')
    has_rated = RelationshipTo(Opportinuity, 'HAS_RATED', model=UserNoteRel)
    has_pred = RelationshipTo(Opportinuity, 'HAS_PRED', model=UserPredRel)
    has_see_later = RelationshipTo(Opportinuity, 'HAS_SEE_LATER', model=UserLaterRel)
    has_hist = RelationshipTo(Opportinuity, 'HAS_HIST', model=UserHistoryRel)
    has_pref = RelationshipTo(Preference, 'HAS_PREF')
    discutes = RelationshipTo('User', 'DISCUTED', model=DiscussionRel)
    has_old_passwords = RelationshipTo(OldPassword, 'HAS_OLD_PASSWORDS')

    discutes = RelationshipTo('User', 'DISCUTED', model=DiscussionRel)
    has_old_passwords = RelationshipTo(OldPassword, 'HAS_OLD_PASSWORDS')
    has_sim = RelationshipTo('User', 'HAS_SIM_USER', model=similarity)

    discutes = RelationshipTo('User', 'DISCUTED', model=DiscussionRel)
    has_old_passwords = RelationshipTo(OldPassword, 'HAS_OLD_PASSWORDS')


    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password, passwordHash):
        return pwd_context.verify(password, passwordHash)

    def convert(self):
        data = {}
        data['uid'] = self.uid
        data['bool_auth'] = self.bool_auth
        data['code_auth'] = self.code_auth
        data['email'] = self.email
        data['name'] = self.name
        data['username'] = self.username
        data['password'] = self.password
        data['phoneNumber'] = self.phoneNumber
        data['economicstatus'] = self.economicstatus
        data['user_image'] = self.user_image
        return data

    def user_information_first_step(self):
        data = {}
        data['uid'] = self.uid
        data['email'] = self.email
        data['name'] = self.name
        data['username'] = self.username
        data['phoneNumber'] = self.phoneNumber
        data['economicstatus'] = self.economicstatus
        data['user_image'] = self.user_image
        return data
