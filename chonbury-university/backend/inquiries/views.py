from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inquiry
from .serializers import InquirySerializer

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

@api_view(['POST'])
def create_inquiry(request):
    serializer = InquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Thank you for your inquiry! We will contact you soon.',
            'data': serializer.data
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_inquiries_by_course(request, course_id):
    inquiries = Inquiry.objects.filter(course_interested_id=course_id)
    serializer = InquirySerializer(inquiries, many=True)
    return Response(serializer.data)