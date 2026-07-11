from fpdf import FPDF

def create_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content)
    pdf.output(filename)

create_pdf(
    "f:/NariGuard/frontend/posh_act.pdf", 
    "The POSH Act (2013) - Legal Guide", 
    "Protection of Women from Sexual Harassment at Workplace (Prevention, Prohibition and Redressal) Act, 2013.\n\n"
    "This act mandates employers to form Internal Complaints Committees (ICC) in workplaces with 10 or more employees.\n\n"
    "Key Provisions:\n"
    "1. Defines sexual harassment clearly.\n"
    "2. Mandates the constitution of an ICC.\n"
    "3. Outlines the complaint mechanism and redressal process.\n"
    "4. Protects the complainant against victimization."
)

create_pdf(
    "f:/NariGuard/frontend/zero_fir.pdf", 
    "Zero FIR Rights - Fact Sheet", 
    "A Zero FIR is an FIR that can be registered by any police station, irrespective of jurisdiction, when it receives a complaint regarding a cognizable offence.\n\n"
    "Why it is crucial for women:\n"
    "1. Immediate action can be taken without jurisdictional delays.\n"
    "2. It prevents evidence from being destroyed.\n"
    "3. After registration, the Zero FIR is transferred to the police station with actual jurisdiction for investigation."
)

create_pdf(
    "f:/NariGuard/frontend/maternity_act.pdf", 
    "Maternity Benefit Act", 
    "The Maternity Benefit Act guarantees 26 weeks of paid maternity leave for women working in establishments with 10 or more employees.\n\n"
    "Key Rights:\n"
    "1. 26 weeks of paid leave for the first two children.\n"
    "2. 12 weeks of paid leave for a third child or for adopting a child below 3 months.\n"
    "3. Work from home options post the maternity leave period, if the nature of work permits.\n"
    "4. Mandatory crèche facility for establishments with 50 or more employees."
)

create_pdf(
    "f:/NariGuard/frontend/wellness_guide.pdf", 
    "Comprehensive Mental Wellness Guide", 
    "This guide provides all essential mental wellness resources for women in distress and professionals seeking support.\n\n"
    "National Crisis Hotlines (India):\n"
    "1. Women Helpline (All India) - 1091\n"
    "2. Domestic Abuse National Helpline - 181\n"
    "3. KIRAN (Mental Health Helpline) - 1800-599-0019\n"
    "4. Vandrevala Foundation (24x7) - 9999 666 555\n\n"
    "Online Therapy Platforms:\n"
    "1. Trijog - Specialized care and therapy.\n"
    "2. MindTribe - Affordable and accessible counseling.\n"
    "3. InnerHour - App-based psychological wellness tools."
)
