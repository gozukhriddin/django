from django.contrib import admin
from .models import ProfileUser
# Register your models here.


@admin.register(ProfileUser)
class ProfileUser(admin.ModelAdmin):
    list_display = ['user', 'photo', 'date_brith']
