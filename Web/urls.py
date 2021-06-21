from django.urls import path

from . import views

urlpatterns = [
    path('sign-in', views.display_sign_in, name='display_sign_in'),
    path('logout', views.logout, name='logout'),
    path('sign-up-step-1', views.display_sign_up_step_1, name='display_sign_up_step_1'),
    path('sign-up-step-2', views.display_sign_up_step_2, name='display_sign_up_step_2'),
    path('sign-up-step-3-4/<slug:id_user>', views.display_sign_up_step_3, name='display_sign_up_step_3'),
    path('sign-up-last-step', views.post_sign_up_last_step, name='post_sign_up_last_step'),
    # appelé via ajax uniquement
    path('home', views.home, name='home'),
    #path('', views.home, name='home'),
    path('category/<slug:idcat>', views.category, name='category'),
    path('see-later', views.display_see_later, name='display_see_later'),
    path('history', views.display_history, name='display_history'),
    path('profile', views.display_profile, name='display_profile'),
    path('about', views.display_about, name='display_about'),
    path('policy', views.display_policy, name='display_policy'),
    path('search', views.search, name='search'),
    path('opportunity/<slug:id_opp>', views.opportunity, name='opportunity'),
    path('post-note', views.post_note, name='post_note'),  # appelé via ajax uniquement
    path('post-comment', views.post_comment, name='post_comment'),  # appelé via ajax uniquement
    path('add-see-later', views.add_see_later, name='add_see_later'),  # appelé via ajax uniquement
    path('remove-see-later', views.remove_see_later, name='remove_see_later'),  #appelé via ajax uniquement
]