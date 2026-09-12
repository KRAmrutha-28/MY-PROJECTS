from rest_framework import serializers
from .models import Inquiry
from courses.models import Course

class InquirySerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course_interested.name', read_only=True)
    
    class Meta:
        model = Inquiry
        fields = '__all__'