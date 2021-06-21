import csv
import random

from Technipedia.App.Controlers.Opportinuity.Other import *
from Technipedia.App.Controlers.Preference.Crud import *
from Technipedia.App.app import connexion

config.DATABASE_URL = connexion


def generateCat(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            Category(name=row[0], pref_image=row[1]).save()
        f.close()

def generateSubCat(path, group):
    cats = [cat for cat in Category.nodes.all() if not cat.contents_cat]
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            cat = cats[random.randint(0, group)]
            sub = Category(name=row[0], pref_image=row[1]).save()
            cat.contents_cat.connect(sub)
        f.close()
    return cats

def generatePreference(path, cats):
    nb_cat = len(cats) - 1
    prefs = []
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            pref = Preference(name=row[0], pref_image=row[1]).save()
            cat = cats[random.randint(0, nb_cat)]
            cat.contents_pref.connect(pref)
            prefs.append(pref)
        f.close()
    return prefs

def generateOpportinuite(path, prefs):
    nb_pref = len(prefs) - 1
    status = ['Small entreprise', 'Big entreprise', 'Entrepreneur']
    opps = []
    i = 0
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            st = random.randint(0, 2)
            opp = Opportinuity(name=row[0], description=row[1], economicstatus=status[st]).save()
            pref = prefs[random.randint(0, nb_pref)]
            pref.located.connect(opp)
            opps.append(opp)
            print(i)
            i = i + 1
        f.close()
    return opps

def generateUser(path, prefs, opps):
    votes = [1, 2, 3, 4, 5]
    status = ['Beginner', 'Small Medium Entreprise', 'Industry']
    nb_pref = len(prefs) - 1
    nb_opp = len(opps) - 1
    i = 0
    users = []
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            st = random.randint(0, 2)
            user = User(name=row[0], surname=row[1], email=row[2], phoneNumber=row[3], economicstatus=status[st])
            password = user.hash_password(row[4])
            user.password = password
            user.save()
            for j in range(random.randint(1, 20)):
                pref = prefs[random.randint(0, nb_pref)]
                opp = opps[random.randint(0, nb_opp)]
                createhas_prefRelationship(user, pref)
                createhas_ratedRelationship(user, opp, votes[random.randint(0, 4)])
            users.append(user)
            print(str(i))
            i = i + 1

def generateLoc(path):
    i = 0
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            Localisation(name=row[0], latitude=float(row[1]), longitude=float(row[2])).save()
            print(str(i))
            i = i + 1
        f.close()

def getUsers():
    return User.nodes.all()

def getOpps():
    return Opportinuity.nodes.all()

def getLocs():
    return Localisation.nodes.all()

def linkUserToLoc(users, locs):
    nb_loc = len(locs) - 1
    i = 0
    for user in users:
        createlocatesRelationship(user, locs[random.randint(0, nb_loc)])
        print(str(i))
        i = i + 1

def linkOppToLoc(opps, locs):
    nb_loc = len(locs) - 1
    i = 0
    for opp in opps:
        createis_locatedRelationship(opp, locs[random.randint(0, nb_loc)])
        print(str(i))
        i = i + 1

def generatePred(users):
    votes = [1, 2, 3, 4]
    i = 0
    for user in users:
        opps = [opp for opp in Opportinuity.nodes.all() if not user.has_rated.is_connected(opp)]
        for opp in opps:
            rand_pred = random.random()
            pred = votes[random.randint(0, 3)] + rand_pred
            createhas_predRelationship(user, opp, pred)
        print(str(i))
        i = i + 1


def moyenneOpp(opps):
    i = 0
    for opp in opps:
        users = opp.interests.all()
        nb_users = len(users)
        moy = 0
        for user in users:
            rel = user.has_rated.relationship(opp)
            moy += rel.ratings
        if not (nb_users == 0):
            moy /= nb_users
            opp.moyenne = moy
            opp.save()
            print(str(i))
            i = i + 1


def run():
    print("starting...")
    generateCat('scripts/categories.csv')
    print(".")
    cats_feuille = generateSubCat('scripts/categories_feuille.csv', 4)
    print("..")
    prefs = generatePreference('scripts/preferences.csv', cats_feuille)
    print("...")
    opps = generateOpportinuite('scripts/opportinuities.csv', prefs)
    print("....")
    generateUser('scripts/users.csv', prefs, opps)
    print(".....")
    generateLoc('scripts/localisations.csv')
    print("......")
    users = getUsers()
    locs = getLocs()
    linkUserToLoc(users, locs)
    print(".......")
    linkOppToLoc(opps, locs)
    print("........")
    generatePred(users)
    print(".........")
    moyenne(opps)
    print("finish....")


# run()

def add_profil_search():
    users = User.nodes.all()
    profils = ['Financial', 'Partner', 'Mentor']
    i = 0
    for user in users:
        user.profil_search = random.sample(set(profils), random.randint(1, 3))
        user.save()
        print(str(i))
        i = i + 1


# add_profil_search()

"""def u():
    users = User.nodes.all()
    status = ['Beginner', 'Small Medium Entreprise', 'Industry']
    i = 0
    for user in users:
        user.economicstatus = status[random.randint(0, 2)]
        user.save()
        print(str(i))
        i = i + 1

u()"""
