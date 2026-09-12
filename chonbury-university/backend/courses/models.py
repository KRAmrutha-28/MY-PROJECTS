from django.db import models

class Campus(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Chanakya University - {self.name}"

class Course(models.Model):
    COURSE_TYPES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    course_type = models.CharField(max_length=2, choices=COURSE_TYPES)
    specialization = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='courses')
    duration = models.IntegerField(help_text="Duration in years")
    description = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Chanakya University - {self.name} - {self.specialization}"

class BTechSpecialization(models.Model):
    SPECIALIZATION_CHOICES = [
        ('CS', 'Computer Science'),
        ('EC', 'Electronics & Communication'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
    ]
    
    specialization = models.CharField(max_length=2, choices=SPECIALIZATION_CHOICES)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    fee_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Chanakya University - BTech {self.get_specialization_display()}"