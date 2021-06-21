from neomodel import *
from Technipedia.App.Models.PreferenceModel import Preference

from Technipedia.App.Models.PreferenceModel import Preference


class Category(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    pref_image = StringProperty(default='')
    active = BooleanProperty(default=True)
    contents_pref = RelationshipTo(Preference, 'CONTENTS_PREF')
    contents_cat = RelationshipTo('Category', 'CONTENTS_CAT')

    def convert(self):
        data = {}
        data['uid'] = self.uid
        data['name'] = self.name
        data['pref_image'] = self.pref_image
        data['active'] = self.active
        return data