from django.contrib import admin

# Register your models here.
from wechat_manage.models.public_model import PublicAccount


class PublicAccountAdmin(admin.ModelAdmin):
    list_display = (
        'public_name', 'app_id', 'app_secret', 'encrypt_mode', 'encrypt_aes_key', 'token', 'create_time', 'update_time')
    list_display_links = ['public_name']
    search_fields = ['public_name']


admin.site.register(PublicAccount, PublicAccountAdmin)
