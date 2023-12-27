from django.contrib import admin
from .models import Newa, Category, ContactForm

@admin.register(Newa)
class NewSAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "publish_time", "status"]
    list_filter = ["status", "publish_time"]
    prepopulated_fields = {"slug":("title",)}
    ordering = ["status", "publish_time"]
    search_fields = ["title", "text"]
    date_hierarchy = "publish_time"



@admin.register(Category)
class CategoryaAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

admin.site.register(ContactForm)

