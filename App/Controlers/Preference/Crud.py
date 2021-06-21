from Technipedia.App.Controlers.Category.Crud import *
from Technipedia.App.Models.PreferenceModel import Preference


"""Create preference and relationships"""
# Create preference by name and image
def createPref(name, pref_image):
    pref = None
    try:
        pref = Preference(name=name, pref_image=pref_image).save()
    except:
        return None
    return pref

# Create relationship between preference and opportinuity
def createLocatedRelationship(startNode, endNode):
    try:
        startNode.located.connect(endNode)
    except:
        return False
    return True

"""Read preference and relationships"""
# Search Category by her name
def searchPrefByName(name):
    pref = None
    try:
        pref = Preference.nodes.get_or_none(name=name)
    except:
        return None
    return pref


# Search category by her uid
def searchPrefById(uid):
    pref = None
    try:
        pref = Preference.nodes.get_or_none(uid=uid)
    except:
        return None
    return pref

# search preference in category
def searchPrefByIdCatUsingName(uid_cat, name):
    cat = searchCatById(uid_cat)
    prefs = [pref for pref in cat.contents_pref.all() if pref.name==name]
    if prefs == [] or prefs is None:
        return None, False
    else:
        return prefs, True


"""Update preference and relationships"""

"""Delete preference and relationships"""