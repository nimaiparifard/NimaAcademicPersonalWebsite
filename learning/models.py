from django.db import models


class Book(models.Model):
    class Status(models.TextChoices):
        READING = "reading", "Reading now"
        FINISHED = "finished", "Finished"
        WANT = "want", "Want to read"

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.READING)
    progress = models.PositiveSmallIntegerField(default=0, help_text="0-100 %")
    rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="1-5, when finished")
    cover = models.ImageField(upload_to="books/", blank=True)
    notes = models.TextField(blank=True, help_text="Your takeaways. Blank line = new paragraph")
    link = models.URLField(blank=True)
    finished_on = models.CharField(max_length=20, blank=True, help_text="e.g. 'Oct 2026'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title


class Course(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "progress", "In progress"
        COMPLETED = "done", "Completed"

    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=150, blank=True, help_text="Coursera, university, ...")
    instructor = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.COMPLETED)
    progress = models.PositiveSmallIntegerField(default=0, help_text="0-100 %, for in-progress courses")
    completed_on = models.CharField(max_length=20, blank=True, help_text="e.g. 'Sep 2026'")
    skills = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    notes = models.TextField(blank=True)
    certificate = models.FileField(upload_to="certificates/", blank=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title
