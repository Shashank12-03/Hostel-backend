from rest_framework import serializers
from .models import Complaints,ComplaintType
from registration.models import LeaveRecord,StudentProfile
class RegisterComplaintSerializer(serializers.ModelSerializer):
    complaint_type = serializers.SlugRelatedField(slug_field="type",queryset = ComplaintType.objects.all())
    
    class Meta:
        model = Complaints
        fields = [
            'complaint_type',
            'description',
            'date'
        ]
        
    
class StudentLeaveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LeaveRecord
        fields = [
            'leave_reason',
            'leave_start_date',
            'leave_end_date',
            'location',
        ]
        
class ComplaintsSerializer(serializers.ModelSerializer):
    complaint_type = serializers.SlugRelatedField(
        slug_field="type", queryset=ComplaintType.objects.all()
    )
    complainant = serializers.SlugRelatedField(
        slug_field="name", queryset=StudentProfile.objects.all()
    )

    class Meta:
        model = Complaints
        fields = [
            'complaint_type',
            'complainant',
            'description',
            'date'
        ]