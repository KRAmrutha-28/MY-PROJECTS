from django.contrib import admin
from .models import Admission

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['course', 'status', 'last_date', 'application_fee']
    list_filter = ['status']
    search_fields = ['course__name']