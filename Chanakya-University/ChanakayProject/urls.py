from django.contrib import admin
from django.urls import include, path

# ✅ CORRECT IMPORT
from django.conf import settings
from django.conf.urls.static import static

# ✅ your views
from .views import home, courses, faclty, hostel, transport


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('courses/', courses, name='courses'),
    path('faculty/', faclty, name='faculty'),
    path('hostel/', hostel, name='hostel'),
    path('transport/', transport, name='transport'),

    path('enquiry/', include('enquiryApp.urls')),

    # ✅ FIX APP NAME (IMPORTANT)
    path('admindashboard/', include('adimApp.urls')),
]

# ✅ MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)