from django.urls import path
from .views import (
    DocumentUploadView,
    DocumentListView,
    QueryView,
    DeleteDocumentView
)

urlpatterns = [
    path("upload/", DocumentUploadView.as_view()),
    path("list/", DocumentListView.as_view()),
    path("query/", QueryView.as_view()),
    path("delete/<uuid:document_id>/",DeleteDocumentView.as_view()),
]