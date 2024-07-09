from django.shortcuts import render
from rest_framework import generics
from .models import HostelProfile,StudentProfile,LeaveRecord,HostelStudent
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.exceptions import TokenError
from .serializer import HostelEmailTokenObtainPairSerializer, HostelRegisterSerializer,StudentEmailTokenObtainPairSerializer,LeaveRecordSerializer
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .backends import StudentBackend
import random
import string

class HostelEmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = HostelEmailTokenObtainPairSerializer

class StudentEmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = StudentEmailTokenObtainPairSerializer


class RegisterHostelView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self,request):
        
        serializer = HostelRegisterSerializer(data=request.data)
        if serializer.is_valid():
            hostel = serializer.save()
            self.send_confirmation_email(hostel)
            return Response({'message': 'Hostel details saved and confirmation email sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_confirmation_email(self,hostel):
        
        try:
            email_subject = 'Hostel Registration on Our Platform Confirmed'
            email_body = 'Thank you for registering your hostel on our platform.\n\n'
            email_body += 'Your hostel has been successfully registered. Here are the details you provided:\n'
            email_body += f'Hostel Name: {hostel.name}\n'
            email_body += f'Contact Person: {hostel.contact_person_name}\n'
            email_body += f'Contact Email: {hostel.email}\n'
            email_body += f'Phone Number: {hostel.contact}\n\n'
            email_body += 'Please keep this information for your records. If you need to update any details or have any questions, feel free to contact our support team.\n\n'
            email_body += 'We look forward to a successful partnership.\n\n'
            email_body += 'Best regards,\n'
            email_body += 'The Platform Support Team'
            
            
            # Send email
            send_mail(
                email_subject,
                email_body,
                'noreply@gmail.com',
                [hostel.email],
                fail_silently=False
            )
            
            return Response({'message': 'mail sent'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            
            print("Error:", e)
        
        
        
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class Home(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class HostelLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email and password:
            hostel = authenticate(request, email=email, password=password)
            if hostel is not None and isinstance(hostel, HostelProfile):
                refresh = RefreshToken()
                refresh['user_id'] = hostel.id
                refresh['user_type'] = 'hostel'
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)


class HostelLogoutView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        
        refresh_token = request.data.get('refresh')
        print("Received refresh token:", refresh_token)
        
        try:
            token = RefreshToken(refresh_token)
            print("Validated token:", token)
            token.blacklist()
            return Response({'message':'logout'},status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            print("TokenError:", e)
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception:", e)
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterStudentWithHostelView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        
        data = request.data
        email = data.get('email')
        name = data.get('name')
        room_no = data.get('room_no')
        contact = data.get('contact')
        home_address = data.get('home_address')
        parents_name = data.get('parents_name')
        parents_contact = data.get('parents_contact')
        year = data.get('year')
        course = data.get('course')
        tenure = data.get('tenure')
        guardian_name = data.get('guardian_name')
        guardian_address = data.get('guardian_address')
        guardian_contact = data.get('guardian_contact')
        
        
        hostel = get_object_or_404(HostelProfile, email=request.user.email)

        print(hostel)
        def generate_password(name):
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            password = f"{name[:3].capitalize()}{random_string}"
            return password
        
        
        
        if StudentProfile.objects.filter(email=email).exists():
            return Response({'message':'student with the hostel already exist'},status=status.HTTP_400_BAD_REQUEST)
        else:
            password = generate_password(name)
            student = StudentProfile.objects.create(
                email=email,
                name=name,
                room_no=room_no,
                contact=contact,
                home_address=home_address,
                parents_name=parents_name,
                parents_contact=parents_contact,
                year=year,
                course=course,
                tenure=tenure,
                guardian_name=guardian_name,
                guardian_address=guardian_address,
                guardian_contact=guardian_contact,
                password=make_password(password)
            )
            student_hostel = HostelStudent.objects.create(student=student,hostel=hostel)
            self.send_email_of_credentials(student,hostel,password)
            return Response({'message': 'Student details saved and email sent'}, status=status.HTTP_201_CREATED)
    
    def send_email_of_credentials(self,student,hostel,password):
        
        try:
            email_subject = 'Student Registration on Our Platform Confirmed'
            email_body = f'Hello {student.name},\n\n'
            email_body += f'We are pleased to inform you that your {hostel.name} has registered you on our platform.\n\n'
            email_body += 'Your login details are as follows:\n'
            email_body += f'Email: {student.email}\n'
            email_body += f'Password: {password}\n\n'
            email_body += 'Please use these credentials to log in.\n\n'
            email_body += 'Best regards,\n'
            email_body += 'The Platform Support Team'
            
            # Send email
            send_mail(
                email_subject,
                email_body,
                'noreply@gmail.com',
                [student.email],
                fail_silently=False
            )
            
            return Response({'message': 'mail sent'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            
            print("Error:", e)


class StudentLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            student = StudentBackend.authenticate(self,request, username=email, password=password, backend='registration.backends.StudentBackend')
            # hostel = authenticate(request, username=email, password=password, backend='registration.backends.HostelBackend')

            if student is not None:
                user = student
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user)
            refresh['user_content_type'] = ContentType.objects.get_for_model(user).model
            refresh['user_object_id'] = user.id
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)


class ViewLeaves(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        try:
            hostel_profile = HostelProfile.objects.get(email=request.user)
        except HostelProfile.DoesNotExist:
            return Response({'detail': 'Hostel profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        leaverecords = LeaveRecord.objects.filter(hostel=hostel_profile)
        serializer = LeaveRecordSerializer(leaverecords, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
