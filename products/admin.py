from django.contrib import admin
from .models import product, offer

class offerAdmin(admin.ModelAdmin):
    list_display = ('code','discount')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock')


admin.site.register(offer, offerAdmin)
admin.site.register(product, ProductAdmin)

