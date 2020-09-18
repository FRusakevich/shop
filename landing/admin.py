from django.contrib import admin
from .models import *


# Register your models here.
class BuyerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Buyer._meta.fields]
    search_fields = ('name', 'email')

    class Meta:
        model = Buyer


admin.site.register(Buyer, BuyerAdmin)
