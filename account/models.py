# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

GENDER_CHOICES = [
    ['none', u"Не определенно"],
    ['male', u"Мужской"],
    ['female', u"Женский"],
]

PROFILE_TYPE_CHOICES = [
    ['none', u"Не определенно"],
    ['doctor', u"Врач"],
    ['tehnik', u"Техник"],

]




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u"Пользователь")
    avatar = models.FileField(verbose_name=u"Аватар", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=u"О себе")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name=u"Дата рождения")
    gender = models.CharField(max_length=10, verbose_name=u"Пол", choices=GENDER_CHOICES, default="none")
    profile_type = models.CharField(max_length=20, verbose_name=u"Тип профиля", choices=PROFILE_TYPE_CHOICES, default="none")

    def __str__(self):
        return('Profile: {name}'.format(
            name = self.user,

        ))

# Signals
# @receiver(post_save, sender = User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user = instance)
#
# @receiver(post_save, sender = User)
# def save_user_profile(sender, instance, created, **kwargs):
#     instance.profile.save()