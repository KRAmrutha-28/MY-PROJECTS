from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'faculty', views.FacultyViewSet)
router.register(r'rooms', views.RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('by-course/<int:course_id>/', views.get_faculty_by_course),
    path('hod/<str:department>/', views.get_hod_by_department),
]