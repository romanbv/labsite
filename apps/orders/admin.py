from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'UID', 'company', 'number', 'user', 'date', 'date_update')
    list_display_links = ('id', )
    search_fields = ('id', 'number')


admin.site.register(Order, OrderAdmin)
