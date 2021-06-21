from neomodel import *

from Technipedia.App.Models.OpportinuityModel import Opportinuity


class Preference(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    pref_image = StringProperty(default='')
    active = BooleanProperty(default=True)
    interests = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_PRED')
    users_pref = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_PREF')
    located = RelationshipTo(Opportinuity, 'LOCATED')
    belongs_cat = RelationshipFrom('Technipedia.App.Models.CategoryModel.Category', 'CONTENTS_PREF')

    def convert(self):
        data = {}
        data['uid'] = self.uid
        data['name'] = self.name
        data['pref_image'] = self.pref_image
        data['active'] = self.active
        return data