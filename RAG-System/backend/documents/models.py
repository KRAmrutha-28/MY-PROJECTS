from django.db import models
import uuid


class Document(models.Model):
    document_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to="documents/"
    )

    file_type = models.CharField(max_length=20)

    file_size = models.BigIntegerField(default=0)

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    processing_status = models.CharField(
        max_length=20,
        default="PENDING"
    )

    total_chunks = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class QueryHistory(models.Model):
    query_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.query_text[:50]