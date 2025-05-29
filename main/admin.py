from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from .models import *
from ads.models import *
from user_profile.models import *


class UsersAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'reg_time', 'balance')  # Изменено 'name' на 'display_name'
    search_fields = ('telegram_id', 'telegram_name')  # Добавил 'telegram_name' для поиска

    def display_name(self, obj):
        return str(obj)  # Использует метод __str__

    display_name.short_description = 'Имя пользователя'  # Название столбца в админке


class MyAdminSite(AdminSite):

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        #for app in app_list:
        #    app['models'].sort(key=lambda x: x['name'])

        return app_list


admin.site = MyAdminSite()

admin.site.register(Users)
admin.site.register(Ad)
admin.site.register(Categories)
admin.site.register(ExchangeProposal)
