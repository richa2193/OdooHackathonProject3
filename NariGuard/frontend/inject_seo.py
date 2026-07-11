import os
import glob

base_dir = r"f:\NariGuard\frontend"
html_files = glob.glob(os.path.join(base_dir, "*.html"))

seo_template = """    <meta name="description" content="{description}" />
    <meta name="keywords" content="women safety, empowerment, sos alert, safe routes, career guidance, women mentor, legal rights for women, health resources, hackathon project" />
    <meta name="author" content="NariGuard Team" />
    <meta name="robots" content="index, follow" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />"""

page_data = {
    "index.html": {
        "title": "NariGuard - Women Safety & Empowerment Platform",
        "description": "NariGuard is a comprehensive digital platform offering instant SOS alerts, live geolocation tracking, and tools for women's safety and empowerment."
    },
    "safe-routes.html": {
        "title": "Safe Routes & Nearby Spots | NariGuard",
        "description": "Plan your journey safely. Use our real-time routing to find verified police stations, hospitals, and safe zones mapped dynamically."
    },
    "career.html": {
        "title": "AI Career Guidance | NariGuard",
        "description": "Get free, instant career guidance, mock interviews, and resume reviews driven by Google Gemini AI tailored for women professionals."
    },
    "mentors.html": {
        "title": "Women Mentor Network | NariGuard",
        "description": "Connect with industry leaders, request guidance, and build your career through our verified Women Mentor Network."
    },
    "resources.html": {
        "title": "Legal & Health Resource Center | NariGuard",
        "description": "Access vital information about women's legal rights (POSH Act, Zero FIR) and wellness guides to support your mental and reproductive health."
    },
    "jobs.html": {
        "title": "Jobs & Scholarships | NariGuard",
        "description": "Discover curated job opportunities, scholarships, and educational grants focused on empowering women in the workforce."
    }
}

for file_path in html_files:
    filename = os.path.basename(file_path)
    if filename in page_data:
        data = page_data[filename]
        seo_tags = seo_template.format(title=data["title"], description=data["description"])
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find the <title> tag and insert the SEO tags right after it
        if "<title>" in content:
            # We already have a title, let's inject after it
            # But the title tag might be different, let's just find the closing title tag
            parts = content.split("</title>")
            new_content = parts[0] + "</title>\n" + seo_tags + parts[1]
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

print("SEO injected successfully into all HTML files!")
