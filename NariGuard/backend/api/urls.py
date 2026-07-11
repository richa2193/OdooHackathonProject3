from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, EmergencyContactViewSet, SosAlertViewSet, SafeRouteReportViewSet,
    VerifiedPartnerViewSet, MentorViewSet, MentorshipRequestViewSet,
    CareerProfileViewSet, JobViewSet, ScholarshipViewSet, LegalHealthResourceViewSet, ResumeUploadViewSet,
    ServiceRatingViewSet, AIChatbotView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'emergency-contacts', EmergencyContactViewSet)
router.register(r'sos-alerts', SosAlertViewSet)
router.register(r'safe-routes', SafeRouteReportViewSet)
router.register(r'verified-partners', VerifiedPartnerViewSet)
router.register(r'mentors', MentorViewSet)
router.register(r'mentorship-requests', MentorshipRequestViewSet)
router.register(r'career-profiles', CareerProfileViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'scholarships', ScholarshipViewSet)
router.register(r'resources', LegalHealthResourceViewSet)
router.register(r'resumes', ResumeUploadViewSet)
router.register(r'ratings', ServiceRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/', AIChatbotView.as_view(), name='ai_chatbot'),
]
