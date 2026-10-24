from django.contrib import admin

# Register your models here.
from .models import AdminUser, Course, Faculty, Hostel, Transport

admin.site.register(AdminUser)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(Hostel)
admin.site.register(Transport)