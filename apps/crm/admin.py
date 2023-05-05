from django.contrib import admin
from .models import *
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'number', 'user', 'date', 'date_update')
    list_display_links = ('id', )
    search_fields = ('id', 'number')


admin.site.register(Order, OrderAdmin)

admin.site.register(Company)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', )
    search_fields = ('id', '')

admin.site.register(CompanyType, CompanyTypeAdmin)