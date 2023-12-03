from django.contrib import admin

from .models import ItemCategory , Item


# Register your models here.

admin.site.register(Item)

admin.site.register(ItemCategory)
