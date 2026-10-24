from django.urls import path
from .views import (
    ReportGenerationView,
    DownloadReportPDFView,
    DownloadHTMLView,
    DownloadDOCXView,
    DownloadPPTXView,
    DownloadXLSXView,
    ReportHistoryView
)

urlpatterns = [

    path("generate/", ReportGenerationView.as_view()),

    path("download-pdf/", DownloadReportPDFView.as_view()),

    path("download-html/", DownloadHTMLView.as_view()),

    path("download-docx/", DownloadDOCXView.as_view()),

    path("download-pptx/", DownloadPPTXView.as_view()),

    path("download-xlsx/", DownloadXLSXView.as_view()),
    path("history/",ReportHistoryView.as_view(),name="report-history"),
]