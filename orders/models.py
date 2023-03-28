from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

COMPANY_TYPE_CHOICES = [
    ['clinica', u"Клиника"],
    ['laba', u"Лаборатория"],
    ['doctor', u"Врач"],
    ['tehnik', u"Техник"],

]


class Order(models.Model):
    UID = models.CharField(verbose_name='UID',db_index=True, max_length=64)
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name="Номер")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

