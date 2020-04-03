from django.contrib import admin
from .models import Topic, TopicReading


class ReadingInline(admin.StackedInline):
    model = TopicReading
    extra = 0
    min_num = 1
    verbose_name = "Reading"
    verbose_name_plural = "Readings"


class TopicAdmin(admin.ModelAdmin):
    inlines = [
        ReadingInline,
    ]


admin.site.register(Topic, TopicAdmin)
