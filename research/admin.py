from django.contrib import admin

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "year", "progress", "featured", "order")
    list_editable = ("status", "progress", "featured", "order")
    list_filter = ("status",)
    search_fields = ("title", "authors", "venue")
