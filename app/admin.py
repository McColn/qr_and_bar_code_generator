from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(QRCode)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'barcode')