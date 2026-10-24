from django.shortcuts import render

# ✅ ONLY IMPORT EXISTING MODEL
from adimApp.models import Course, Faculty, Hostel, Transport


# ================= HOME =================
def home(request):
    return render(request, 'index.html', {
        'courses': Course.objects.all()[:3],
        'faculty': Faculty.objects.all()[:3],
        'hostel': Hostel.objects.all()[:2],
        'transport': Transport.objects.all()[:2],
    })


# ================= COURSES =================
def courses(request):
    courses = Course.objects.all()
    return render(request, 'course.html', {'courses': courses})


# ================= FACULTY =================
def faclty(request):
    faculty = Faculty.objects.all()   # ✅ fetch data

    return render(request, 'faculty.html', {
        'faculty': faculty           # ✅ pass to template
    })

# ================= HOSTEL =================
def hostel(request):
    return render(request, 'hostel.html', {
        'hostel': Hostel.objects.all()
    })

# ================= TRANSPORT =================
def transport(request):
    return render(request, 'transport.html', {
        'transport': Transport.objects.all()
    })  # temporary static page