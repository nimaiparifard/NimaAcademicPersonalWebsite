from django.shortcuts import get_object_or_404, render

from core.caching import cached_page

from .models import Project


@cached_page
def project_list(request):
    projects = Project.objects.filter(published=True)
    categories = sorted({p.category for p in projects if p.category})
    return render(request, "portfolio/list.html", {"projects": projects, "categories": categories})


@cached_page
def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related("media"), slug=slug, published=True)
    return render(request, "portfolio/detail.html", {"project": project})
