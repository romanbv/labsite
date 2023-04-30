from django.urls import path, include
from .views import *


app_name = 'apps.userprofiles'

urlpatterns = [
    path('api/users/', GetUserInfoView.as_view()),
    path('check_token', check_token, name = 'check_token'),

]