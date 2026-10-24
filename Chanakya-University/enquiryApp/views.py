from django.shortcuts import render, redirect
from .models import Enquiry, HR


# ================= SAVE ENQUIRY =================
def save_enquiry(request):
    if request.method == "POST":
        try:
            Enquiry.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                course=request.POST.get('course'),
                message=request.POST.get('message'),
            )
            return redirect('/?success=1')  # ✅ success popup

        except Exception as e:
            print(e)
            return redirect('/?error=1')   # ❌ error popup

    return redirect('/')


# ================= HR LOGIN =================
def hr_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            hr = HR.objects.get(username=username, password=password)

            # store session
            request.session['hr_id'] = hr.id

            # ✅ FIXED REDIRECT
            return redirect('enquiryApp:dashboard')

        except HR.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')


# ================= ENQUIRY DASHBOARD =================
def dashboard(request):

    # 🔐 check login
    if not request.session.get('hr_id'):
        return redirect('enquiryApp:login')

    enquiries = Enquiry.objects.all().order_by('-created_at')

    return render(request, 'enquiry_dashboard.html', {
        'enquiries': enquiries
    })


# ================= LOGOUT =================
def logout(request):
    request.session.flush()
    return redirect('enquiryApp:login')