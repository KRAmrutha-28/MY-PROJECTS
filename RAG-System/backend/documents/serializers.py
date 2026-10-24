from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"

        read_only_fields = (
            "document_id",
            "file_type",
            "file_size",
            "uploaded_at",
            "processing_status",
            "total_chunks",
        )