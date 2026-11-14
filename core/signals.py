"""Keep the site fast *and* fresh.

* Any save/delete of site content clears the page cache, so edits in the admin
  appear immediately even though pages are cached for a day.
* Uploaded images get optimised WebP variants; removed images clean them up.
"""
from django.core.cache import cache
from django.db.models import ImageField
from django.db.models.signals import post_delete, post_save

from .images import build_variants, delete_variants

SITE_APPS = {"core", "portfolio", "research", "learning"}


def _image_fields(instance):
    return [f for f in instance._meta.get_fields() if isinstance(f, ImageField)]


def on_save(sender, instance, **kwargs):
    if sender._meta.app_label not in SITE_APPS:
        return
    for f in _image_fields(instance):
        build_variants(getattr(instance, f.name))
    cache.clear()


def on_delete(sender, instance, **kwargs):
    if sender._meta.app_label not in SITE_APPS:
        return
    for f in _image_fields(instance):
        delete_variants(getattr(instance, f.name))
    cache.clear()


post_save.connect(on_save, dispatch_uid="site_save")
post_delete.connect(on_delete, dispatch_uid="site_delete")
