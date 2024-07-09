from .models import HostelProfile, StudentProfile
from django.contrib.auth.backends import BaseBackend

class HostelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            hostel = HostelProfile.objects.get(email=username)
            if hostel.check_password(password):
                return hostel
        except HostelProfile.DoesNotExist:
            return None

    def get_user(self, hostel_id):
        try:
            return HostelProfile.objects.get(pk=hostel_id)
        except HostelProfile.DoesNotExist:
            return None

class StudentBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = StudentProfile.objects.get(email=username)
            if student.check_password(password):
                return student
        except StudentProfile.DoesNotExist:
            return None

    def get_user(self, student_id):
        try:
            return StudentProfile.objects.get(pk=student_id)
        except StudentProfile.DoesNotExist:
            return None