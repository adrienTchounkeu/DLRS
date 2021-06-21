import csv
import os
import pandas as pd

from Technipedia.App.Models.UserModel import User
from Technipedia.App.Models.OpportinuityModel import Opportinuity
from Technipedia.App.RecSys.config import protocolConnexion, usernameConnexion, passwordConnexion, hoteConnexion, portConnexion

from neomodel import config


connexion = protocolConnexion+'://'+usernameConnexion+':'+passwordConnexion+'@'+hoteConnexion+':'+portConnexion
config.DATABASE_URL = connexion

def getUsers():
    return User.nodes.all()


def getOpps():
    return Opportinuity.nodes.all()


def order_id_users():
    print("users")
    users = getUsers()
    id = 1
    for user in users:
        user.id_user_for_pred = id
        user.save()
        id += 1
        print(str(id))
    return users


def order_id_opportinuity():
    print("opportinuities")
    opps = getOpps()
    id = 1
    for opp in opps:
        if opp.active == True:
            opp.id_opp_for_pred = id
            opp.save()
            id += 1
            print(str(id))
    return opps


def write_in_csv_file(path):
    users = order_id_users()
    order_id_opportinuity()
    if os.access(path, os.F_OK):
        if os.access(path, os.W_OK):
            FillData(path, users)
    else:
        FillData(path, users)


def read_in_csv_file(path):
    if os.access(path, os.F_OK) and os.access(path, os.R_OK):
        df_train = pd.read_csv(path, sep=',', names=['user', 'item', 'rate'], skiprows=1)
        users_number = len(getUsers())
        items_number = len(getOpps())
        return df_train, users_number, items_number


def FillData(path, users):
    with open(path, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for user in users:
            opps_user = user.has_rated.all()
            for opp_user in opps_user:
                rel = user.has_rated.relationship(opp_user)
                spamwriter.writerow([user.id_user_for_pred, opp_user.id_opp_for_pred, rel.ratings])
        csvfile.close()


if __name__ == "__main__":
    while True:
        path = 'ratings.csv'
        write_in_csv_file(path)