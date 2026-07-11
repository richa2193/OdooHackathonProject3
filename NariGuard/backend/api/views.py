from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LYtRlqFLA2DTqKfYGD0hlO2QwOJo3WeCJ6_THI9QXJoQ"))

from core.models import (
    User, EmergencyContact, SosAlert, SafeRouteReport,
    VerifiedPartner, Mentor, MentorshipRequest,
    CareerProfile, Job, Scholarship, LegalHealthResource, ResumeUpload, ServiceRating
)
from .serializers import (
    UserSerializer, EmergencyContactSerializer, SosAlertSerializer, SafeRouteReportSerializer,
    VerifiedPartnerSerializer, MentorSerializer, MentorshipRequestSerializer,
    CareerProfileSerializer, JobSerializer, ScholarshipSerializer, LegalHealthResourceSerializer, ResumeUploadSerializer, ServiceRatingSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class EmergencyContactViewSet(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SosAlertViewSet(viewsets.ModelViewSet):
    queryset = SosAlert.objects.all()
    serializer_class = SosAlertSerializer
    permission_classes = [AllowAny] # Allow anonymous triggering for emergency

class SafeRouteReportViewSet(viewsets.ModelViewSet):
    queryset = SafeRouteReport.objects.all()
    serializer_class = SafeRouteReportSerializer
    permission_classes = [AllowAny]

class VerifiedPartnerViewSet(viewsets.ModelViewSet):
    queryset = VerifiedPartner.objects.all()
    serializer_class = VerifiedPartnerSerializer
    permission_classes = [AllowAny]

class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [AllowAny]

class MentorshipRequestViewSet(viewsets.ModelViewSet):
    queryset = MentorshipRequest.objects.all()
    serializer_class = MentorshipRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CareerProfileViewSet(viewsets.ModelViewSet):
    queryset = CareerProfile.objects.all()
    serializer_class = CareerProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [AllowAny]

class LegalHealthResourceViewSet(viewsets.ModelViewSet):
    queryset = LegalHealthResource.objects.all()
    serializer_class = LegalHealthResourceSerializer
    permission_classes = [AllowAny]

class ResumeUploadViewSet(viewsets.ModelViewSet):
    queryset = ResumeUpload.objects.all()
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ServiceRatingViewSet(viewsets.ModelViewSet):
    queryset = ServiceRating.objects.all()
    serializer_class = ServiceRatingSerializer
    permission_classes = [AllowAny]

class AIChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        query = request.data.get('query', '')
        if not query:
            return Response({'error': 'Query is required'}, status=400)
            
        try:
            model = genai.GenerativeModel('gemini-3.5-flash')
            prompt = query + " (Please provide a concise, structured response suitable for a women's empowerment platform providing career guidance, safety tips, or legal/health education.)"
            response = model.generate_content(prompt)
            return Response({'response': response.text})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

