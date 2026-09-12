from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'course_interested', 'inquiry_date', 'is_contacted']
    list_filter = ['is_contacted', 'inquiry_date']
    search_fields = ['student_name', 'email', 'phone']