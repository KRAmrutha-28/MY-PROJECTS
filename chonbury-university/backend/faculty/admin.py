from django.contrib import admin
from .models import Faculty, Room

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_hod', 'email', 'experience_years']
    list_filter = ['designation', 'is_hod']
    search_fields = ['name', 'email', 'specialization']
    filter_horizontal = ['courses']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'capacity', 'course']
    list_filter = ['room_type', 'is_ac_available']
    search_fields = ['room_number']