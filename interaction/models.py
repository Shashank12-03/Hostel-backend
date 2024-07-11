from django.db import models
from registration.models import StudentProfile,HostelProfile
from django.utils import timezone
# Create your models here.
    
    
class ComplaintType(models.Model):
    type = models.CharField(max_length=20,default=None)
    
class Complaints(models.Model):
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE, default= None)
    complaint_type = models.ForeignKey(ComplaintType,on_delete=models.CASCADE)
    complainant = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    description = models.TextField(default=None)
    date = models.DateField(default=timezone.now)
    
class Notices(models.Model):
    hostel = models.ForeignKey(HostelProfile,on_delete=models.CASCADE, default=None)
    description = models.TextField(default= None)
    date = models.DateField(default=timezone.now)
    