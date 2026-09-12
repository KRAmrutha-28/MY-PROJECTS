from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'campuses', views.CampusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('btech-courses/', views.get_btech_courses),
    path('type/<str:course_type>/', views.get_courses_by_type),
]