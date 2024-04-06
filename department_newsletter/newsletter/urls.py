from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('create_article/', views.create_article, name='create_article'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
