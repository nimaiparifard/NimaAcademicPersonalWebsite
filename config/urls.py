from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from core import views as core_views
from core.sitemaps import SITEMAPS

admin.site.site_header = "Nima's site – content manager"
admin.site.site_title = "Site admin"
admin.site.index_title = "Add or edit anything on your website"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", core_views.robots, name="robots"),
    re_path(r"^media/(?P<path>.*)$", core_views.media, name="media"),
    path("projects/", include("portfolio.urls")),
    path("research/", include("research.urls")),
    path("learning/", include("learning.urls")),
    path("", include("core.urls")),
]
