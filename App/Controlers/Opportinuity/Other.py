from flask import jsonify
from Technipedia.App.Controlers.Opportinuity.Crud import *
from Technipedia.App.Controlers.Preference.Crud import *
from Technipedia.App.Controlers.User.Crud import *
from Technipedia.App.Controlers.Localisation.Crud import *


def registerOpp(id_pref, name, description, name_loc, latitude, longitude):
    pref = searchPrefById(id_pref)
    if pref == None:
        return jsonify(datas='', status=0, errmsg='create preference before in a category')
    opp = createOpp(name, description)
    if not (opp is None):
        if createLocatedRelationship(pref, opp):
            loc = createLocByPositionAndName(name=name_loc, latitude=latitude, longitude=longitude)
            if not (loc is None):
                if createis_locatedRelationship(opp, loc):
                    return jsonify(datas='', status=1, errmsg='')
                else:
                    return jsonify(datas='', status=0, errmsg='Relationship between opportinuity and localisation don\'t create')
        else:
            return jsonify(datas='', status=0, errmsg='Problem of relationship')
    else:
        return jsonify(datas='', status=0, errmsg='Problem about information of opportinuity')


def listTopOpportunity():
    cat_list = []
    cats_feuille = Category.nodes.has(contents_pref=True)
    for cat in cats_feuille:
        preferences_cat = [p for p in cat.contents_pref.all() if p.located]
        cat_item_opps, cat_rate = [], 0
        for pref in preferences_cat:
            all_opp = [opp for opp in pref.located.all() if opp.interests]
            cat_rate += somme([op.moyenne for op in all_opp])
            for opp in all_opp:
                cat_item_opps.append(opp)
        cat_item_opps.sort(reverse=True, key=moyenne)
        cat_item_opps = cat_item_opps[:4]
        cat_list.append((cat, cat_rate, cat_item_opps))
    cat_list.sort(reverse=True, key=second)
    real_cat = cat_list[:10]
    data = []
    for cat_ech in real_cat:
        opps_cat = []
        for opp_cat_ech in cat_ech[2]:
            opps_cat.append(dict(id_opp=opp_cat_ech.uid, name_opp=opp_cat_ech.name, url_image=opp_cat_ech.opp_image,
                     mean=opp_cat_ech.moyenne))
        data.append(dict(id_cat=cat_ech[0].uid, title_cat=cat_ech[0].name, opp_cat=opps_cat))
    return dict(status=1, errormsg='', datas=data)


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

# Fin des fonctions utilisees dans la fonction precedente


def detailsOpportinuity(id_opp, id_user):
    if not (id_user == ''):
        user = searchUserById(id_user)
    opp = searchOppById(id_opp)
    loc = opp.is_located.all()[0]
    opps =  []
    if loc == None:
        name_loc = ''
        lat_loc = ''
        lon_loc = ''
    else:
        name_loc=loc.name
        lat_loc = loc.latitude
        lon_loc = loc.longitude
    opps_sim = opp.has_sim.all()
    op_sim = []
    for op in opps_sim:
        loc = op.is_located.all()[0]
        if loc == None:
            name = ''
        else:
            name = loc.name
        if not (id_user == ''):
            if user.has_see_later.is_connected(op):
                see_later = True
            else:
                see_later = False
            op_sim.append(dict(id_opp=op.uid, title=op.name, url_img=op.opp_image, mean=op.moyenne, see_later=see_later ,location=name))
        else:
            op_sim.append(dict(id_opp=op.uid, title=op.name, url_img=op.opp_image, mean=op.moyenne,location=name))
    localisation = dict(lng=lat_loc, lat=lon_loc, name=name_loc)
    cat_node = opp.concerns.all()[0].belongs_cat.all()[0]
    cat = dict(id_cat=cat_node.uid, name_cat=cat_node.name)
    if not (id_user == ''):
        if opp.users_see_later.is_connected(user):
            see_later = True
        else:
            see_later = False
    if not (id_user == ''):
        opps = dict(title=opp.name, url_img=opp.opp_image, average=opp.moyenne, description=opp.description, see_later=see_later, localisation=localisation, cat=cat,sim_opp=op_sim)
    else:
        opps = dict(title=opp.name, url_img=opp.opp_image, average=opp.moyenne, description=opp.description, localisation=localisation, cat=cat,sim_opp=op_sim)
    return dict(datas=opps, status=1, errmsg='')

