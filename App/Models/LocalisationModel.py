from neomodel import *


class Localisation(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()
    inhabitant = RelationshipFrom('Technipedia.App.Models.UserModel.User', 'LOCATES')
    has_opps = RelationshipFrom('Technipedia.App.Models.OpportinuityModel.Opportinuity', 'HAS_LOC', cardinality=One)

    def convert(self):
        data = {}
        data['uid'] = self.uid
        data['name'] = self.name
        data['latitude'] = self.latitude
        data['longitude'] = self.longitude
        return data