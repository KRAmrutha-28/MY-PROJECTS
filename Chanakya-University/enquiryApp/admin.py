from django.contrib import admin

# Register your models here.
from .models import HR, Enquiry

admin.site.register(Enquiry)
admin.site.register(HR)