from django.urls import path
from . import views

app_name = 'enquiryApp' 

urlpatterns = [
    path('submit/', views.save_enquiry, name='save_enquiry'),
    path('login/', views.hr_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]