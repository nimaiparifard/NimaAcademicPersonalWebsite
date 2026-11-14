from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.static import serve

from learning.models import Book, Course
from portfolio.models import Project
from research.models import Publication

from .caching import cached_page
from .models import Award, Education, Experience, NewsItem, SkillGroup


@cached_page
def home(request):
    return render(request, "home.html", {
        "news": NewsItem.objects.filter(published=True)[:4],
        "projects": Project.objects.filter(published=True, featured=True)[:3],
        "publications": Publication.objects.filter(featured=True)[:3],
        "reading": Book.objects.filter(status=Book.Status.READING)[:3],
        "learning_now": Course.objects.filter(status=Course.Status.IN_PROGRESS)[:3],
    })


@cached_page
def about(request):
    exp = Experience.objects.all()
    return render(request, "about.html", {
        "education": Education.objects.all(),
        "work": [e for e in exp if e.kind in ("work", "research")],
        "teaching": [e for e in exp if e.kind == "teaching"],
        "skills": SkillGroup.objects.all(),
        "awards": Award.objects.all(),
    })


@cached_page
def news_list(request):
    return render(request, "news_list.html", {"items": NewsItem.objects.filter(published=True)})


@cached_page
def news_detail(request, slug):
    item = get_object_or_404(NewsItem, slug=slug, published=True)
    return render(request, "news_detail.html", {"item": item})


def robots(request):
    body = f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {settings.SITE_URL}/sitemap.xml\n"
    return HttpResponse(body, content_type="text/plain")


def media(request, path):
    """Serve uploads with a 1-year immutable cache header.

    Safe because Django never overwrites a file: a re-upload gets a new name, so a
    given URL always means the same bytes. In production you can serve /media/
    straight from nginx/Caddy/CDN for even better speed and video seeking.
    """
    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response["Cache-Control"] = "public, max-age=31536000, immutable"
    return response
