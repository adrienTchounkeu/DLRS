from Technipedia.App.Models.UserModel import *


"""Create user and relationships"""
# Create user with name, username, email, phoneNumber, economicstatus, password
def createUser(name, username, email, phoneNumber, economicstatus, password):
    try:
        user = User(name=name, username=username, email=email, phoneNumber=phoneNumber, economicstatus=economicstatus, password=str(User().hash_password(password))).save()
    except:
        return None
    return user

# Create user with name, username, email, phoneNumber, economicstatus, password
def createUser_android(name, username, email, phoneNumber, password):
    try:
        user = User(name=name, username=username, email=email, phoneNumber=phoneNumber, password=str(User().hash_password(password))).save()
    except:
        return None
    return user

# Create relationship between user and opportinuity. User rates and opportinuity
def createhas_ratedRelationship(startNode, endNode, ratings):
    try:
        startNode.has_rated.connect(endNode, {'ratings':ratings})
    except:
        return False
    return True

#create relationship between user and preferences
def createhas_prefRelationship(startNode, endNode):
    try:
        startNode.has_pref.connect(endNode)
    except:
        return False
    return True

# create relationship between user and opportinuity: prediction
def createhas_predRelationship(startNode, endNode, pred):
    try:
        startNode.has_pred.connect(endNode, {'pred':pred})
    except:
        return False
    return True

# create relationship between user and location
def createlocatesRelationship(startNode, endNode):
    try:
        startNode.locates.connect(endNode)
    except:
        return False
    return True

# create relationship : user ratings opportinuity
def createhas_ratedRelationship(startNode, endNode, ratings):
    try:
        startNode.has_rated.connect(endNode, {'ratings':ratings})
    except:
        return False
    return True

# create relationship between user and opportinuity to see later
def createhas_pred_laterRelationship(startNode, endNode):
    try:
        startNode.has_pred_later.connect(endNode)
    except:
        return False
    return True


"""Read user and relationships"""
# Search user by her email
def searchUserByEmail(email):
    return User.nodes.get_or_none(email=email)



# Search user by her uid
def searchUserById(uid):
    user = None
    try:
        user = User.nodes.get_or_none(uid=uid)
    except:
        return None
    return user

# Search user by her id_user_for_pred
def searchUserById_User_For_Pred(id_user_for_pred):
    user = None
    try:
        user = User.nodes.get_or_none(id_user_for_pred=id_user_for_pred)
    except:
        return None
    return user


"""Update user and relationships"""


"""Delete user and relationships"""