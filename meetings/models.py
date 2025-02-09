from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    transcript = models.TextField()
    summary = models.TextField()
    action_log = models.TextField()  # NEW: Store action log in Markdown format
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.title

