from django.db import models
from courses.models import Course

class Inquiry(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course_interested = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    inquiry_date = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    contacted_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Inquiry from {self.student_name} for {self.course_interested.name}"