from django.shortcuts import render
from django.http import JsonResponse

def api_home(request):
    return JsonResponse({
        'message': 'Welcome to Chonbury University API',
        'available_endpoints': {
            'courses': '/api/courses/courses/',
            'btech_courses': '/api/courses/btech-courses/',
            'faculty': '/api/faculty/faculty/',
            'transport_routes': '/api/transport/routes/',
            'transport_details': '/api/transport/details/',
            'admission_status': '/api/admissions/status/',
            'admin_panel': '/admin/'
        }
    })