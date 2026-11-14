from django.contrib import admin

from .models import Book, Course


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "progress", "rating", "order")
    list_editable = ("status", "progress", "rating", "order")
    list_filter = ("status",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "provider", "status", "progress", "completed_on", "order")
    list_editable = ("status", "progress", "order")
    list_filter = ("status",)
