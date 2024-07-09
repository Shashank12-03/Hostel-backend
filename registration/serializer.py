from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from .models import HostelProfile,StudentProfile,LeaveRecord
from rest_framework_simplejwt.tokens import RefreshToken
from .backends import HostelBackend,StudentBackend
import logging

class HostelEmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        email = attrs.get('email')
        print(email)
        password = attrs.get('password')
        print(password)
        if email and password:
            # Try to authenticate using CustomUserModel
            self.user = HostelBackend.authenticate(self,request=self.context.get('request'), username=email, password=password)
            print(self.user)
            if not self.user:
                print('customuser block')
                raise serializers.ValidationError(
                    _('No active account found with the given credentials'),
                    code='authentication',
                )

            if isinstance(self.user, HostelProfile):
                # Handle hostel-specific logic
                print('hostel profile check')
                refresh = RefreshToken.for_user(self.user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            else:
                # Handle unexpected user types (if any)
                print('last block')
                raise serializers.ValidationError(
                    
                    _('No active account found with the given credentials'),
                    code='authentication',
                )

        else:
            raise serializers.ValidationError(
                _('Must include "email" and "password"'),
                code='authorization',
            )

class StudentEmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        email = attrs.get('email')
        print(email)
        password = attrs.get('password')
        print(password)
        if email and password:
            # Try to authenticate using CustomUserModel
            self.user = StudentBackend.authenticate(self,request=self.context.get('request'), username=email, password=password)
            print(self.user)
            if not self.user:
                print('customuser block')
                raise serializers.ValidationError(
                    _('No active account found with the given credentials'),
                    code='authentication',
                )

            if isinstance(self.user, StudentProfile):
                # Handle hostel-specific logic
                print('student profile check')
                refresh = RefreshToken.for_user(self.user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            else:
                # Handle unexpected user types (if any)
                print('last block')
                raise serializers.ValidationError(
                    
                    _('No active account found with the given credentials'),
                    code='authentication',
                )

        else:
            raise serializers.ValidationError(
                _('Must include "email" and "password"'),
                code='authorization',
            )

class HostelRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HostelProfile
        fields = ['email','password','name','address','contact','contact_person_name']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        hostel = HostelProfile.objects.create_user(email=email,password=password,**validated_data)
        return hostel
    
class LeaveRecordSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        slug_field="name", queryset=StudentProfile.objects.all()
    )
    
    
    class Meta:
        model = LeaveRecord
        fields =[
            'student',
            'leave_reason',
            'leave_start_date',
            'leave_end_date',
            'location',
            'date_applied'
        ]