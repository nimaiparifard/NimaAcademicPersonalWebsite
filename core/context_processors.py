from django.conf import settings

from .models import SiteProfile


def site(request):
    return {"profile": SiteProfile.get(), "SITE_URL": settings.SITE_URL}
