import os

base_dir = r"f:\NariGuard\frontend"
index_path = os.path.join(base_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split the content
# We will identify sections by their <section id="..."> tags
import re

sections = {
    "home": re.search(r'(<section id="home".*?</section>)', content, re.DOTALL).group(1),
    "map": re.search(r'(<section id="map-section".*?</section>)', content, re.DOTALL).group(1),
    "career": re.search(r'(<section id="career".*?</section>)', content, re.DOTALL).group(1),
    "mentors": re.search(r'(<section id="mentors".*?</section>)', content, re.DOTALL).group(1),
    "resources": re.search(r'(<section id="resources".*?</section>)', content, re.DOTALL).group(1),
    "resume": re.search(r'(<section id="resume-review".*?</section>)', content, re.DOTALL).group(1),
    "admin": re.search(r'(<section id="admin-panel".*?</section>)', content, re.DOTALL).group(1),
}

# The header is everything before <main...>
head_and_nav = re.search(r'(.*?<main[^>]*>)', content, re.DOTALL).group(1)

# The footer is everything after </main>
footer_and_scripts = re.search(r'(</main>.*)', content, re.DOTALL).group(1)

def write_page(filename, sections_to_include, page_title):
    # Adjust nav links based on filename
    nav = head_and_nav
    nav = nav.replace('href="#home"', 'href="index.html"')
    nav = nav.replace('href="#map-section"', 'href="safe-routes.html"')
    nav = nav.replace('href="#career"', 'href="career.html"')
    nav = nav.replace('href="#resources"', 'href="resources.html"')
    nav = nav.replace('NariGuard - Women Safety & Empowerment Platform', f'NariGuard - {page_title}')
    
    # Add extra links to nav for the new pages
    nav = nav.replace('<a href="career.html" class="nav-link">Career & AI</a>', '<a href="career.html" class="nav-link">Career & AI</a>\n                <a href="mentors.html" class="nav-link">Mentors</a>\n                <a href="jobs.html" class="nav-link">Jobs</a>')
    
    body = "\n".join([sections[s] for s in sections_to_include])
    
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(nav + "\n" + body + "\n" + footer_and_scripts)

# Create Pages
write_page("index.html", ["home", "admin"], "Home")
write_page("safe-routes.html", ["map"], "Safe Routes")
write_page("career.html", ["career", "resume"], "Career & AI")
write_page("mentors.html", ["mentors"], "Mentor Network")
write_page("resources.html", ["resources"], "Legal & Health")
write_page("jobs.html", ["career"], "Jobs & Scholarships") # Just reusing career for now, or extracting the jobs div

print("Pages created successfully!")
