from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('question_detail/', views.question_detail, name='question-detail'),
    path('add_question/', views.add_question, name='add-question'),
    path('login_or_signup/', views.login_signup, name='login-signup'),
    path('logout/', views.logout_or_remove_session, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('reload_session/', views.reloadSession, name='reload-session'),
    path('requests/', views.question_requests, name='requests'),
]