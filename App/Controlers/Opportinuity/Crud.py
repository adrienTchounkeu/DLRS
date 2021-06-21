from Technipedia.App.Models.OpportinuityModel import *

"""Create opportinuity and relationships"""
# Create opportinuity by name and description
def createOpp(name, description):
    opp = None
    try:
        opp = Opportinuity(name=name, description=description).save()
    except:
        return None
    return opp

# create relationship between opportinuity and localisation
def createis_locatedRelationship(startNode, endNode):
    try:
        startNode.is_located.connect(endNode)
    except:
        return False
    return True

"""Read opportinuity and relationships"""
# Search opportinuity by id
def searchOppById(uid):
    opp = None
    try:
        opp = Opportinuity.nodes.get_or_none(uid=uid)
    except:
        return None
    return opp

# Search opportinuity by name
def searchOppByName(name):
    opp = None
    try:
        opp = Opportinuity.nodes.get_or_none(name=name)
    except:
        return None
    return opp

# Search opportinuity by her id_opp_for_pred
def searchOppById_Opp_For_Pred(id_opp_for_pred):
    opp = None
    try:
        opp = Opportinuity.nodes.get_or_none(id_opp_for_pred=id_opp_for_pred)
    except:
        return None
    return opp

# Search id pref of opportinuity
def searchIdPrefOfOpp(id_opp):
    id_pref = None
    try:
        id_pref = Opportinuity.nodes.get(uid=id_opp).concerns.all()[0].uid
    except:
        return None
    return id_pref

"""Update opportinuity and relationships"""

"""Delete opportinuity and relationships"""