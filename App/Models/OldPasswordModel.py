import datetime

from neomodel import *


class OldPassword(StructuredNode):
    uid = UniqueIdProperty()
    password = StringProperty()
    date_edition = DateTimeProperty(default=datetime.datetime.now())
    users_passwords = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_OLD_PASSWORDS')

    def convert(self):
        data = {}
        data['uid'] = self.uid
        data['password'] = self.password
        data['date_edition'] = self.date_edition
        return data