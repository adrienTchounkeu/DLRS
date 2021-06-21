from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .forms import SignInForm, SignUpFirstStep, user
from .config import *
import requests

categories=requests.get(url=url_category).json()
#categories=[]
def display_sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            request.session['firstname']=user['firstname']
            request.session['id_user']=user['id_user']
            return redirect(home)
        else:
            email = request.POST.get('email')
            error = ''
            for err in form.errors:
                error = form.errors[err]
                break
            return render(request, 'Web/sign-in.html', {'email': email, 'errormsg': error})
    else:
        return render(request, 'Web/sign-in.html')

def logout(request):
    del request.session['firstname']
    del request.session['id_user']
    return redirect(display_sign_in)

def display_sign_up_step_1(request):
    if request.method == 'POST':
        form = SignUpFirstStep(request.POST)
        if form.is_valid():
            return redirect(display_sign_up_step_2)
        else:
            error = ''
            for err in form.errors:
                error = form.errors[err]
                break
            return render(request, 'Web/sign-up-step-1.html', {'firstname': request.POST.get('firstname'),
                        'lastname': request.POST.get('lastname'), 'email': request.POST.get('email'),
                        'phonenumber': request.POST.get('phonenumber'), 'errormsg': error})
    else:
        return render(request, 'Web/sign-up-step-1.html')

def display_sign_up_step_2(request):
    return render(request, 'Web/sign-up-step-2.html')

def display_sign_up_step_3(request, id_user):
    response = requests.get(url=url_preference).json()
    return render(request, 'Web/sign-up-step-3.html', {'id_user': id_user, 'preferences': response['datas']})

def post_sign_up_last_step(request):
    locations=request.POST.get('user_locations').split('-')
    preferences=request.POST.get('user_preferences').split('-')
    del preferences[0]
    #ici on appelle la méthode registerUserFinalStep
    params = {'locations': locations, 'preferences': preferences, 'id_user':request.POST.get('id_user')}
    try:
        if len(locations)==0 or len(preferences)==0:
            raise Exception('bla bla car')
        response = requests.post(url=url_user_register_final_step, json=params).json()
        if response['status'] == 0:
            raise Exception('bla bla car')
    except:
        response = requests.get(url=url_preference).json()
        return render(request, 'Web/sign-up-step-3.html', {'id_user': request.POST.get('id_user'), 'preferences': response['datas']})
    return HttpResponse('/sign-in')

def home(request):
    if request.session.has_key('firstname'):
        #ici on appelle la méthode listRecommendation qui prend en paramètre l'id_user dans la session
        response = requests.post(url=url_user_coldstart, json={'id_user': request.session['id_user']}).json()
        #response = requests.post(url=url_user_recommend, json={'id_user': request.session['id_user']}).json()
        print(response)
        return render(request, 'Web/home.html', {'firstname': request.session['firstname'], 'datas': response['datas'], 'is_connected': True, 'categories': categories})
        """datas=[
            {
                'id_cat': 'cat1',
                'title_cat': 'cat1',
                'opp_cat':[
                    {
                        'id_opp': 'opp1',
                        'name_opp': 'opp1',
                        'location': 'Yaounde, Biyem Assi',
                        'mean': '3.4',
                        'seelater': True
                    },
                    {
                        'id_opp': 'opp2',
                        'name_opp': 'opp2',
                        'location': 'Yaounde, Biyem Assi',
                        'mean': '3.5',
                        'seelater': True
                    }
                ]
            },
            {
                'id_cat': 'cat2',
                'title_cat': 'cat2',
                'opp_cat': [
                    {
                        'id_opp': 'opp3',
                        'name_opp': 'opp3',
                        'location': 'Yaounde, Biyem Assi',
                        'mean': '3.4',
                        'seelater': False
                    },
                    {
                        'id_opp': 'opp4',
                        'name_opp': 'opp4',
                        'location': 'Yaounde, Biyem Assi',
                        'mean': '3.5',
                        'seelater': True
                    }
                ]
            }
        ]
        return render(request, 'Web/home.html',
                      {'firstname': request.session['firstname'], 'id_user': request.session['id_user'],
                       'datas': datas, 'is_connected': True, 'categories': categories})"""
    else:
        #ici on appelle la méthode listTopOpportunities
        response = requests.get(url=url_opportunity).json()
        return render(request, 'Web/home.html', {'datas': response['datas'], 'is_connected': False, 'categories': categories})

def category(request, idcat):
    #ici on appelle la méthode listOpportunitiesOfCat qui prend en paramètre idcat
    if request.session.has_key('firstname'):
        response = requests.post(url=url_category, json={'id_cat': idcat, 'id_user': request.session['id_user']}).json()
        return render(request, 'Web/category.html', {'firstname': request.session['firstname'], 'datas': response['datas'], 'is_connected': True, 'categories': categories})
    else:
        response = requests.post(url=url_category, json={'id_cat': idcat, 'id_user': ''}).json()
        return render(request, 'Web/category.html', {'datas': response['datas'], 'is_connected': False, 'categories': categories})

def display_see_later(request):
    if request.session.has_key('firstname'):
        # ici on appelle la méthode listSeelater qui prend en paramètre l'id_user dans la session
        response = requests.post(url=url_seelater,
                                 json={'id_user': request.session['id_user'], 'listSeeLater': 1}).json()
        print(response)
        return render(request, 'Web/see-later.html',
                      {'firstname': request.session['firstname'], 'datas': response['datas'], 'is_connected': True, 'categories': categories})
    else:
        raise Http404

def display_history(request):
    if request.session.has_key('firstname'):
        # ici on appelle la méthode listRecommendation qui prend en paramètre l'id_user dans la session
        response = requests.post(url=url_opportunity,
                                 json={'id_user': request.session['id_user']}).json()
        print(response)
        datas = {}
        return render(request, 'Web/history.html',
                      {'firstname': request.session['firstname'], 'datas': datas, 'is_connected': True, 'categories': categories})
    else:
        raise Http404

def display_profile(request):
    return render(request, 'Web/profile.html')

def display_about(request):
    return render(request, 'Web/about.html')

def display_policy(request):
    return render(request, 'Web/policy.html')

def search(request):
    return render(request, 'Web/search.html')

def opportunity(request, id_opp):
    if request.session.has_key('firstname'):
        response = requests.post(url=url_details, json={'id_opp': id_opp, 'id_user': request.session['id_user']}).json()
        print(response)
        return render(request, 'Web/watch.html', {'firstname': request.session['firstname'], 'datas': response['datas'], 'is_connected': True, 'categories': categories})
    else :
        response = requests.post(url=url_details, json={'id_opp': id_opp, 'id_user':''}).json()
        return render(request, 'Web/watch.html', {'datas': response['datas'], 'is_connected': False, 'categories': categories})

def post_note(request):
    return HttpResponse('/sign-in')

def post_comment(request):
    return HttpResponse('/sign-in')

def add_see_later(request):
    print('ajout dans see later')
    print(request.POST.get('id_opp'))
    response = requests.put(url=url_seelater, json={'id_user': request.session['id_user'], 'id_opp': request.POST.get('id_opp')}).json()
    return HttpResponse('/sign-in')

def remove_see_later(request):
    print('retrait de see later')
    print(request.POST.get('id_opp'))
    response = requests.delete(url=url_seelater, json={'id_user': request.session['id_user'], 'id_opp': request.POST.get('id_opp')}).json()
    return HttpResponse('/sign-in')
