from django.contrib import admin
from .models import Document, QueryHistory

admin.site.register(Document)
admin.site.register(QueryHistory)