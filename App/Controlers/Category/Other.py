from flask import jsonify
from Technipedia.App.Controlers.Category.Crud import *
from Technipedia.App.Controlers.User.Crud import searchUserById

from Technipedia.App.Controlers.User.Other import *
from Technipedia.App.Controlers.Category.Other import *


def registerCat(name, pref_image):
    """cat = searchCatByName(name)
    if not (cat == None):
        return jsonify(datas='', status='failure', errormsg='Cat exists')"""
    cat = createCat(name, pref_image)
    if not (cat is None):
        return jsonify(datas=cat.convert(), status='succes', error_msg='')
    else:
        return jsonify(datas='', status='failure', errormsg='Problem about category information')


def registerSubCat(idCat, name, pref_image):
    cat = searchCatById(idCat)
    sub_cat = createCat(name, pref_image)
    if not (sub_cat is None):
        if createcontents_prefRelationship(cat, sub_cat):
            return jsonify(datas='', status=1, errmsg='')
        else:
            return jsonify(datas='', status=0, errmsg='Relation between category and category don\'t give')


def listCatMobile():
    cats = Category.nodes.has(contents_pref=True)
    cats = cats[:20]
    print(len(cats))
    datas = []
    for cat in cats:
        datas.append(dict(id_category=cat.uid, name_category=cat.name, url_img_category=cat.pref_image))
    print(datas)
    return dict(status=1, category=datas)


def listCatPrefMobile(categories_ids):
    print(categories_ids)
    print('hello')
    datas = []
    user = searchUserById(categories_ids['uid'])
    user.economicstatus = categories_ids['economic_status']
    user.save()
    for uid in categories_ids['category']:
        cat = searchCatById(uid)
        preferences = [pref for pref in cat.contents_pref.all() if pref.located][:20]
        preferences_display = []
        for pref in preferences:
            preferences_display.append(dict(pref_id=pref.uid, pref_title=pref.name, pref_img_url=pref.pref_image))
        datas.append(dict(id_category=uid, name_category=cat.name, preference=preferences_display))
    print(datas)
    return dict(status=1, category=datas)



def listCat():
    cats = Category.nodes.has(contents_pref=True)
    tab_cats = []
    for cat in cats:
        json_cat = {}
        json_cat['id_cat'] = cat.uid
        json_cat['name_cat'] = cat.name
        tab_cats.append(json_cat)
    return tab_cats


def listOpportinuitiesOfCat(id_cat, id_user):
    if not (id_user == ''):
        user = searchUserById(id_user)
    opps = []
    cat = searchCatById(id_cat)
    i = 0
    for pref in cat.contents_pref.all():
        for opp in pref.located.all():
            opps.append(opp)
            i = i + 1
            if i == 10:
                break
        if i == 10:
            break
    opp_cat = []
    for op in opps:
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
            opp_cat.append(dict(id_opp=op.uid, title=op.name, url_img=op.opp_image, mean=op.moyenne, see_later=see_later ,location=name))
        else:
            opp_cat.append(dict(id_opp=op.uid, title=op.name, url_img=op.opp_image, mean=op.moyenne,location=name))
    if not (id_user == ''):
        ops = dict(name_category=cat.name, opp_cat=opp_cat)
    else:
        ops = dict(name_category=cat.name, opp_cat=opp_cat)
    return dict(datas=ops, status=1, errmsg='')
