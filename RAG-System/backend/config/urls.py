from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include


def home(request):
    return HttpResponse(
        "RAG Research Report Generator Backend Running Successfully"
    )

urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),

    path('api/documents/', include('documents.urls')),
    path('api/reports/', include('reports.urls')),
    path(
    "api/dashboard/",
    include("dashboard.urls")
),
]