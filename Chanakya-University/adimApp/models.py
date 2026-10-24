from django.db import models
from django.shortcuts import render, redirect


class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username




class Course(models.Model):
    name = models.CharField(max_length=200)

    description = models.TextField()
    duration = models.CharField(max_length=50)

    fee = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    seats = models.PositiveIntegerField()   # ✅ better than IntegerField

    status = models.CharField(
        max_length=50,
        choices=[
            ('Open', 'Open'),
            ('Closed', 'Closed'),
            ('Coming Soon', 'Coming Soon')
        ],
        default='Open'
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    syllabus = models.TextField(null=True, blank=True)
    certification = models.CharField(max_length=100, null=True, blank=True)

    mode = models.CharField(
        max_length=50,
        choices=[
            ('Online', 'Online'),
            ('Offline', 'Offline'),
            ('Hybrid', 'Hybrid')
        ]
    )

    location = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(upload_to='courses/', null=True, blank=True)  # ✅ important fix

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=15)

    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)

    bio = models.TextField()

    availability = models.CharField(max_length=50, default="Available")
    joining_date = models.DateField(null=True, blank=True)

    location = models.CharField(max_length=200)

    image = models.ImageField(upload_to='faculty/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Hostel(models.Model):
    hostel_name = models.CharField(max_length=200)
    hostel_type = models.CharField(max_length=50)  # Boys / Girls

    room_type = models.CharField(max_length=100)
    total_rooms = models.IntegerField()
    capacity = models.IntegerField()
    available = models.IntegerField()

    fee = models.DecimalField(max_digits=10, decimal_places=2)

    facilities = models.TextField()
    security = models.CharField(max_length=200)
    curfew_time = models.CharField(max_length=50)

    location = models.CharField(max_length=200)

    def __str__(self):
        return self.hostel_name



class Transport(models.Model):
    route_name = models.CharField(max_length=200)
    bus_no = models.CharField(max_length=50)

    seats = models.IntegerField()
    available = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    pickup_time = models.TimeField()
    drop_time = models.TimeField()

    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)

    status = models.CharField(max_length=50)

    image = models.ImageField(upload_to='transport/', null=True, blank=True)

    def __str__(self):
        return self.route_name