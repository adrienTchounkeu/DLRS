from neomodel import *
from Technipedia.App.Models.LocalisationModel import Localisation
import datetime

class similarity(StructuredRel):
    distance = FloatProperty()


class Opportinuity(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    description = StringProperty()
    opp_image = StringProperty(default='')
    date_edition = DateTimeProperty(default=datetime.datetime.now())
    moyenne = FloatProperty(default=0)
    active = BooleanProperty(default=True)
    id_opp_for_pred = IntegerProperty()
    economicstatus = StringProperty()
    interests = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_RATED')
    users_rated = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_PRED')
    users_see_later = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_SEE_LATER')
    users_hist = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'HAS_HIST')
    concerns = RelationshipFrom('Technipedia.App.Models.PreferenceModel.Preference', 'LOCATED')
    is_located = RelationshipTo(Localisation, 'HAS_LOC')
    has_sim = RelationshipTo('Opportinuity', 'HAS_SIM_OPP', model=similarity)

    def convert(self):
        data={}
        data['uid'] = self.uid
        data['name'] = self.name
        data['description'] = self.description
        data['opp_image'] = self.opp_image
        data['date_edition'] = self.date_edition
        data['moyenne'] = self.moyenne
        data['active'] = self.active
        return data