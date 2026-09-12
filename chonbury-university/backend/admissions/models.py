from django.db import models
from courses.models import Course

class Admission(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('COMING_SOON', 'Coming Soon'),
    ]
    
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    last_date = models.DateField()
    eligibility_criteria = models.TextField()
    application_fee = models.DecimalField(max_digits=8, decimal_places=2)
    required_documents = models.TextField(help_text="List of required documents")
    admission_process = models.TextField()
    
    def __str__(self):
        return f"{self.course.name} - {self.status}"