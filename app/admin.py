from django.contrib import admin
from models import feather_models


# Register your models here.
class FeatherModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'feather_class', 'created_at', 'updated_at', 'status']
    fields = ['name','feather_class','status']
    search_fields = ['name']


admin.site.register(feather_models.FeatureModel, FeatherModelAdmin)
