from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'admissions', views.AdmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('status/', views.get_admission_status),
    path('open/', views.get_open_admissions),
]