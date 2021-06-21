import multiprocessing as mp
import numpy as np
import os
import pandas as pd
from neomodel import config
from sklearn.metrics.pairwise import pairwise_distances

from Technipedia.App.Controlers.Opportinuity.Crud import *
from Technipedia.App.Controlers.User.Crud import *
from Technipedia.App.RecSys.Extract import getOpps, getUsers
from Technipedia.App.RecSys.config import protocolConnexion, usernameConnexion, passwordConnexion, hoteConnexion, \
    portConnexion

connexion = protocolConnexion+'://'+usernameConnexion+':'+passwordConnexion+'@'+hoteConnexion+':'+portConnexion
config.DATABASE_URL = connexion


def load(path, nb_users, nb_opps):
    if os.access(path, os.F_OK) and os.access(path, os.R_OK):
        df = pd.read_csv(path, sep=',')
        train_data_matrix = np.zeros((nb_users, nb_opps))
        for line in df.itertuples():
            train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
        return train_data_matrix


def process(user, user_similarity, nb_users):
    topMatches = np.argsort(user_similarity[user])[nb_users - 50:nb_users]
    register_similarity_users(user, topMatches, user_similarity)


def run(train_data_matrix):
    if not (train_data_matrix.size == 0):
        user_similarity = pairwise_distances(train_data_matrix, metric='manhattan')  # euclidean
        nb_users = user_similarity.shape[0]
        for user in range(nb_users):
            p = mp.Process(target=process, args=(user, user_similarity, nb_users))
            p.start()
            p.join()


def register_prediction_opportinuities(id_user, id_opp, pred):
    user = searchUserById_User_For_Pred(id_user)
    opp = searchOppById_Opp_For_Pred(id_opp)
    return createhas_predRelationship(user, opp, pred)


def register_similarity_users(id_user, topMatches, user_similarity):
    user = searchUserById_User_For_Pred(id_user+1)
    user_sim = user.has_sim.all()
    if user_sim == [] or user_sim == None:
        for i in list(reversed(range(len(topMatches)))):
            user_other = searchUserById_User_For_Pred(topMatches[i])
            distance = user_similarity[id_user][topMatches[i]]
            if not (user == None) and not (user_other == None) and not (distance == 0) and not (user.uid == user_other.uid):
                user.has_sim.connect(user_other, { 'distance': distance })
                print(user_other)
    else:
        listes = []
        for other_sim in list(reversed(range(len(topMatches)))):
            elt = []
            elt.append(topMatches[other_sim])
            elt.append(user_similarity[id_user][topMatches[other_sim]])
            if not elt in listes:
                listes.append(elt)
        for u in user_sim:
            rel = user.has_sim.relationship(u)
            elt = []
            elt.append(u.id_user_for_pred)
            elt.append(rel.distance)
            if not elt in listes:
                listes.append(elt)
        user.has_sim.disconnect_all()
        listes.sort(reverse=True, key=bySecondElt)
        print(listes)
        for elt in listes:
            u = searchUserById_User_For_Pred(elt[0])
            if not u == None and not user == None and not (elt[1] == 0) and not (user.uid == u.uid):
                user.has_sim.connect(u, {'distance': elt[1]})


def bySecondElt(elt):
    return elt[1]

if __name__ == "__main__":
    i = 0
    while (True):
        path = '../ratings.csv'
        nb_users, nb_opps = len(getUsers()), len(getOpps())
        if not (nb_users == 0) and not (nb_opps == 0):
            run(load(path, nb_users, nb_opps))
        print(str(i))
        i = i + 1
        break
