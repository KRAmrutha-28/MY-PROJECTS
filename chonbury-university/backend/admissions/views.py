from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Admission
from .serializers import AdmissionSerializer

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

@api_view(['GET'])
def get_admission_status(request):
    admissions = Admission.objects.all()
    serializer = AdmissionSerializer(admissions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_open_admissions(request):
    admissions = Admission.objects.filter(status='OPEN')
    serializer = AdmissionSerializer(admissions, many=True)
    return Response(serializer.data)