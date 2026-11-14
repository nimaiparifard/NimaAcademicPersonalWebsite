from django.db import models
from django.urls import reverse


class SiteProfile(models.Model):
    """Single row: who you are. Edit it in the admin (there is only ever one)."""

    name = models.CharField(max_length=100, default="Nima Parifard")
    headline = models.CharField(max_length=200, help_text="One line under your name")
    availability = models.CharField(max_length=200, blank=True, help_text="e.g. 'Open to PhD positions in Europe'")
    short_bio = models.TextField(help_text="2-3 sentences on the home page")
    long_bio = models.TextField(blank=True, help_text="About page. Blank line = new paragraph")
    research_interests = models.TextField(blank=True, help_text="One interest per line")
    photo = models.ImageField(upload_to="profile/", blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    google_scholar = models.URLField(blank=True)
    orcid = models.URLField(blank=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, help_text="PDF offered as 'Download CV'")

    class Meta:
        verbose_name = "Site profile"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        return cls.objects.first()

    def interests(self):
        return [l.strip() for l in self.research_interests.splitlines() if l.strip()]


class Experience(models.Model):
    class Kind(models.TextChoices):
        WORK = "work", "Industry"
        RESEARCH = "research", "Research"
        TEACHING = "teaching", "Teaching"

    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.WORK)
    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    period = models.CharField(max_length=60, help_text="Free text, e.g. '2023 – 2025' or '2024 – Present'")
    description = models.TextField(blank=True, help_text="One bullet per line")
    order = models.PositiveIntegerField(default=0, help_text="Lower = higher on the page")

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return f"{self.title} – {self.organization}"


class Education(models.Model):
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    period = models.CharField(max_length=60)
    gpa = models.CharField(max_length=40, blank=True)
    supervisor = models.CharField(max_length=120, blank=True)
    thesis = models.CharField(max_length=250, blank=True)
    notes = models.TextField(blank=True, help_text="One bullet per line")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} – {self.institution}"


class SkillGroup(models.Model):
    name = models.CharField(max_length=80)
    skills = models.TextField(help_text="Comma separated")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Award(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150, blank=True)
    year = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    date = models.DateField()
    summary = models.CharField(max_length=300, help_text="Shown in lists")
    body = models.TextField(blank=True, help_text="Optional full text. Blank line = new paragraph")
    image = models.ImageField(upload_to="news/", blank=True)
    link = models.URLField(blank=True, help_text="Optional external link")
    pinned = models.BooleanField(default=False)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-pinned", "-date", "-id"]
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", args=[self.slug])
