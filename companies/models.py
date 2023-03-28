from django.db import models
from django.contrib.auth.models import User
# Create your models here.



COMPANY_TYPE_CHOICES = [
    ['clinica', u"Клиника"],
    ['laba', u"Лаборатория"],
    ['doctor', u"Врач"],
    ['tehnik', u"Техник"],

]

class Company(models.Model):

    name = models.TextField(max_length=500, blank=True, null=True, verbose_name=u"О себе")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"Город")
    profile_type = models.CharField(max_length=20, verbose_name=u"Тип профиля", choices=COMPANY_TYPE_CHOICES)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete = models.SET_NULL, null = True)