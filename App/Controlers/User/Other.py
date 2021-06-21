import numpy as np
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from math import fabs, nan

from Technipedia.App.Controlers.Localisation.Crud import *
from Technipedia.App.Controlers.Opportinuity.Crud import *
from Technipedia.App.Controlers.Preference.Crud import *
from Technipedia.App.Controlers.User.Crud import *
from Technipedia.App.config import FromEmail, passwordEmail


# WEB

def sendMail(From, To, password, uid_user):
    username = From
    hostname = 'smtp.gmail.com'
    msg = MIMEMultipart('alternative')
    text = 'Inscription'
    html = """\
    <html>
      <head></head>
      <body>
        <div>
           <h2>
               <a href="http://localhost:8000/sign-up-step-3-4/""" + str(uid_user) + """" target="_blank">
                   <b>CONTINUE YOUR INSCRIPTION HERE ...</b>
                </a>
            </h2>.
        </div>
      </body>
    </html>"""
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    msg['Subject'] = 'COMPLETE INSCRIPTION'
    msg['From'] = From
    msg['To'] = To
    try:
        server = smtplib.SMTP(hostname, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(From, [To], msg.as_string(), )
        server.close()
        return True
    except:
        return False


def registerUserFirstStep(name, surname, email, phoneNumber, economicstatus, pwd):
    userbd = User.nodes.get_or_none(email=email)
    if not (userbd == None):
        return dict(datas='', status=0, errmsg=0)
    if economicstatus == '1':
        economicstatus = 'Entrepreneur'
    elif economicstatus == '2':
        economicstatus = 'Small entreprise'
    elif economicstatus == '3':
        economicstatus = 'Big entreprise'
    user = createUser(name, surname, email, phoneNumber, economicstatus, pwd)
    if user is None:
        return dict(datas='', status=0, errmsg='User don\'t save well...')
    To = email
    user = searchUserByEmail(email)
    user = user.convert()
    if (sendMail(FromEmail, To, passwordEmail, user['uid'])):
        return dict(datas=user, status=1, errmsg='')
    else:
        return dict(datas='', status=0, errmsg=2)


def registerUserSecondStepMobile(email, code):
    user = searchUserByEmail(email)
    print(email)
    print(code)
    try:
        if user.code_auth == code:
            return dict(status=1, uid=user.uid)
    except:
        return dict(status=0)
    return dict(status=1, uid=user.uid)


def registerUserThirdStepMobile(uid, latitude, longitude, place):
    loc = createLocByPositionAndName(place, latitude, longitude)
    user = searchUserById(uid)
    if user == None:
        return dict(status=0)
    user.locates.connect(loc)
    return dict(status=1)


def registerUserFourthStepMobile(preferences_ids):
    user = searchUserById(preferences_ids['uid'])
    prefs = preferences_ids['preference']
    print(prefs)
    for pref in prefs:
        pref_item = Preference.nodes.get(uid=pref)
        user.has_pref.connect(pref_item)
    return dict(status=1)


def checkUser(email, password):
    if email == None and password == None:
        return dict(datas='', status=0, errmsg='')
    elif not password is None and not email is None:
        user = searchUserByEmail(email)
        if user is None:
            return dict(datas='', status=0, errmsg=0)
        data = user.convert()
        if not user.verify_password(password, data['password']):
            return dict(datas='', status=0, errmsg=0)
        if not user.bool_auth:
            return dict(datas='', status=0, errmsg=1)
        return dict(datas=user.user_information_first_step(), status=1, errmsg='')
    else:
        return dict(datas='other', status=0, errmsg='')


def checkUserMobile(email, password):
    if not password is None and not email is None:
        user = User.nodes.get_or_none(email=email)
        if user is None:
            return dict(datas='', status=0, errmsg=0)
        if not user.verify_password(password, user.password):
            return dict(datas='', status=0, errormsg=0)
        if not user.bool_auth:
            datas = dict(uid=user.uid, email=user.email, name=user.name, username=user.username,
                         phonenumber=user.phoneNumber, economic_status=user.economicstatus,
                         location_name=user.locates.all()[0].name)
            return dict(datas=datas, status=0, errmsg=1)
        prefs = user.has_pref.all()
        prefs_send = []
        for pref in prefs:
            prefs_send.append(dict(pref_id=pref.uid, pref_title=pref.name, pref_img_url=pref.pref_image))
            datas = dict(uid=user.uid, email=user.email, name=user.name, username=user.username,
                         phonenumber=user.phoneNumber, economic_status=user.economicstatus,
                         location_name=user.locates.all()[0].name, preferences=prefs_send)
        return dict(datas=datas, status=1, errmsg='')
    else:
        return dict(datas='other', status=0, errormsg='')


def registerUserFinalStep(locations, preferences, iduser):
    user = searchUserById(iduser)
    if user == None:
        return dict(datas='', status=0, errmsg='User don\'t exist')
    for elt in preferences:
        pref = searchPrefById(elt)
        createhas_prefRelationship(user, pref)
    for elt in locations:
        dt = elt.split("|")
        name = dt[0]
        lat = dt[1]
        lon = dt[2]
        loc = searchLocByPositionAndName(name, float(lat), float(lon))
        if loc == None:
            loc = createLocByPositionAndName(name, float(lat), float(lon))
            loc.save()
        createlocatesRelationship(user, loc)
    user.bool_auth = True
    user.save()
    return dict(datas=user.convert(), status=1, errmsg='')


def registerRatingsUserOpp(id_user, id_opp, ratings):
    user = searchUserById(id_user)
    opp = searchOppById(id_opp)
    n_user = len([u for u in User.nodes.all() if u.has_rated.is_connected(opp)])
    if not user.has_rated.is_connected(opp):
        moyenne = ((n_user * opp.moyenne) + ratings) / (n_user + 1)
        opp.moyenne = moyenne
        opp.save()
        createhas_ratedRelationship(user, opp, ratings)
        return dict(datas=opp.convert(), status='succes', errormsg='')
    else:
        rel = user.has_rated.relationship(opp)
        moyenne = ((n_user * opp.moyenne) - rel.ratings + ratings) / (n_user)
        opp.moyenne = moyenne
        opp.save()
        rel.ratings = ratings
        rel.save()
        return dict(datas=opp.convert(), status='succes', errormsg='')


def sendMail_android(From, To, password, randNumber):
    username = From
    hostname = 'smtp.gmail.com'
    msg = MIMEMultipart('alternative')
    text = 'Inscription'
    html = """\
    <html>
      <head></head>
      <body>
        <div>
           <h2>
                <b>YOUR CODE IS """ + str(randNumber) + """ ...</b>
            </h2>.
        </div>
      </body>
    </html>"""
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    msg['Subject'] = 'COMPLETE INSCRIPTION'
    msg['From'] = From
    msg['To'] = To
    try:
        server = smtplib.SMTP(hostname, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(From, [To], msg.as_string(), )
        server.close()
        return True
    except:
        return False


def registerUserFirstStep_android(name, surname, email, phoneNumber, pwd):
    userbd = searchUserByEmail(email=email)
    print(userbd)
    if not userbd == None:
        return dict(status=0, errmsg=1)
    To = email
    code = random.randint(100000, 999999)
    user = createUser_android(name, surname, email, phoneNumber, pwd)
    user.code_auth = code
    user.save()
    if sendMail_android(FromEmail, To, passwordEmail, code):
        return dict(uid=user.uid, status=1)
    else:
        return dict(status=1, errmsg=2)


def listRecommandations(id_user):
    user = searchUserById(id_user)
    cat_list = []
    cats_feuille = Category.nodes.has(contents_pref=True)
    for cat in cats_feuille:
        preferences_cat = [p for p in cat.contents_pref.all() if p.located]
        cat_item_opps, cat_rate = [], 0
        for pref in preferences_cat:
            all_opp = [opp for opp in pref.located.all() if user.has_rated.is_connected(opp)]
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
            if user.has_see_later.relationship(opp_cat_ech):
                seeLater = True
            else:
                seeLater = False
            loc = opp_cat_ech.is_located.all()[0]
            if loc == None:
                name = ''
            else:
                name = loc.name
            opps_cat.append(dict(id_opp=opp_cat_ech.uid, name_opp=opp_cat_ech.name, url_image=opp_cat_ech.opp_image,
                                 mean=opp_cat_ech.moyenne, seeLater=seeLater, location=name))
        data.append(dict(id_cat=cat_ech[0].uid, title_cat=cat_ech[0].name, opp_cat=opps_cat))
    return dict(status=1, errmsg='', datas=data)


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


def addSeeLater(id_user, id_opp):
    user = User.nodes.get(uid=id_user)
    opp = Opportinuity.nodes.get(uid=id_opp)
    user.has_see_later.connect(opp)
    return dict(datas='', status='succes', errmsg='')


def listSeeLater(id_user):
    user = User.nodes.get(uid=id_user)
    opps_see_later = user.has_see_later.all()
    relations = [(user.has_see_later.relationship(opp).date, opp) for opp in opps_see_later]
    dates = list(set([row[0] for row in relations]))
    dates.sort(reverse=True)
    datas = []
    for date in dates:
        opps = [opp for opp in opps_see_later if user.has_see_later.relationship(opp).date == date]
        opps_date = [dict(id_opp=opp.uid, url_image=opp.opp_image, name_opp=opp.name, descr_opp=opp.description,
                          mean=opp.moyenne, name_localisation=opp.is_located.single().name) for opp in opps]
        datas.append(dict(date=date.isoformat(), opp_date=opps_date))
    return dict(status='succes', errmsg='', datas=datas)


def history(id_user):
    opps_see_later = User.nodes.get(uid=id_user).has_hist.all()
    datas = []
    for opp in opps_see_later:
        localisation_name = opp.is_located.single().name
        datas.append(dict(id_opp=opp.uid, name_opp=opp.name, name_localisation=localisation_name))
    return dict(status='succes', errormsg='', datas=datas)


def removeSeeLater(id_user, id_opportunity):
    user = User.nodes.get(uid=id_user)
    opp = Opportinuity.nodes.get(uid=id_opportunity)
    user.has_see_later.disconnect(opp)
    return dict(status=1, errmsg='', datas=[])


def recommendUser(id_user):
    user = searchUserByEmail(id_user)
    data = []
    if not (user == None):
        users = user.has_sim.all()
        for user in users:
            data.append(dict(uid=user.uid, name=user.name, location=user.locates.all()[0].name, username=user.username, url=user.user_image))
        print(data)
        return dict(status=1, errmsg='', datas=data)
    else:
        return dict(status=0, errmsg='', datas='')


def cold_start(id_user):
    user = searchUserById(id_user)
    locs_user = user.locates.all()
    prefs = [pref for pref in user.has_pref.all() if pref.located and user.has_pref]
    data = []
    opps = []
    for pref in prefs:
        opps += [opp for opp in pref.located.all() if opp.economicstatus == user.economicstatus]
    matrix = distance(opps, locs_user)
    sim_opps = []
    for i in range(20):
        if not (len(matrix[0]) == 0):
            ind = np.unravel_index(np.argmin(matrix, axis=None), matrix.shape)
            sim_opps.append(dict(id_opp=opps[ind[0]].uid))
            matrix = np.delete(matrix, ind[0], 0)
        else:
            break

    cats = []
    for sim_opp in sim_opps:
        opp = searchOppById(sim_opp['id_opp'])
        cat = opp.concerns.all()[0].belongs_cat.all()[0]
        if not cats.__contains__(cat):
            cats.append(cat)

    for cat in cats:
        ops = []
        for op in sim_opps:
            opp = searchOppById(op['id_opp'])
            if cat.uid == (opp.concerns.all()[0].belongs_cat.all()[0]).uid:
                loc = opp.is_located.all()[0]
                if loc == None:
                    name = ''
                else:
                    name = loc.name
                ops.append(dict(id_opp=opp.uid, name_opp=opp.name, url_image=opp.opp_image,
                                mean=opp.moyenne, location=name))
        data.append(dict(id_cat=cat.uid, title_cat=cat.name, opp_cat=ops))
    return dict(status=1, errmsg='', datas=data)


# samedi
def cold_start_second(id_user, state='new'):
    user = searchUserById(id_user)
    if state == 'new':
        users_concerned = User.nodes.all()
    if state == 'old':
        users_concerned = user.has_sim.all()
    users_profils_status_concerned = recommendByProfilSearchAndStatus(user, users_concerned)
    users_prefs_concerned = recommendByPrefs(user, users_profils_status_concerned, users_concerned)
    return recommendByLocByPrefs(user, users_prefs_concerned)


# samedi
def recommendUsersToUserForOpportinuity(id_user, id_opp):
    opp = searchOppById(id_opp)
    pref_opp = opp.concerns.all()[0]
    users_concerned = pref_opp.users_pref.all()
    user = searchUserById(id_user)
    users_profils_status_concerned = recommendByProfilSearchAndStatus(user, users_concerned)
    return recommendByLocByUsers(user, users_profils_status_concerned)


# samedi
def recommendByProfilSearchAndStatus(user, users_sim):
    tab = ['Beginner', 'Small Medium Entreprise', 'Industry']
    financial = 'Financial'
    partner = 'Partner'
    mentor = 'Mentor'
    profil = user.profil_search
    status = user.economicstatus
    data = []
    if len(profil) == 1 and partner in profil:
        for user_sim in users_sim:
            if tab.index(user_sim.economicstatus) >= tab.index(status) and partner in user_sim.profil_search:
                data.append(user_sim)
    elif len(profil) == 1 and mentor in profil:
        for user_sim in users_sim:
            if (tab.index(user_sim.economicstatus) > tab.index(status) or user_sim.economicstatus == tab[2]):
                data.append(user_sim)
    elif (len(profil) == 1 and (financial in profil)) or (
            len(profil) == 2 and (mentor in profil) and (financial in profil)):
        for user_sim in users_sim:
            if (tab.index(user_sim.economicstatus) > tab.index(status) and not (
                    financial in user_sim.profil_search)) or user_sim.economicstatus == tab[2]:
                data.append(user_sim)
    elif (len(profil) >= 2) and ((partner in profil and financial in profil) or (
            partner in profil and financial in profil and mentor in profil)):
        for user_sim in users_sim:
            if (tab.index(user_sim.economicstatus) >= tab.index(status) and partner in user_sim.profil_search) and \
                    ((tab.index(user_sim.economicstatus) > tab.index(status) and not (
                            financial in user_sim.profil_search)) or user_sim.economicstatus == tab[2]):
                data.append(user_sim)
    elif (len(profil) == 2) and (partner in profil and mentor in profil):
        for user_sim in users_sim:
            if (tab.index(user_sim.economicstatus) >= tab.index(status) and partner in user_sim.profil_search) and \
                    (tab.index(user_sim.economicstatus) > tab.index(status) or user_sim.economicstatus == tab[2]):
                data.append(user_sim)
    if not len(data) == 0:
        return data
    return users_sim


# samedi
def recommendByPrefs(user, users, AllPrefs):
    vec1 = vecteurPref(searchUserById(user.uid).has_pref.all(), AllPrefs)
    data = []
    for us in users:
        vec2 = vecteurPref(us.has_pref.all(), AllPrefs)
        if len(vec1) == len(vec2):
            d = 0
            for i in range(len(vec2)):
                d += fabs(vec1[i] - vec2[i])
            data.append([us, d])
            data.sort(key=second)
    return data[0:40]


# samedi
def recommendByLocByPrefs(user, prefs_distances):
    data = []
    locs_user = user.locates.all()
    lat1, lon1 = centerLoc(locs_user)
    for dp in prefs_distances:
        locs = dp[0].locates.all()
        if locs == []:
            lat2, lon2 = nan, nan
        else:
            lat2, lon2 = centerLoc(locs)
        data.append([dp[0], fabs(lat1 - lat2) + fabs(lon1 - lon2)])
    data.sort(key=second)
    return data[0:20]


# samedi
def recommendByLocByUsers(user, users_prefs):
    data = []
    locs_user = user.locates.all()
    lat1, lon1 = centerLoc(locs_user)
    for us in users_prefs:
        locs = us.locates.all()
        if locs == []:
            lat2, lon2 = nan, nan
        else:
            lat2, lon2 = centerLoc(locs)
        data.append([us, fabs(lat1 - lat2) + fabs(lon1 - lon2)])
    data.sort(key=second)
    return data[0:20]


# samedi
def vecteurPref(userPrefs, AllPrefs):
    vec = []
    for pref in AllPrefs:
        if pref in userPrefs:
            vec.append(1)
        else:
            vec.append(0)
    return vec


def distance(opps, locs):
    matrix = np.zeros((len(opps), len(locs)))
    for i in range(len(opps)):
        for j in range(len(locs)):
            matrix[i][j] = fabs(locs[j].latitude - opps[i].is_located.all()[0].latitude) + fabs(
                locs[j].longitude - opps[i].is_located.all()[0].longitude)
    return matrix


# samedi
def centerLoc(locs):
    latCenter, lonCenter = 0, 0
    for loc in locs:
        latCenter, lonCenter = latCenter + loc.latitude, lonCenter + loc.longitude
    if not len(locs) == 0:
        return latCenter / len(locs), lonCenter / len(locs)
