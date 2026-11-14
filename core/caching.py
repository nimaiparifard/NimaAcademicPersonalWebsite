"""Page cache with correct browser headers.

Django's own cache_page sets max-age = server timeout, which would make visitors
wait a day to see an edit. Here the server keeps the rendered page for a day
(cleared on every save) while browsers revalidate every few minutes; the
ConditionalGetMiddleware ETag turns those revalidations into cheap 304s.
"""
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


def cached_page(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        # Logged-in admins always see fresh pages (handy while editing).
        if request.method != "GET" or request.user.is_authenticated:
            return view(request, *args, **kwargs)
        key = "page:" + request.get_full_path()
        hit = cache.get(key)
        if hit is None:
            response = view(request, *args, **kwargs)
            if hasattr(response, "render"):
                response.render()
            if response.status_code == 200:
                cache.set(key, (response.content, response["Content-Type"]), settings.PAGE_CACHE_SECONDS)
        else:
            response = HttpResponse(hit[0], content_type=hit[1])
        response["Cache-Control"] = (
            f"public, max-age={settings.BROWSER_CACHE_SECONDS}, stale-while-revalidate=86400"
        )
        return response

    return wrapper
