from django.db import models
from documents.models import QueryHistory
import uuid


class GeneratedReport(models.Model):
    report_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    query = models.ForeignKey(
        QueryHistory,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    report_title = models.CharField(
        max_length=255
    )

    report_content = models.TextField()

    pdf_file = models.FileField(
        upload_to="reports/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default="completed"
    )

    def __str__(self):
        return self.report_title