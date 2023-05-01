from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import yadisk

from apps.companies.models import Company

COMPANY_TYPE_CHOICES = [
    ['clinica', u"Клиника"],
    ['laba', u"Лаборатория"],
    ['doctor', u"Врач"],
    ['tehnik', u"Техник"],

]


class Order(models.Model):
    UID = models.CharField(verbose_name='UID',db_index=True, max_length=64, null=True)
    company = models.ForeignKey(Company, verbose_name='Компания',  on_delete=models.CASCADE)
    number = models.CharField(max_length= 9, verbose_name="Номер")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    date = models.DateTimeField (auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.number


    def get_absolute_url(self):
        return reverse('orders:order', kwargs={'order_num': self.number})

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