from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'routes', views.BusRouteViewSet)
router.register(r'buses', views.BusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('details/', views.get_transport_details),
    path('route/<str:route_number>/', views.get_buses_by_route),
]