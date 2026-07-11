from django.contrib import admin
from .models import (
    User, EmergencyContact, SosAlert, SafeRouteReport, 
    VerifiedPartner, Mentor, MentorshipRequest, 
    CareerProfile, Job, Scholarship, LegalHealthResource, ResumeUpload
)

admin.site.register(User)
admin.site.register(EmergencyContact)
admin.site.register(SosAlert)
admin.site.register(SafeRouteReport)
admin.site.register(VerifiedPartner)
admin.site.register(Mentor)
admin.site.register(MentorshipRequest)
admin.site.register(CareerProfile)
admin.site.register(Job)
admin.site.register(Scholarship)
admin.site.register(LegalHealthResource)
admin.site.register(ResumeUpload)
