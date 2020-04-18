from django.contrib import admin
from .models import Post, PostGroup


class GroupInline(admin.StackedInline):
    model = PostGroup
    extra = 0
    verbose_name = "Group"
    verbose_name_plural = "Groups"


class PostAdmin(admin.ModelAdmin):
    inlines = [
        GroupInline,
    ]


admin.site.register(Post, PostAdmin)
