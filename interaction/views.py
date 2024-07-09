from django.shortcuts import render
from .models import Complaints
from rest_framework.views import APIView
from .serializer import RegisterComplaintSerializer, StudentLeaveSerializer,ComplaintsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from registration.models import StudentProfile
from rest_framework.response import Response 
from registration.models import HostelProfile
from rest_framework import status
# Create your views here.


class RegisterComplaintView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    
    def post(self, request):
        print(f"User type: {type(request.user)}")
        print(f"User email: {request.user.email}")
        
        try:
            student_profile = StudentProfile.objects.get(email=request.user)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        hostel = student_profile.get_hostel()
        
        if hostel:
            print(f"Student {student_profile.email} is associated with Hostel {hostel.name}")
        else:
            print(f"Student {student_profile.email} is not associated with any hostel")
        
        serializer = RegisterComplaintSerializer(data=request.data)
        
        if serializer.is_valid():
            complaint = serializer.save(complainant=student_profile,hostel = hostel)
            return Response({'message': 'Complaint registered'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class TakeLeaveView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        try:
            student_profile = StudentProfile.objects.get(email=request.user)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not isinstance(student_profile, StudentProfile):
            return Response({'detail': 'Permission denied. Only students can apply for leave.'}, status=status.HTTP_403_FORBIDDEN)
        
        hostel = student_profile.get_hostel()
        if not hostel:
            return Response({'detail': 'Student is not associated with any hostel.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentLeaveSerializer(data=request.data)
        if serializer.is_valid():
            leaverecord = serializer.save(student=student_profile, hostel=hostel)
            return Response({'message': 'Leave applied successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ViewComplaints(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            hostel_profile = HostelProfile.objects.get(email=request.user)
        except HostelProfile.DoesNotExist:
            return Response({'detail': 'Hostel profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        complaints = Complaints.objects.filter(hostel=hostel_profile)
        serializer = ComplaintsSerializer(complaints, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)