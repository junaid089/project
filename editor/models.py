from django.db import models
from django.utils import timezone


class Asset(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or f"Asset {self.pk}"


class EditPreset(models.Model):
    name = models.CharField(max_length=100)
    settings = models.JSONField(default=dict)  # brightness, contrast, saturation, etc.

    def __str__(self):
        return self.name


class Job(models.Model):
    TYPE_CHOICES = [
        ('manual', 'Manual Adjustment'),
        ('object_removal', 'Object Removal'),
        ('ai_process', 'AI Process'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    params = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Job {self.pk} ({self.job_type})"


class Version(models.Model):
    """Store snapshots of an Asset's edit action list for history/restore."""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='versions')
    actions = models.JSONField(default=list)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Version {self.pk} for Asset {self.asset_id} at {self.created_at}"


class GeneratorJob(models.Model):
    """Track prompt->images generation jobs (placeholder/demo)."""
    prompt = models.TextField()
    count = models.PositiveSmallIntegerField(default=1)
    size = models.CharField(max_length=32, default='512x512')
    created_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    result_assets = models.ManyToManyField(Asset, blank=True, related_name='generator_jobs')

    def __str__(self):
        return f"GeneratorJob {self.pk} ({'done' if self.completed else 'pending'})"
