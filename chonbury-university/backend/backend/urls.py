from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_home

urlpatterns = [
    path('', api_home),
    path('admin/', admin.site.urls),
    path('api/courses/', include('courses.urls')),
    path('api/faculty/', include('faculty.urls')),
    path('api/transport/', include('transport.urls')),
    path('api/inquiries/', include('inquiries.urls')),
    path('api/admissions/', include('admissions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)