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


def process(opp, opp_similarity, nb_opps):
    topMatches = np.argsort(opp_similarity[opp])[nb_opps - 50:nb_opps]
    register_similarity_opportinuities(opp, topMatches, opp_similarity)


def run(train_data_matrix):
    if not (train_data_matrix.size == 0):
        opp_similarity = pairwise_distances(train_data_matrix.T, metric='manhattan')  # euclidean
        nb_opps = opp_similarity.shape[0]
        for opp in range(nb_opps):
            p = mp.Process(target=process, args=(opp, opp_similarity, nb_opps))
            p.start()
            p.join()


def register_prediction_opportinuities(id_user, id_opp, pred):
    user = searchUserById_User_For_Pred(id_user)
    opp = searchOppById_Opp_For_Pred(id_opp)
    return createhas_predRelationship(user, opp, pred)


def register_similarity_opportinuities(id_opp, topMatches, opp_similarity):
    opp = searchOppById_Opp_For_Pred(id_opp+1)
    opp_sim = opp.has_sim.all()
    if opp_sim == [] or opp_sim == None:
        for i in list(reversed(range(len(topMatches)))):
            opp_other = searchOppById_Opp_For_Pred(topMatches[i])
            distance = opp_similarity[id_opp][topMatches[i]]
            if not (opp==None) and not (opp_other==None) and not (distance == 0) and not (opp.uid == opp_other.uid):
                opp.has_sim.connect(opp_other, { 'distance': distance })
                print(opp_other)
    else:
        listes = []
        for other_sim in list(reversed(range(len(topMatches)))):
            elt = []
            elt.append(topMatches[other_sim])
            elt.append(opp_similarity[id_opp][topMatches[other_sim]])
            if not elt in listes:
                listes.append(elt)
        for op in opp_sim:
            rel = opp.has_sim.relationship(op)
            elt = []
            elt.append(op.id_opp_for_pred)
            elt.append(rel.distance)
            if not elt in listes:
                listes.append(elt)
        opp.has_sim.disconnect_all()
        listes.sort(reverse=True, key=bySecondElt)
        print(listes)
        for elt in listes:
            op = searchOppById_Opp_For_Pred(elt[0])
            if not opp == None and not op == None and not (elt[1] == 0) and not (opp.uid == op.uid):
                opp.has_sim.connect(op, {'distance': elt[1]})


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
