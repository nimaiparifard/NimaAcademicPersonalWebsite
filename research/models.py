from django.db import models


class Publication(models.Model):
    """Papers: published, under review, preprints AND the ones you are still writing."""

    class Status(models.TextChoices):
        PUBLISHED = "published", "Published"
        REVIEW = "review", "Under review"
        PREPRINT = "preprint", "Preprint"
        WRITING = "writing", "In preparation"

    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300, help_text="e.g. 'Parifard, N., Momtazi, S.'")
    venue = models.CharField(max_length=200, blank=True, help_text="Journal / conference / 'arXiv'")
    year = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.WRITING)
    progress = models.PositiveSmallIntegerField(default=0, help_text="0-100, shown as a bar for 'In preparation'")
    abstract = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Short public status note, e.g. 'Running ablations'")
    pdf = models.FileField(upload_to="papers/", blank=True)
    arxiv_url = models.URLField(blank=True)
    doi_url = models.URLField(blank=True)
    code_url = models.URLField(blank=True)
    bibtex = models.TextField(blank=True)
    featured = models.BooleanField(default=False, help_text="Show on the home page")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year", "-id"]

    def __str__(self):
        return self.title
