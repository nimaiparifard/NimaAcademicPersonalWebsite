from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core.models import NewsItem
from portfolio.models import Project


class StaticSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return ["home", "about", "project_list", "research", "learning", "news_list"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    def items(self):
        return Project.objects.filter(published=True)


class NewsSitemap(Sitemap):
    def items(self):
        return NewsItem.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.date


SITEMAPS = {"static": StaticSitemap, "projects": ProjectSitemap, "news": NewsSitemap}
