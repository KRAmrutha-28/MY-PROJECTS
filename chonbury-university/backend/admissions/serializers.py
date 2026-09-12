from rest_framework import serializers
from .models import Admission
from courses.serializers import CourseSerializer

class AdmissionSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = Admission
        fields = '__all__'