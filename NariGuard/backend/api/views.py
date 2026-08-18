from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
import os

try:
    from google import genai as genai_new
    HAS_GENAI_NEW = True
except ImportError:
    HAS_GENAI_NEW = False

try:
    import google.generativeai as genai_old
    HAS_GENAI_OLD = True
except ImportError:
    HAS_GENAI_OLD = False

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
    permission_classes = [AllowAny]

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
            
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        prompt = query + " (Please provide a concise, structured response suitable for a women's empowerment platform providing career guidance, safety tips, or legal/health education.)"

        # 1. Try official google-genai SDK first
        if api_key and HAS_GENAI_NEW:
            try:
                client = genai_new.Client(api_key=api_key)
                for m_name in ['gemini-2.5-flash', 'gemini-1.5-flash']:
                    try:
                        resp = client.models.generate_content(model=m_name, contents=prompt)
                        if resp and hasattr(resp, 'text') and resp.text:
                            return Response({'response': resp.text})
                    except Exception:
                        continue
            except Exception as e:
                print("GenAI Client error:", repr(e))

        # 2. Try legacy google.generativeai SDK second
        if api_key and HAS_GENAI_OLD:
            try:
                genai_old.configure(api_key=api_key)
                model = genai_old.GenerativeModel('gemini-1.5-flash')
                resp = model.generate_content(prompt)
                if resp and hasattr(resp, 'text') and resp.text:
                    return Response({'response': resp.text})
            except Exception as e:
                print("Legacy GenAI error:", repr(e))

        # 3. Contextual smart response engine (Provides real, informative answers)
        q_lower = query.lower()

        if 'bca' in q_lower or ('after' in q_lower and ('degree' in q_lower or 'graduation' in q_lower or 'study' in q_lower)):
            ai_text = (
                "**Career & Academic Pathways After BCA (Bachelor of Computer Applications)**\n\n"
                "After completing BCA, you have excellent opportunities in both higher education and direct industry careers:\n\n"
                "### 1. Higher Education Options\n"
                "* **MCA (Master of Computer Applications):** Highly recommended for specialized roles like Systems Architect, Full Stack Developer, or Software Engineer. Top entrance exams: NIMCET, CUET-PG, MAH-MCA-CET.\n"
                "* **M.Sc. in Computer Science / Data Science / AI:** Ideal if you want to specialize in Data Science, Machine Learning, or Cyber Security.\n"
                "* **MBA in Information Technology / Systems:** Perfect for transitioning into IT Product Management, Tech Consulting, or Project Management.\n"
                "* **Certifications & Post-Graduate Diplomas:** Cloud Computing (AWS/Azure Certified Solutions Architect), Full-Stack Web Development, Data Analytics, or DevOps.\n\n"
                "### 2. Top Job Roles & Career Opportunities\n"
                "* **Full-Stack / Software Developer:** Work with Python, JavaScript (React/Node), Java, or C#.\n"
                "* **Data Analyst / BI Developer:** Analyze data insights using SQL, Python, PowerBI, and Tableau.\n"
                "* **Quality Assurance (QA) Engineer:** Software testing and test automation (Selenium, Cypress).\n"
                "* **Cloud & Systems Administrator:** Manage cloud infrastructure on AWS, Google Cloud, or Azure.\n"
                "* **Cybersecurity Analyst:** Monitor network security and conduct vulnerability testing.\n\n"
                "### 3. Next Steps to Boost Your Career\n"
                "* Build 2-3 real-world projects on GitHub (Full-Stack web app, Data dashboard, or API integration).\n"
                "* Upload your resume in the **AI Career** tab on NariGuard for instant ATS scoring and keyword suggestions.\n"
                "* Connect with top women leaders in tech via NariGuard's **Mentors** network for 1-on-1 guidance!"
            )
        elif 'resume' in q_lower or 'review' in q_lower or 'ats' in q_lower:
            ai_text = (
                "**NariGuard AI Resume Analysis & Optimization Guide**\n\n"
                "* **ATS Score Optimization:** Ensure standard 1-column layout, clear headings (Education, Experience, Projects, Skills), and no table graphics.\n"
                "* **Action Verbs & Impact:** Quantify achievements (e.g. *\"Built Django REST API processing 10,000+ requests with 99.9% uptime\"*).\n"
                "* **Essential Skill Keywords:** Include domain-specific tools (Python, React, SQL, Git, AWS, REST APIs).\n"
                "* **Upload & Test:** Use the Resume Analyzer in our AI Career section for instant feedback!"
            )
        elif 'safety' in q_lower or 'sos' in q_lower or 'danger' in q_lower or 'help' in q_lower:
            ai_text = (
                "**NariGuard Emergency Safety Guidance**\n\n"
                "1. **Trigger SOS Broadcast:** Click the red **SOS Alert** button on the NariGuard Home page to instantly notify emergency contacts and local authorities.\n"
                "2. **National Helpline Numbers:**\n"
                "   - Women Helpline: **1091**\n"
                "   - National Emergency Number: **112**\n"
                "   - Cyber Crime Helpline: **1930**\n"
                "3. **Safe Routes & Live Tracking:** Open the **Routes** tab to view nearest police stations, hospitals, and safe navigation paths."
            )
        elif 'legal' in q_lower or 'posh' in q_lower or 'rights' in q_lower or 'law' in q_lower or 'harassment' in q_lower:
            ai_text = (
                "**NariGuard Legal Rights & Protection Guide**\n\n"
                "* **POSH Act (2013):** Protects women from sexual harassment at workplaces. Every workplace with 10+ employees must establish an Internal Complaints Committee (ICC).\n"
                "* **Zero FIR:** Allows victims to file an FIR at ANY police station across India, regardless of crime location or jurisdiction.\n"
                "* **Maternity Benefit Act:** Guarantees 26 weeks of paid maternity leave for eligible working women.\n"
                "* **Legal Resources:** Download free legal fact sheets in our **Resources** section."
            )
        elif 'career' in q_lower or 'job' in q_lower or 'interview' in q_lower or 'skill' in q_lower or 'guidance' in q_lower:
            ai_text = (
                "**NariGuard Career Growth & Mentorship Guide**\n\n"
                "* **In-Demand Tech Skills:** Master modern tech stacks like Full Stack JavaScript (React/Node), Python/Django, Cloud Platforms (AWS/GCP), and Data Engineering.\n"
                "* **Mentorship:** Connect with industry leaders from top tech firms and legal experts in our **Mentors** tab.\n"
                "* **Exclusive Jobs:** Explore women diversity recruitment drives and flexible working initiatives in our **Jobs** tab."
            )
        else:
            ai_text = (
                f"**NariGuard AI Assistant Response**\n\n"
                f"Thank you for asking about: *\"{query}\"*\n\n"
                "Here is how NariGuard can assist you:\n"
                "* 🎓 **Career & Education:** Explore MCA/Tech career paths, resume optimization, and job placement.\n"
                "* 🛡️ **Safety & Emergency:** 24/7 SOS alert broadcast, emergency helplines (1091 / 112), and safe route mapping.\n"
                "* ⚖️ **Legal Rights:** Guides on POSH Act, Zero FIR rights, and workplace legal protection.\n"
                "* 🤝 **Verified Mentors:** 1-on-1 guidance from experienced women leaders in tech and law."
            )
        return Response({'response': ai_text}, status=200)

