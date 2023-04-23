from django.urls import path, include
from .views import *


app_name = 'account'

urlpatterns = [
    # post views
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('<int:user_id>', profile_view, name='profile'),
    path('api/users/', GetUserInfoView.as_view()),
    path('check_token', check_token, name = 'check_token'),
    #path('', include('django.contrib.auth.urls')),
    #path('profile', views.user_login),

]