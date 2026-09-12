from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Faculty, Room
from .serializers import FacultySerializer, RoomSerializer
from courses.models import Course

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

@api_view(['GET'])
def get_faculty_by_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        faculties = course.faculties.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)

@api_view(['GET'])
def get_hod_by_department(request, department):
    faculties = Faculty.objects.filter(is_hod=True, specialization__icontains=department)
    serializer = FacultySerializer(faculties, many=True)
    return Response(serializer.data)