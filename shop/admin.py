from django.contrib import admin
from .models import *

class DisplayStatus(admin.ModelAdmin):
    list_display = ('name', 'display_status')

admin.site.register(SuperCategory, DisplayStatus)
admin.site.register(Category, DisplayStatus)
admin.site.register(Products, DisplayStatus)
