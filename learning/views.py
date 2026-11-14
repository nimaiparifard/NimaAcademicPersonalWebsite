from django.shortcuts import render

from core.caching import cached_page

from .models import Book, Course


@cached_page
def learning(request):
    books = Book.objects.all()
    courses = Course.objects.all()
    return render(request, "learning.html", {
        "reading": [b for b in books if b.status == "reading"],
        "finished": [b for b in books if b.status == "finished"],
        "want": [b for b in books if b.status == "want"],
        "courses_now": [c for c in courses if c.status == "progress"],
        "courses_done": [c for c in courses if c.status == "done"],
    })
