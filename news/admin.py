from django.contrib import admin
from .models import Newa, Category, ContactForm, Comment

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



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','created', 'is_activ']
    list_filter = ['is_activ', 'created']
    search_fields = ['body','user']
    #actions = ['disable_comments', 'active_comments']

    # def disable_comments(self, request, queryset):
    #     queryset.update(is_active=False)
    #
    # def active_comments(self, request, queryset):
    #     queryset.update(is_active=True)