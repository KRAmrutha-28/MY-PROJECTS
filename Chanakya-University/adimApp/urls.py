from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('', views.dashboard, name='dashboard'),

    # COURSE
    path('course/add/', views.add_course, name='add_course'),

    # FACULTY (temporary page)
    path('faculty/add/', views.add_faculty, name='add_faculty'),

    # HOSTEL
    path('hostel/add/', views.add_hostel, name='add_hostel'),

    # TRANSPORT
    path('transport/add/', views.add_transport, name='add_transport'),

    path('course/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('faculty/delete/<int:id>/', views.delete_faculty, name='delete_faculty'),
    path('hostel/delete/<int:id>/', views.delete_hostel, name='delete_hostel'),
    path('transport/delete/<int:id>/', views.delete_transport, name='delete_transport'),

    path('course/update/<int:id>/', views.update_course, name='update_course'),
    path('faculty/update/<int:id>/', views.update_faculty, name='update_faculty'),
    path('hostel/update/<int:id>/', views.update_hostel, name='update_hostel'),
    path('transport/update/<int:id>/', views.update_transport, name='update_transport'),
]