from rest_framework import serializers
from .models import Faculty, Room
from courses.models import Course

class FacultySerializer(serializers.ModelSerializer):
    course_names = serializers.StringRelatedField(source='courses', many=True, read_only=True)
    
    class Meta:
        model = Faculty
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'