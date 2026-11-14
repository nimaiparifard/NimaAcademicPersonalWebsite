from django.contrib import admin

from .models import Award, Education, Experience, NewsItem, SiteProfile, SkillGroup


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NewsItem)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "pinned", "published")
    list_editable = ("pinned", "published")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "kind", "period", "order")
    list_editable = ("order",)
    list_filter = ("kind",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "period", "order")
    list_editable = ("order",)


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "year", "order")
    list_editable = ("order",)
