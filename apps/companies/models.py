from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.



COMPANY_TYPE_CHOICES = [
    ['clinica', u"Клиника"],
    ['laba', u"Лаборатория"],
    ['doctor', u"Врач"],
    ['tehnik', u"Техник"],

]

class CompanyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
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
        return reverse('companies:company', kwargs={'company_id': self.pk})

