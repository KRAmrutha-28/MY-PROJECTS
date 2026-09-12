from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'inquiries', views.InquiryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.create_inquiry),
    path('course/<int:course_id>/', views.get_inquiries_by_course),
]