from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('mentor', 'Mentor'),
        ('ngo_admin', 'NGO Admin'),
        ('gov_admin', 'Gov Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    firebase_uid = models.CharField(max_length=128, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.username

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class SosAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    triggered_at = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lng = models.FloatField()
    status = models.CharField(max_length=20, default='active') # active, resolved
    resolved_at = models.DateTimeField(null=True, blank=True)
    admin_message = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=50, blank=True, null=True)

class SafeRouteReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    safety_rating = models.IntegerField() # e.g. 1-5
    time_of_day = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class VerifiedPartner(models.Model):
    TYPE_CHOICES = (
        ('ngo', 'NGO'),
        ('police', 'Police'),
        ('legal', 'Legal'),
        ('health', 'Health'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    region = models.CharField(max_length=100)
    verification_status = models.CharField(max_length=50, default='pending')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_partners')

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    industry = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    focus_area = models.CharField(max_length=255)
    availability = models.CharField(max_length=255)
    verification_status = models.CharField(max_length=50, default='pending')

class MentorshipRequest(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_requests')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_requests')
    status = models.CharField(max_length=50, default='pending')
    scheduled_at = models.DateTimeField(null=True, blank=True)

class CareerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.TextField()
    skills = models.TextField()
    interests = models.TextField()
    goals = models.TextField()

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    remote = models.BooleanField(default=False)
    source = models.CharField(max_length=255)
    posted_at = models.DateTimeField(auto_now_add=True)

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    field = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    deadline = models.DateField()

class LegalHealthResource(models.Model):
    CATEGORY_CHOICES = (
        ('legal', 'Legal'),
        ('health', 'Health'),
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=100)
    content = models.TextField()
    source_url = models.URLField(blank=True, null=True)

class ResumeUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloudinary_url = models.URLField()
    ai_feedback_json = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ServiceRating(models.Model):
    service_name = models.CharField(max_length=100, default='Police Response')
    rating = models.IntegerField() # 1 to 5
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name} - {self.rating} Stars"
