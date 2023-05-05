from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import yadisk

from .models import *

class CompanyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Тип компании"
        verbose_name_plural = "Типы компаний"

class Company(models.Model):

    name = models.TextField(max_length=500, blank=True, null=True, verbose_name=u"Название")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"Город")
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete = models.SET_NULL, null = True)
    type = models.ForeignKey(CompanyType, verbose_name=u"Тип компании", on_delete=models.SET_DEFAULT, default = 1)
    def __str__(self):
        return('{name}'.format(
            name = self.name,

        ))
    def get_absolute_url(self):
        return reverse('crm:company', kwargs={'company_id': self.pk})
    class Meta():
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
class Order(models.Model):

    company = models.ForeignKey(Company, verbose_name='Компания',  on_delete=models.CASCADE)
    number = models.CharField(max_length= 9, verbose_name="Номер")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    date = models.DateTimeField (auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.number


    def get_absolute_url(self):
        return reverse('crm:order', kwargs={'order_num': self.number})

    class Meta():
        verbose_name = "Заказы"
        verbose_name_plural = "Заказы"


class OrderFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    yandex_file_path = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order, verbose_name='Заказ',  on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                loader = yadisk.YaDisk('4bf5384cd0904299a07adcb616cc0e08', 'cc9a5b4b894e40649b8e2bd8be5aad5f', 'y0_AgAAAAALE7y3AAm3GAAAAADhGLoR90SrSie4Q7Sh8hEJ6f29c5MBG9E')

                path = f"/{self.file.name}"
                yapath = f"/Projects/{self.file.name}"
                 # Создать папку
                loader.upload(path, yapath)
                self.yandex_file_path = yapath
            except:
                self.yandex_file_path = None
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('orders:order', kwargs={'order_num': self.order})

class Pricelist(models.Model):

    number = models.CharField(max_length= 9, verbose_name="Номер")
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return('{name}'.format(
            name = self.name,
        ))

class ProductGroup(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Наименование")

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Наименование")
    code = models.CharField(max_length=10, blank=False, verbose_name="Код")
    group = models.ForeignKey(ProductGroup, verbose_name='Группа', on_delete=models.CASCADE)
    pricelist = models.ForeignKey(Pricelist, verbose_name='Прайс', on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True, default=None, verbose_name="Цена")
    def __str__(self):
        return self.name


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Изделие', on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True, default=None, verbose_name="Количество")



