from flask import jsonify
from Technipedia.App.Controlers.Preference.Crud import *



def registerPref(id_cat, name, pref_image):
    cat = searchCatById(id_cat)
    if cat is None:
        return jsonify(datas='', status='failure', errmsg='Create category')
    prefs, trouve = searchPrefByIdCatUsingName(id_cat, name)
    if trouve == True:
        return jsonify(datas='', status='failure', errmsg='La preference exists for this cat')
    pref = createPref(name, pref_image)
    if not (pref is None):
        if createcontents_prefRelationship(cat, pref):
            return jsonify(datas='', status='succes', errmsg='')
        else:
            return jsonify(datas='', status='failure', errmsg='relationship don\' create')
    else:
        return jsonify(datas='', status='failure', error_message='Problem about information of preference')


def listPrefByCat():
    cats_feuille = Category.nodes.has(contents_pref=True)
    data=[]
    for cat in cats_feuille:
        prefs = []
        for p in cat.contents_pref.all():
            if p.located:
                prefs.append(dict(id_pref=p.uid, name_pref=p.name, url_image=p.pref_image))
        if not (prefs == []):
            data.append(dict(id_cat=cat.uid, title_cat=cat.name, pref_cat=prefs))
    return dict(datas=data, status=1, errmsg='')

# La fonction suivante est une fonction qui va me permettre de trier les opportunites

def moyenne(opp):
    return opp.moyenne


def second(elem):
    return elem[1]


def somme(tab):
    som = 0
    for i in tab:
        som += i
    return som