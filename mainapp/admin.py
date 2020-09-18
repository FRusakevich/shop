from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *


class UnderWearAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='underwear'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HomeWearAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='homewear'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(UnderWear, UnderWearAdmin)
admin.site.register(HomeWear, HomeWearAdmin)

