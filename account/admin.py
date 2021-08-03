from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):

	list_display = ('user', 'user_type', 'phone_number','company','company_description') #specify the fields to display


class MyUserAdmin(admin.ModelAdmin):

	list_display = ('firstname', 'lastname', 'is_admin','is_staff','is_superadmin','is_active') #specify the fields to display

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)



