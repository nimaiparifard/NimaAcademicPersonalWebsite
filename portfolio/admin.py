from django.contrib import admin

from .models import Project, ProjectMedia


class ProjectMediaInline(admin.StackedInline):
    model = ProjectMedia
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "year", "featured", "published", "order")
    list_editable = ("featured", "published", "order")
    list_filter = ("status", "category", "published")
    search_fields = ("title", "summary", "tech")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectMediaInline]
