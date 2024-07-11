from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The User must have a valid email address')
        extra_fields.setdefault('is_active', True)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUserModel(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class HostelProfile(CustomUserModel):
    name = models.CharField(max_length=200)
    contact_person_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=10, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Hostel Profile'
        verbose_name_plural = 'Hostel Profiles'

class StudentProfile(CustomUserModel):
    name = models.CharField(max_length=100)
    room_no = models.CharField(max_length=2)
    contact = models.CharField(max_length=10)
    home_address = models.CharField(max_length=200)
    parents_name = models.CharField(max_length=100)
    parents_contact = models.CharField(max_length=10)
    year = models.CharField(max_length=5)
    course = models.CharField(max_length=50)
    tenure = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=100)
    guardian_address = models.CharField(max_length=200)
    guardian_contact = models.CharField(max_length=10)

    def get_hostel(self):
        try:
            return HostelStudent.objects.get(student=self).hostel
        except HostelStudent.DoesNotExist:
            return None

class HostelStudent(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE)
    

class LeaveRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE)
    leave_reason = models.TextField()
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    location = models.CharField()
    date_applied = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.name} - {self.leave_start_date} to {self.leave_end_date}"
    

    
class OutstandingToken(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='custom_outstanding_tokens',default= None)
    
    