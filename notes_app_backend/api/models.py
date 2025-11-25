from django.db import models
from django.contrib.auth import get_user_model


class Note(models.Model):
    """
    Note model storing user notes with title and content.
    """
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notes",
        help_text="User who owns this note",
    )
    title = models.CharField(max_length=255, help_text="Title of the note")
    content = models.TextField(blank=True, help_text="Content/body of the note")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last updated timestamp")

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["owner", "title"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.owner})"
