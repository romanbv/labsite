from django.urls import path, include
from .views import *


app_name = 'account'

urlpatterns = [
    # post views
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password_change/', password_change_view, name='password_change'),
    path('profile/', profile_view, name='profile'),
    #path('', include('django.contrib.auth.urls')),
    #path('profile', views.user_login),

]