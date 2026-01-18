from rest_framework import serializers
from core.models import *
from rest_framework.validators import UniqueValidator

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Resume
        fields = '__all__'
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
    
class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=Employee.objects.all(), 
            message="This email is already used."
        )]
    )
    class Meta:
        model = Employee
        fields = '__all__'