from django.shortcuts import render

from core.caching import cached_page

from .models import Publication


@cached_page
def research(request):
    pubs = Publication.objects.all()
    done = [p for p in pubs if p.status in ("published", "review", "preprint")]
    writing = [p for p in pubs if p.status == "writing"]
    return render(request, "research.html", {"done": done, "writing": writing})
