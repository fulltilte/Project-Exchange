from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'user_bio', 'user_mask_name', ]

fields = list(UserAdmin.fieldsets) #Unpacking admin fieldsets
fields[0] = (None, {'fields': ('username', 'password','user_bio', 'user_mask_name')}) #adding fields from custom user
UserAdmin.fieldsets = tuple(fields) #packing back new set

admin.site.register(CustomUser, CustomUserAdmin)