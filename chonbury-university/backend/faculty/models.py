from django.db import models
from courses.models import Course

class Faculty(models.Model):
    DESIGNATIONS = [
        ('PROF', 'Professor'),
        ('APROF', 'Associate Professor'),
        ('ASPROF', 'Assistant Professor'),
        ('LECT', 'Lecturer'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    # Fix: Change max_length from 5 to 10 (or higher)
    designation = models.CharField(max_length=10, choices=DESIGNATIONS)  # Changed from 5 to 10
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    is_hod = models.BooleanField(default=False)
    courses = models.ManyToManyField(Course, related_name='faculties')
    joining_date = models.DateField()
    image = models.ImageField(upload_to='faculty/', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"

class Room(models.Model):
    ROOM_TYPES = [
        ('LECTURE', 'Lecture Hall'),
        ('LAB', 'Laboratory'),
        ('SEMINAR', 'Seminar Hall'),
        ('WORKSHOP', 'Workshop Room'),
        ('AUDI', 'Auditorium'),
    ]
    
    room_number = models.CharField(max_length=20)
    # Fix: Change max_length from 10 to 20 to accommodate longer values
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)  # Changed from 10 to 20
    capacity = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='rooms')
    facilities = models.TextField()
    is_ac_available = models.BooleanField(default=False)
    has_projector = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.room_number} - {self.get_room_type_display()}"