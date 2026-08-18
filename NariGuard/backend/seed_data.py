import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import (
    User, EmergencyContact, SosAlert, SafeRouteReport,
    VerifiedPartner, Mentor, MentorshipRequest,
    Job, Scholarship, LegalHealthResource, ServiceRating
)

def seed():
    print("Seeding database...")
    
    # 1. Admin & Users
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@nariguard.org', 'role': 'gov_admin', 'is_staff': True, 'is_superuser': True}
    )
    admin_user.set_password('admin123')
    admin_user.save()
    
    demo_user, _ = User.objects.get_or_create(
        username='demouser',
        defaults={'email': 'user@nariguard.org', 'role': 'user', 'phone': '+91 9876543210', 'region': 'Delhi'}
    )
    demo_user.set_password('user123')
    demo_user.save()

    mentor_user, _ = User.objects.get_or_create(
        username='anita_desai',
        defaults={'email': 'anita@google.com', 'role': 'mentor', 'phone': '+91 9811223344', 'region': 'Bangalore'}
    )

    # 2. Emergency Contacts
    EmergencyContact.objects.get_or_create(
        user=demo_user, name='Parent Emergency', phone='+91 9876543211', relation='Parent', verified=True
    )
    EmergencyContact.objects.get_or_create(
        user=demo_user, name='Local Guardian', phone='+91 9876543212', relation='Friend', verified=True
    )

    # 3. Verified Partners
    VerifiedPartner.objects.get_or_create(
        name='Delhi Women Helpline & Protection Center',
        defaults={'type': 'ngo', 'contact_info': 'Helpline: 1091 | Email: support@delhiwomen.org', 'region': 'Delhi', 'verification_status': 'verified', 'verified_by': admin_user}
    )
    VerifiedPartner.objects.get_or_create(
        name='Central Police Special Women Cell',
        defaults={'type': 'police', 'contact_info': 'Emergency: 112 | Station: Connaught Place', 'region': 'Delhi', 'verification_status': 'verified', 'verified_by': admin_user}
    )
    VerifiedPartner.objects.get_or_create(
        name='Legal Aid Society India',
        defaults={'type': 'legal', 'contact_info': 'Free Legal Aid: 15100 | Legal Helpdesk', 'region': 'National', 'verification_status': 'verified', 'verified_by': admin_user}
    )

    # 4. Mentors
    Mentor.objects.get_or_create(
        user=mentor_user,
        defaults={'industry': 'Technology', 'experience_years': 12, 'focus_area': 'Cloud Architecture & Engineering Leadership', 'availability': 'Weekends', 'verification_status': 'verified'}
    )

    # 5. Jobs
    Job.objects.get_or_create(
        title='Senior Software Engineer',
        defaults={'company': 'Microsoft', 'region': 'Remote / India', 'remote': True, 'source': 'Women in Tech Diversity Drive'}
    )
    Job.objects.get_or_create(
        title='Lead Product Manager',
        defaults={'company': 'FinTech Innovations', 'region': 'Bangalore', 'remote': False, 'source': 'Maternity & Flexi-Work Supported'}
    )
    Job.objects.get_or_create(
        title='Data Science Specialist',
        defaults={'company': 'Adobe', 'region': 'Noida / Hybrid', 'remote': True, 'source': 'SheCodes Career Returnship'}
    )

    # 6. Scholarships
    Scholarship.objects.get_or_create(
        title='Generation Google Scholarship (APAC)',
        defaults={'provider': 'Google', 'field': 'Computer Science & Engineering', 'education_level': 'Undergraduate', 'region': 'Asia Pacific', 'deadline': date(2026, 12, 31)}
    )
    Scholarship.objects.get_or_create(
        title='Women Techmakers Education Grant',
        defaults={'provider': 'Google Developers', 'field': 'STEM Fields', 'education_level': 'Postgraduate', 'region': 'Global', 'deadline': date(2026, 11, 30)}
    )

    # 7. Legal & Health Resources
    LegalHealthResource.objects.get_or_create(
        title='POSH Act 2013 Workplace Protection',
        defaults={'category': 'legal', 'region': 'National', 'content': 'Comprehensive guide on Internal Complaints Committee (ICC) procedures and rights against sexual harassment.', 'source_url': 'https://wcd.nic.in'}
    )
    LegalHealthResource.objects.get_or_create(
        title='Zero FIR Rights & Immediate Filing Guide',
        defaults={'category': 'legal', 'region': 'National', 'content': 'Zero FIR allows filing an official complaint in any police station across India regardless of crime location.', 'source_url': 'https://mha.gov.in'}
    )

    # 8. Service Ratings
    ServiceRating.objects.get_or_create(
        service_name='Police Response (100)',
        defaults={'rating': 5, 'feedback': 'Rapid dispatch within 6 minutes during night emergency patrol.'}
    )
    ServiceRating.objects.get_or_create(
        service_name='Women Helpline (1091)',
        defaults={'rating': 4, 'feedback': 'Courteous counselor provided clear legal guidance and counseling.'}
    )

    # 9. SOS Alert
    SosAlert.objects.get_or_create(
        lat=28.6139, lng=77.2090,
        defaults={'status': 'active', 'user': demo_user, 'emergency_contact': '+91 9876543211', 'admin_message': 'Patrol Unit 4 Dispatched. Arrival ETA 4 mins.'}
    )

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
