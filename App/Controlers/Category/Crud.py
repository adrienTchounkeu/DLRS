from Technipedia.App.Models.CategoryModel import *

"""Create category and relationships"""
# Create category by name and image
def createCat(name, pref_image):
    cat = None
    try:
        cat = Category(name=name, pref_image=pref_image).save()
    except:
        return None
    return cat

# Create relationship between category and preference
def createcontents_prefRelationship(startNode, endNode):
    try:
        startNode.contents_pref.connect(endNode)
    except:
        return False
    return True

# Create relationship between category and category
def createcontents_catRelationship(startNode, endNode):
    try:
        startNode.contents_cat.connect(endNode)
    except:
        return False
    return True

"""Read category and relationships"""
# Search Category by her name
def searchCatByName(name):
    cat = None
    try:
        cat = Category.nodes.get_or_none(name=name)
    except:
        return None
    return cat


# Search category by her uid
def searchCatById(uid):
    cat = None
    try:
        cat = Category.nodes.get_or_none(uid=uid)
    except:
        return None
    return cat


"""Update category and relationships"""

"""Delete category and relationships"""


