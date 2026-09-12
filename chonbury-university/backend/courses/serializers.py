from rest_framework import serializers
from .models import Campus, Course, BTechSpecialization

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

class BTechSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BTechSpecialization
        fields = '__all__'