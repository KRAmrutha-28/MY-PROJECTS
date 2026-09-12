from django.contrib import admin
from .models import BusRoute, Bus

@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'route_name', 'start_point', 'end_point']
    search_fields = ['route_number', 'route_name']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'route', 'capacity', 'driver_name', 'status']
    list_filter = ['status', 'route']
    search_fields = ['bus_number', 'driver_name']