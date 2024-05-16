from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserProfile 


class CustomeUserAdmin(UserAdmin): # custom user admin display 

    model = CustomUser

    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login']
    list_display_links = ['username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'last_login']
    fieldsets = [
        ('Basic Info', {'fields':('username', 'email', 'password')}),
        ('Permissions', {'fields':('is_active','is_staff','is_superuser',
                        'groups','user_permissions')}),
        ('Dates', {'fields': ('last_login',)})
    ]
    ordering = ('username', 'email',)
    search_fields = ['username', 'email']

admin.site.register(CustomUser,CustomeUserAdmin)


class UserAdmin(admin.ModelAdmin): # user profile admin
    list_display = ['display_name','user','login_trials','max_login_trials','time']
    list_display_links = ['display_name','user','time']

admin.site.register(UserProfile,UserAdmin)