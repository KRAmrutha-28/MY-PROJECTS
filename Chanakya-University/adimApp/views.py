from django.shortcuts import render, redirect

from .models import AdminUser, Course, Faculty, Hostel, Transport  


# 🔐 ADMIN LOGIN
def admin_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = AdminUser.objects.get(username=username, password=password)

            request.session['admin_id'] = admin.id

            return redirect('dashboard')

        except AdminUser.DoesNotExist:
            return render(request, 'admin-login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'admin-login.html')


# ================= DASHBOARD =================
def dashboard(request):

    if not request.session.get('admin_id'):
        return redirect('admin_login')

    courses = Course.objects.all()
    faculty = Faculty.objects.all()
    hostel = Hostel.objects.all()
    transport = Transport.objects.all()

    return render(request, 'adminDashboard.html', {
        'courses': courses,
        'faculty': faculty,
        'hostel': hostel,
        'transport': transport
    })

# ================= COURSE =================
def add_course(request):
    if request.method == "POST":
        Course.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            duration=request.POST.get('duration'),
            fee=request.POST.get('fee'),
            category=request.POST.get('category'),
            level=request.POST.get('level'),
            seats=request.POST.get('seats'),
            status=request.POST.get('status'),
            mode=request.POST.get('mode'),
            location=request.POST.get('location'),
            image=request.FILES.get('image')
        )
        return redirect('dashboard')

    return render(request, 'add-course.html')


def delete_course(request, id):
    Course.objects.filter(id=id).delete()
    return redirect('dashboard')



def update_course(request, id):
    course = Course.objects.get(id=id)

    if request.method == "POST":
        course.name = request.POST.get('name')
        course.description = request.POST.get('description')
        course.duration = request.POST.get('duration')
        course.fee = request.POST.get('fee')
        course.category = request.POST.get('category')
        course.level = request.POST.get('level')
        course.seats = request.POST.get('seats')
        course.status = request.POST.get('status')
        course.mode = request.POST.get('mode')
        course.location = request.POST.get('location')

        if request.FILES.get('image'):
            course.image = request.FILES.get('image')

        course.save()
        return redirect('dashboard')

    return render(request, 'update-course.html', {'c': course})



# ================= FACULTY =================
def add_faculty(request):
    if request.method == "POST":
        Faculty.objects.create(
            name=request.POST.get('name'),
            designation=request.POST.get('designation'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            qualification=request.POST.get('qualification'),
            experience=request.POST.get('experience'),
            specialization=request.POST.get('specialization'),
            bio=request.POST.get('bio'),
            availability=request.POST.get('availability'),
            joining_date=request.POST.get('joining_date'),
            location=request.POST.get('location'),
            image=request.FILES.get('image')
        )
        return redirect('dashboard')

    return render(request, 'add-faculty.html')


def delete_faculty(request, id):
    Faculty.objects.filter(id=id).delete()
    return redirect('dashboard')


def update_faculty(request, id):
    faculty = Faculty.objects.get(id=id)

    if request.method == "POST":
        faculty.name = request.POST.get('name')
        faculty.designation = request.POST.get('designation')
        faculty.email = request.POST.get('email')
        faculty.phone = request.POST.get('phone')
        faculty.qualification = request.POST.get('qualification')
        faculty.experience = request.POST.get('experience')
        faculty.specialization = request.POST.get('specialization')
        faculty.bio = request.POST.get('bio')
        faculty.availability = request.POST.get('availability')
        faculty.location = request.POST.get('location')

        if request.POST.get('joining_date'):
            faculty.joining_date = request.POST.get('joining_date')

        if request.FILES.get('image'):
            faculty.image = request.FILES.get('image')

        faculty.save()
        return redirect('dashboard')

    return render(request, 'update-faculty.html', {'f': faculty})



# ================= HOSTEL (TEMP) =================
# ================= ADD HOSTEL =================
def add_hostel(request):
    if request.method == "POST":
        Hostel.objects.create(
            hostel_name=request.POST.get('hostel_name'),
            hostel_type=request.POST.get('hostel_type'),
            room_type=request.POST.get('room_type'),
            total_rooms=request.POST.get('total_rooms'),
            capacity=request.POST.get('capacity'),
            available=request.POST.get('available'),
            fee=request.POST.get('fee'),
            facilities=request.POST.get('facilities'),
            security=request.POST.get('security'),
            curfew_time=request.POST.get('curfew_time'),
            location=request.POST.get('location'),
        )
        return redirect('dashboard')

    return render(request, 'add-hostel.html')

# ================= DELETE HOSTEL =================
def delete_hostel(request, id):
    Hostel.objects.filter(id=id).delete()
    return redirect('dashboard')


def update_hostel(request, id):
    hostel = Hostel.objects.get(id=id)

    if request.method == "POST":
        hostel.hostel_name = request.POST.get('hostel_name')
        hostel.hostel_type = request.POST.get('hostel_type')
        hostel.room_type = request.POST.get('room_type')
        hostel.total_rooms = request.POST.get('total_rooms')
        hostel.capacity = request.POST.get('capacity')
        hostel.available = request.POST.get('available')
        hostel.fee = request.POST.get('fee')
        hostel.facilities = request.POST.get('facilities')
        hostel.security = request.POST.get('security')
        hostel.curfew_time = request.POST.get('curfew_time')
        hostel.location = request.POST.get('location')

        hostel.save()
        return redirect('dashboard')

    return render(request, 'update-hostel.html', {'h': hostel})





# ================= TRANSPORT =================
def add_transport(request):
    if request.method == "POST":
        Transport.objects.create(
            route_name=request.POST.get('route_name'),
            bus_no=request.POST.get('bus_no'),
            seats=request.POST.get('seats'),
            available=request.POST.get('available'),
            fee=request.POST.get('fee'),
            pickup_time=request.POST.get('pickup_time'),
            drop_time=request.POST.get('drop_time'),
            driver_name=request.POST.get('driver_name'),
            driver_phone=request.POST.get('driver_phone'),
            status=request.POST.get('status'),
            image=request.FILES.get('image')
        )
        return redirect('dashboard')

    return render(request, 'add-transport.html')


def delete_transport(request, id):
    Transport.objects.filter(id=id).delete()
    return redirect('dashboard')



def update_transport(request, id):
    transport = Transport.objects.get(id=id)

    if request.method == "POST":
        transport.route_name = request.POST.get('route_name')
        transport.bus_no = request.POST.get('bus_no')
        transport.seats = request.POST.get('seats')
        transport.available = request.POST.get('available')
        transport.fee = request.POST.get('fee')
        transport.pickup_time = request.POST.get('pickup_time')
        transport.drop_time = request.POST.get('drop_time')
        transport.driver_name = request.POST.get('driver_name')
        transport.driver_phone = request.POST.get('driver_phone')
        transport.status = request.POST.get('status')

        if request.FILES.get('image'):
            transport.image = request.FILES.get('image')

        transport.save()
        return redirect('dashboard')

    return render(request, 'update-transport.html', {'t': transport})






def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')