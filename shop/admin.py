from django.contrib import admin

from .models import Shop, Product, Supplies, Sales

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Supplies)
admin.site.register(Sales)
