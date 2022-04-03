from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_type', 'email', 'f_name', 'l_name', 'gender']


class GuestContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'question']


admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(GuestContactUs, GuestContactUsAdmin)