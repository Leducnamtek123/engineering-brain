from django.db import models


class JobPost(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [(STATUS_OPEN, "Open"), (STATUS_CLOSED, "Closed")]

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="job_posts")
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)


class JobPostActivity(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="activities")
    actor = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
