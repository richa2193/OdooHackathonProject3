from rest_framework import serializers
from core.models import (
    User, EmergencyContact, SosAlert, SafeRouteReport,
    VerifiedPartner, Mentor, MentorshipRequest,
    CareerProfile, Job, Scholarship, LegalHealthResource, ResumeUpload, ServiceRating
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'region', 'firebase_uid']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

class SosAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SosAlert
        fields = '__all__'
        extra_kwargs = {'user': {'required': False, 'allow_null': True}}

class SafeRouteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeRouteReport
        fields = '__all__'

class VerifiedPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedPartner
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'

class MentorshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipRequest
        fields = '__all__'

class CareerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProfile
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'

class LegalHealthResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalHealthResource
        fields = '__all__'

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeUpload
        fields = '__all__'

class ServiceRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRating
        fields = '__all__'
