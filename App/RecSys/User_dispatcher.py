from Technipedia.App.Controlers.User.Crud import *
from Technipedia.App.Controlers.Opportinuity.Crud import *

import csv
import multiprocessing as mp
import os


def dispatch(matrix, path):
    multi_process(func=user_recommend, matrix=matrix, path=path)


def secondElt(elt):
    return elt[1]


def multi_process(func, matrix, path):
    pool = mp.Pool()
    [pool.apply_async(func, (path, indice, ligne)) for indice, ligne in enumerate(matrix)]
    pool.close()
    pool.join()


def user_recommend(path, indice, ligne):
    id_user = searchUserById_User_For_Pred(indice + 1).uid
    datas = []
    for indiceLigne, oppRecomRate in enumerate(ligne):
        if oppRecomRate > 0:
            id_opp = searchOppById_Opp_For_Pred(indiceLigne + 1).uid
            id_pref = searchIdPrefOfOpp(id_opp)
            datas.append((id_opp, oppRecomRate, id_pref))
    if not (datas == []):
        datas.sort(reverse=True, key=secondElt)
        path = path + '/' + id_user + '.csv'
        if os.access(path , os.F_OK):
            while not (os.access(path, os.W_OK)):
                continue
            with open(path, 'w') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerows(datas)
                csvfile.close()
        else:
            with open(path, 'w') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerows(datas)
                csvfile.close()