from django.db import models
from django.contrib.auth.models import User
from companies.models import Company
from django.urls import reverse

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
    date = models.DateTimeField (auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.number


    def get_absolute_url(self):
        return reverse('orders:order', kwargs={'order_num': self.number})