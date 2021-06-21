from Technipedia.App.Models.LocalisationModel import *


"""Create localisation and relationships"""
# Create localisation by position (latitude and longitude)
def createLocByPosition(latitude, longitude):
    loc = None
    try:
        loc = Localisation(latitude=latitude, longitude=longitude).save()
    except:
      return None
    return loc

# Create localisation by position and name
def createLocByPositionAndName(name, latitude, longitude):
    loc = None
    try:
        loc = Localisation(name=name, latitude=latitude, longitude=longitude).save()
    except:
        return None
    return loc

"""Read localisation and relationships"""
# Search localisation by uid
def searchLocById(uid):
    loc = None
    try:
        loc = Localisation.nodes.get_or_none(uid=uid)
    except:
        return None
    return loc

# Search localisation by position
def searchLocByPosition(latitude, longitude):
    loc = None
    try:
        loc = Localisation.nodes.get_or_none(latitude=latitude, longitude=longitude)
    except:
        return None
    return loc


def searchLocByPositionAndName(name, latitude, longitude):
    loc = None
    try:
        loc = Localisation.nodes.get_or_none(name=name, latitude=latitude, longitude=longitude)
    except:
        return None
    return loc

"""Update localisation and relationships"""

"""Delete localisation and relationships"""