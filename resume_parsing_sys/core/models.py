from django.db import models

# Create your models here.
class Resume(models.Model):
    file = models.FileField(upload_to= 'resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class Candidate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=225)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=225, blank=True)
    experience = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):
    SOURCE_CHOICES = (
        ('resume_upload', 'Resume Upload'),
        ('manual_entry', 'Manual Entry'),
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True)
    work_experience = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
