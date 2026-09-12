from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Campus, Course, BTechSpecialization
from .serializers import CampusSerializer, CourseSerializer, BTechSpecializationSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer

@api_view(['GET'])
def get_btech_courses(request):
    try:
        btech_courses = BTechSpecialization.objects.all()
        serializer = BTechSpecializationSerializer(btech_courses, many=True)
        return Response(serializer.data)
    except:
        return Response({'message': 'No BTech courses found'}, status=200)

@api_view(['GET'])
def get_courses_by_type(request, course_type):
    courses = Course.objects.filter(course_type=course_type)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)