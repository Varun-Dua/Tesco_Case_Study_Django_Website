from django.contrib import admin

from .models import Cards


@admin.register(Cards)
class CardAdmin(admin.ModelAdmin):
    list_display = ['customer', 'gender', 'county', 'affluency']
