"""Export the whole site as plain HTML files (for Cloudflare Pages / GitHub Pages / Netlify).

    python manage.py build_static --site-url https://yourname.pages.dev

Output goes to ./dist. Upload that folder; no Python needed on the server.
Run it again after every content change you make in /admin.
"""
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.test.utils import override_settings
from django.urls import reverse

from core.models import NewsItem
from portfolio.models import Project

HEADERS = """\
/static/*
  Cache-Control: public, max-age=31536000, immutable

/media/*
  Cache-Control: public, max-age=31536000, immutable
"""


class Command(BaseCommand):
    help = "Render the site to static files in ./dist"

    def add_arguments(self, parser):
        parser.add_argument("--out", default=str(settings.BASE_DIR / "dist"))
        parser.add_argument("--site-url", default=settings.SITE_URL, help="Public URL, used in sitemap/robots")

    def handle(self, *args, **opts):
        out = Path(opts["out"]).resolve()
        site_url = opts["site_url"].rstrip("/")
        if out.name not in ("dist", "public", "build"):  # we delete this folder first, so be strict
            raise CommandError(f"Refusing to wipe {out}; use a dedicated output folder like ./dist")
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)

        overrides = dict(
            DEBUG=False,
            SITE_URL=site_url,
            STATIC_ROOT=out / "static",
            STORAGES={
                "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                # hashed file names -> safe to cache for a year
                "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
            },
            CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
            ALLOWED_HOSTS=["localhost"],
            SECURE_SSL_REDIRECT=False,
        )
        with override_settings(**overrides):
            call_command("collectstatic", interactive=False, verbosity=0)
            (out / "static" / "staticfiles.json").unlink(missing_ok=True)

            client = Client(SERVER_NAME="localhost")
            urls = [reverse(n) for n in ("home", "about", "project_list", "research", "learning", "news_list")]
            urls += [p.get_absolute_url() for p in Project.objects.filter(published=True)]
            urls += [n.get_absolute_url() for n in NewsItem.objects.filter(published=True)]

            for url in urls:
                r = client.get(url)
                if r.status_code != 200:
                    raise CommandError(f"{url} returned {r.status_code}")
                dest = out / url.strip("/") / "index.html" if url != "/" else out / "index.html"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(r.content)

            r404 = client.get("/does-not-exist/")
            (out / "404.html").write_bytes(r404.content)

            sm = client.get("/sitemap.xml").content.decode().replace("http://localhost", site_url)
            (out / "sitemap.xml").write_text(sm, encoding="utf-8")
            (out / "robots.txt").write_bytes(client.get("/robots.txt").content)

        if Path(settings.MEDIA_ROOT).exists():
            shutil.copytree(settings.MEDIA_ROOT, out / "media")
        (out / "_headers").write_text(HEADERS, encoding="utf-8")
        (out / ".nojekyll").write_text("")  # GitHub Pages: don't ignore files starting with _

        size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1e6
        self.stdout.write(self.style.SUCCESS(f"Built {len(urls)} pages -> {out} ({size:.1f} MB)"))
