from django.db import models
from django.urls import reverse


class Project(models.Model):
    class Status(models.TextChoices):
        DONE = "done", "Completed"
        ACTIVE = "active", "In progress"
        RESEARCH = "research", "Research prototype"

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=300, help_text="Card text")
    description = models.TextField(blank=True, help_text="Full write-up. Blank line = new paragraph")
    highlights = models.TextField(blank=True, help_text="Key points, one bullet per line")
    metrics = models.TextField(blank=True, help_text="One 'Label: value' per line, e.g. 'ROC-AUC: 0.793'")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DONE)
    category = models.CharField(max_length=60, blank=True, help_text="e.g. LLM, MLOps, Graph ML (used for filtering)")
    tech = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    cover = models.ImageField(upload_to="projects/covers/", blank=True)
    repo_url = models.URLField(blank=True, verbose_name="Code (GitHub)")
    demo_url = models.URLField(blank=True, verbose_name="Live demo")
    paper_url = models.URLField(blank=True, verbose_name="Paper / write-up")
    year = models.CharField(max_length=20, blank=True)
    featured = models.BooleanField(default=False, help_text="Show on the home page")
    published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower = first")

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])


class ProjectMedia(models.Model):
    """Screenshots, demo videos (uploaded) or YouTube/Vimeo links for a project."""

    class Kind(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Uploaded video (mp4/webm)"
        EMBED = "embed", "YouTube / Vimeo link"

    project = models.ForeignKey(Project, related_name="media", on_delete=models.CASCADE)
    kind = models.CharField(max_length=6, choices=Kind.choices, default=Kind.IMAGE)
    image = models.ImageField(upload_to="projects/gallery/", blank=True, help_text="For 'Image'; also the poster for a video")
    video = models.FileField(upload_to="projects/videos/", blank=True)
    embed_url = models.URLField(blank=True, help_text="Paste the normal YouTube/Vimeo page link")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "media item"

    def __str__(self):
        return f"{self.project} – {self.kind}"

    def embed_src(self):
        """Convert a watch URL into an embeddable one (privacy-friendly domain)."""
        from urllib.parse import parse_qs, urlparse

        u = urlparse(self.embed_url)
        host = u.netloc.replace("www.", "")
        if host in ("youtube.com", "m.youtube.com"):
            vid = parse_qs(u.query).get("v", [""])[0] or u.path.rstrip("/").split("/")[-1]
            return f"https://www.youtube-nocookie.com/embed/{vid}"
        if host == "youtu.be":
            return f"https://www.youtube-nocookie.com/embed/{u.path.strip('/')}"
        if host == "vimeo.com":
            return f"https://player.vimeo.com/video/{u.path.strip('/')}"
        return self.embed_url

    def embed_poster(self):
        """Thumbnail for YouTube so we don't load the heavy iframe until clicked."""
        src = self.embed_src()
        if "youtube-nocookie.com/embed/" in src:
            return f"https://i.ytimg.com/vi/{src.rsplit('/', 1)[-1]}/hqdefault.jpg"
        return ""
