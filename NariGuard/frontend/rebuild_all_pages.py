import os

base_dir = r"f:\NariGuard\frontend"

nav_template = """
    <nav class="glass sticky top-0 z-50 shadow-sm transition-colors duration-300 dark:bg-gray-900/80 dark:border-b dark:border-gray-800">
        <div class="max-w-7xl mx-auto px-6 py-4 flex flex-wrap justify-between items-center gap-4">
            <div class="text-2xl font-black bg-clip-text text-transparent grad-bg-text">NariGuard</div>
            <div class="flex flex-wrap gap-4 items-center">
                <a href="index.html" class="font-semibold text-gray-700 dark:text-gray-300 hover-text-primary transition">Home</a>
                <a href="safe-routes.html" class="font-semibold text-gray-700 dark:text-gray-300 hover-text-primary transition">Routes</a>
                <a href="career.html" class="font-semibold text-gray-700 dark:text-gray-300 hover-text-primary transition">AI Career</a>
                <a href="mentors.html" class="font-semibold text-gray-700 dark:text-gray-300 hover-text-primary transition">Mentors</a>
                <a href="resources.html" class="font-semibold text-gray-700 dark:text-gray-300 hover-text-primary transition">Resources</a>
                <a href="jobs.html" class="font-semibold text-gray-700 dark:text-gray-300 hover-text-primary transition">Jobs</a>
                
                <!-- Color Cycle Button -->
                <button id="color-cycle-btn" class="p-2 rounded-full bg-primary-light text-primary hover:scale-110 transition shadow-sm" title="Change Color Theme">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
                </button>

                <!-- Dark/Light Toggle Button -->
                <button id="theme-toggle" class="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white transition">
                    <svg id="theme-icon-light" class="w-5 h-5 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                    <svg id="theme-icon-dark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                </button>
                <a href="admin.html" class="px-4 py-2 rounded-full border border-primary-light text-primary hover-bg-primary-light font-semibold transition">Admin</a>
            </div>
        </div>
    </nav>
"""

html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NariGuard Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = { darkMode: 'class' }
    </script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.css" />
    <script src="https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js"></script>
    <style>
        :root {
            --primary-start: #9333ea; /* purple-600 */
            --primary-end: #ec4899;   /* pink-500 */
            --primary-text: #9333ea;
            --primary-bg: #f3e8ff;    /* purple-100 */
            --primary-border: #e9d5ff; /* purple-200 */
        }
        .theme-blue {
            --primary-start: #2563eb;
            --primary-end: #06b6d4;
            --primary-text: #2563eb;
            --primary-bg: #dbeafe;
            --primary-border: #bfdbfe;
        }
        .theme-green {
            --primary-start: #16a34a;
            --primary-end: #84cc16;
            --primary-text: #16a34a;
            --primary-bg: #dcfce7;
            --primary-border: #bbf7d0;
        }
        
        .grad-bg-text { background-image: linear-gradient(to right, var(--primary-start), var(--primary-end)); }
        .grad-btn { background-image: linear-gradient(to right, var(--primary-start), var(--primary-end)); }
        .text-primary { color: var(--primary-text); }
        .bg-primary-light { background-color: var(--primary-bg); }
        .border-primary-light { border-color: var(--primary-border); }
        .hover-text-primary:hover { color: var(--primary-text); }
        .hover-bg-primary-light:hover { background-color: var(--primary-bg); }

        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; transition: background-color 0.3s, color 0.3s; }
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3); }
        .dark .glass { background: rgba(31, 41, 55, 0.7); border: 1px solid rgba(255,255,255,0.05); }
        .sos-btn { background: linear-gradient(135deg, #ff416c, #ff4b2b); box-shadow: 0 10px 30px rgba(255, 65, 108, 0.4); }
    </style>
</head>
<body class="min-h-screen text-gray-800 dark:text-gray-200 bg-gradient-to-br from-gray-50 to-gray-200 dark:from-gray-900 dark:to-gray-900 theme-purple">
"""

footer = """
    <script src="https://www.gstatic.com/firebasejs/10.9.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.9.0/firebase-auth-compat.js"></script>
    <script src="./main.js"></script>
</body>
</html>
"""

pages = {
    "index.html": f"""{html_head}
    {nav_template}
    <main class="max-w-7xl mx-auto px-6 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Left Column: SOS -->
            <div class="lg:col-span-1 flex flex-col items-center justify-center glass p-10 rounded-3xl text-center h-full transform transition hover:-translate-y-1 hover:shadow-2xl">
                <h2 class="text-3xl font-black mb-4 dark:text-white">Emergency</h2>
                <p class="text-gray-500 dark:text-gray-400 mb-12">Press instantly to alert authorities & contacts</p>
                <button id="sos-btn" class="sos-btn w-56 h-56 rounded-full text-white font-black text-5xl transition transform hover:scale-105 active:scale-95 animate-pulse shadow-2xl">
                    SOS
                </button>
                <p id="sos-status" class="hidden mt-8 text-red-500 font-bold text-xl animate-bounce">Alert Sent! Siren Active!</p>
                <div class="mt-8 w-full">
                    <label class="block text-sm font-bold text-gray-500 dark:text-gray-400 mb-2">My Emergency Contact No.</label>
                    <input type="text" id="emergency-contact-input" placeholder="+91 9876543210" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:border-primary-light text-center font-bold text-lg tracking-wider shadow-inner transition">
                </div>
            </div>
            
            <!-- Right Column: Map & AI -->
            <div class="lg:col-span-2 space-y-8">
                <!-- Map -->
                <div class="glass p-6 rounded-3xl">
                    <h3 class="text-xl font-bold mb-4 flex justify-between items-center dark:text-white">
                        <span>Safe Routes & Nearby Spots</span>
                        <div class="flex gap-2">
                            <button id="plan-route-btn" class="text-xs grad-btn text-white px-3 py-2 rounded-full font-bold shadow hover:opacity-90 transition">Plan Route</button>
                            <button id="find-nearby-btn" class="text-xs bg-primary-light text-primary px-3 py-2 rounded-full font-bold shadow hover:opacity-80 transition">Find Police</button>
                        </div>
                    </h3>
                    <div id="map" class="w-full h-72 rounded-2xl border-4 border-gray-200 dark:border-gray-700 shadow-inner z-0"></div>
                </div>
                
                <!-- AI Assistant -->
                <div class="glass p-6 rounded-3xl">
                    <h3 class="text-xl font-bold mb-4 dark:text-white text-primary">AI Safety & Legal Guide</h3>
                    <div class="flex gap-2 mb-4">
                        <input type="text" id="ai-prompt" class="flex-1 px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-600 dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:border-primary-light" placeholder="Ask about self-defense, rights, or career...">
                        <button id="ask-ai-btn" class="grad-btn text-white px-6 py-3 rounded-xl font-bold hover:opacity-90 transition shadow">Ask AI</button>
                    </div>
                    <div id="ai-response" class="hidden p-4 bg-gray-50 dark:bg-gray-800 rounded-xl text-gray-700 dark:text-gray-300 h-32 overflow-y-auto text-sm border border-gray-200 dark:border-gray-700 shadow-inner"></div>
                </div>
            </div>
        </div>
    </main>
    {footer}""",

    "safe-routes.html": f"""{html_head}
    {nav_template}
    <main class="max-w-7xl mx-auto px-6 py-12">
        <div class="glass p-8 rounded-3xl">
            <h2 class="text-3xl font-black mb-6 dark:text-white flex justify-between items-center">
                Safe Routes & Nearby Verification
                <div class="flex gap-4">
                    <button id="plan-route-btn" class="text-sm grad-btn text-white px-5 py-3 rounded-full font-bold shadow-lg hover:opacity-90 transition">Plan Safe Route</button>
                    <button id="find-nearby-btn" class="text-sm bg-primary-light text-primary border border-primary-light px-5 py-3 rounded-full font-bold shadow-lg hover:opacity-80 transition">Find Safe Spots</button>
                </div>
            </h2>
            <div id="map" class="w-full h-[600px] rounded-2xl border-4 border-gray-200 dark:border-gray-700 shadow-inner z-0"></div>
        </div>
        
        <div class="mt-12 glass p-8 rounded-3xl">
            <h2 class="text-2xl font-bold mb-6 dark:text-white">Verified Emergency Contacts</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="p-6 bg-red-500/10 border-l-4 border-red-500 rounded-xl">
                    <h3 class="font-bold text-lg dark:text-white">National Commission for Women</h3>
                    <a href="tel:7827170170" class="text-red-500 font-black text-2xl mt-2 block">7827170170</a>
                </div>
                <div class="p-6 bg-blue-500/10 border-l-4 border-blue-500 rounded-xl">
                    <h3 class="font-bold text-lg dark:text-white">Cyber Crime Helpline</h3>
                    <a href="tel:1930" class="text-blue-500 font-black text-2xl mt-2 block">1930</a>
                </div>
                <div class="p-6 bg-green-500/10 border-l-4 border-green-500 rounded-xl">
                    <h3 class="font-bold text-lg dark:text-white">Women in Distress NGO</h3>
                    <a href="tel:1091" class="text-green-500 font-black text-2xl mt-2 block">1091</a>
                </div>
            </div>
        </div>
    </main>
    {footer}""",

    "career.html": f"""{html_head}
    {nav_template}
    <main class="max-w-7xl mx-auto px-6 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="glass p-8 rounded-3xl">
                <h3 class="text-2xl font-black mb-4 dark:text-white text-primary">AI Career & Legal Assistant</h3>
                <p class="text-gray-500 dark:text-gray-400 mb-6">Ask Gemini AI about workplace rights, self-defense tactics, or interview strategies.</p>
                <div class="flex flex-col gap-4 mb-4">
                    <textarea id="ai-prompt" rows="4" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-600 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:border-primary-light" placeholder="e.g., What are my rights under the POSH Act?"></textarea>
                    <button id="ask-ai-btn" class="grad-btn text-white px-6 py-4 rounded-xl font-black text-lg hover:opacity-90 transition shadow-lg w-full">Generate AI Response</button>
                </div>
                <div id="ai-response" class="hidden p-6 bg-gray-50 dark:bg-gray-800 rounded-xl text-gray-700 dark:text-gray-300 h-64 overflow-y-auto text-sm border border-gray-200 dark:border-gray-700 shadow-inner leading-relaxed"></div>
            </div>
            
            <div class="glass p-8 rounded-3xl flex flex-col justify-center items-center text-center">
                <h3 class="text-2xl font-black mb-4 dark:text-white">AI Resume Review</h3>
                <p class="text-gray-500 dark:text-gray-400 mb-8">Upload your resume. Our AI will automatically score it against industry standards and provide tailored feedback to land high-paying roles.</p>
                <input type="file" id="resume-upload" accept=".pdf,.doc,.docx" class="mb-6 block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-light file:text-primary hover:file:opacity-80 dark:file:bg-gray-700 dark:file:text-white">
                <button id="submit-resume-btn" class="bg-gray-900 dark:bg-white dark:text-gray-900 text-white font-bold py-3 px-8 rounded-full shadow-xl w-full">Analyze Resume</button>
                <div id="resume-feedback" class="hidden mt-6 p-4 w-full bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400 rounded-xl text-sm font-medium"></div>
            </div>
        </div>
    </main>
    {footer}""",

    "mentors.html": f"""{html_head}
    {nav_template}
    <main class="max-w-7xl mx-auto px-6 py-12">
        <h2 class="text-3xl font-black mb-8 dark:text-white text-center">Verified Women Mentor Network</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Mentor 1 -->
            <div class="glass p-8 rounded-3xl text-center transform transition hover:-translate-y-2">
                <div class="w-24 h-24 bg-gradient-to-tr from-purple-400 to-pink-500 rounded-full mx-auto mb-4 shadow-lg"></div>
                <h3 class="font-black text-xl dark:text-white">Dr. Anita Desai</h3>
                <p class="text-purple-600 font-bold text-sm mb-4">Tech Lead @ Google</p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mb-6">Expert in scalable architecture and navigating male-dominated corporate spaces.</p>
                <button onclick="alert('Mentorship Request sent! The mentor will review your profile shortly.')" class="w-full py-3 bg-gray-900 dark:bg-white dark:text-gray-900 text-white font-bold rounded-xl hover:opacity-80">Request Mentorship</button>
            </div>
            <!-- Mentor 2 -->
            <div class="glass p-8 rounded-3xl text-center transform transition hover:-translate-y-2">
                <div class="w-24 h-24 bg-gradient-to-tr from-blue-400 to-cyan-500 rounded-full mx-auto mb-4 shadow-lg"></div>
                <h3 class="font-black text-xl dark:text-white">Priya Sharma, Esq.</h3>
                <p class="text-blue-600 font-bold text-sm mb-4">Corporate Lawyer</p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mb-6">Specializes in POSH act compliance and contract negotiation for women founders.</p>
                <button onclick="alert('Mentorship Request sent! The mentor will review your profile shortly.')" class="w-full py-3 bg-gray-900 dark:bg-white dark:text-gray-900 text-white font-bold rounded-xl hover:opacity-80">Request Mentorship</button>
            </div>
            <!-- Mentor 3 -->
            <div class="glass p-8 rounded-3xl text-center transform transition hover:-translate-y-2">
                <div class="w-24 h-24 bg-gradient-to-tr from-green-400 to-emerald-500 rounded-full mx-auto mb-4 shadow-lg"></div>
                <h3 class="font-black text-xl dark:text-white">Meera Reddy</h3>
                <p class="text-green-600 font-bold text-sm mb-4">Founder, TechShe</p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mb-6">Serial entrepreneur focused on funding and scaling early-stage startups.</p>
                <button onclick="alert('Mentorship Request sent! The mentor will review your profile shortly.')" class="w-full py-3 bg-gray-900 dark:bg-white dark:text-gray-900 text-white font-bold rounded-xl hover:opacity-80">Request Mentorship</button>
            </div>
        </div>
    </main>
    {footer}""",

    "resources.html": f"""{html_head}
    {nav_template}
    <main class="max-w-7xl mx-auto px-6 py-12">
        <h2 class="text-3xl font-black mb-8 dark:text-white text-center">Legal & Health Resource Center</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="glass p-8 rounded-3xl border-t-8 border-purple-500">
                <h3 class="font-black text-2xl dark:text-white mb-4">The POSH Act (2013)</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-4">Protection of Women from Sexual Harassment at Workplace. Mandates employers to form Internal Complaints Committees (ICC).</p>
                <a href="./posh_act.pdf" download="POSH_Act_2013_Guide.pdf" class="text-purple-600 font-bold hover:underline cursor-pointer">Read Full Legal Guide &rarr;</a>
            </div>
            <div class="glass p-8 rounded-3xl border-t-8 border-pink-500">
                <h3 class="font-black text-2xl dark:text-white mb-4">Zero FIR Rights</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-4">A Zero FIR can be filed in any police station, irrespective of jurisdiction. Crucial for immediate action in crimes against women.</p>
                <a href="./zero_fir.pdf" download="Zero_FIR_Fact_Sheet.pdf" class="text-pink-600 font-bold hover:underline cursor-pointer">Download Fact Sheet &rarr;</a>
            </div>
            <div class="glass p-8 rounded-3xl border-t-8 border-blue-500">
                <h3 class="font-black text-2xl dark:text-white mb-4">Maternity Benefit Act</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-4">Guarantees 26 weeks of paid maternity leave for women working in establishments with 10 or more employees.</p>
                <a href="./maternity_act.pdf" download="Maternity_Benefit_Act.pdf" class="text-blue-600 font-bold hover:underline cursor-pointer">Learn Your Rights &rarr;</a>
            </div>
            <div class="glass p-8 rounded-3xl border-t-8 border-green-500">
                <h3 class="font-black text-2xl dark:text-white mb-4">Mental Wellness Guide</h3>
                <p class="text-gray-600 dark:text-gray-300 mb-4">Free resources, coping mechanisms, and subsidized therapy options for trauma survivors and working professionals.</p>
                <a href="./wellness_guide.pdf" download="Comprehensive_Wellness_Guide.pdf" class="text-green-600 font-bold hover:underline cursor-pointer">Access Wellness Portal &rarr;</a>
            </div>
        </div>

        <div class="mt-16 bg-white/5 border border-white/10 p-8 rounded-3xl backdrop-blur-md">
            <h2 class="text-3xl font-black text-white mb-4">Rate Government Services</h2>
            <p class="text-gray-400 mb-6">Help us hold public emergency services accountable. Submit your anonymous feedback directly to the Admin Dashboard.</p>
            <div class="flex flex-col md:flex-row gap-4">
                <select id="gov-service-select" class="bg-gray-800 text-white rounded-xl px-4 py-3 border border-gray-700 outline-none focus:border-blue-500 transition">
                    <option>Police Response (100)</option>
                    <option>Women Helpline (1091)</option>
                    <option>Ambulance Service (108)</option>
                    <option>Cyber Crime Cell</option>
                </select>
                <select id="gov-rating-select" class="bg-gray-800 text-yellow-400 font-bold rounded-xl px-4 py-3 border border-gray-700 outline-none focus:border-blue-500 transition">
                    <option value="5">★★★★★ Excellent</option>
                    <option value="4">★★★★☆ Good</option>
                    <option value="3">★★★☆☆ Average</option>
                    <option value="2">★★☆☆☆ Poor</option>
                    <option value="1">★☆☆☆☆ Terrible</option>
                </select>
                <input type="text" id="gov-feedback" placeholder="Write optional feedback or complaints..." class="flex-1 bg-gray-800 text-white rounded-xl px-4 py-3 border border-gray-700 outline-none focus:border-blue-500 transition">
                <button onclick="submitGovRating()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-xl transition shadow-lg shadow-blue-500/30">Submit Rating</button>
            </div>
        </div>
    </main>
    {footer}""",

    "jobs.html": f"""{html_head}
    {nav_template}
    <main class="max-w-7xl mx-auto px-6 py-12">
        <h2 class="text-3xl font-black mb-8 dark:text-white text-center">Exclusive Jobs & Scholarships</h2>
        <div class="glass p-8 rounded-3xl mb-8">
            <h3 class="text-2xl font-bold dark:text-white mb-6 border-b pb-4 dark:border-gray-700">Top Job Openings (Diversity Drives)</h3>
            <div class="space-y-4">
                <div class="flex justify-between items-center p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div>
                        <h4 class="font-bold text-lg dark:text-white">Senior Software Engineer</h4>
                        <p class="text-gray-500 text-sm">Microsoft • Remote • Women in Tech Initiative</p>
                    </div>
                    <button onclick="alert('Application sent! Your Resume Profile has been forwarded.')" class="bg-primary-light text-primary px-4 py-2 rounded-lg font-bold">Apply Now</button>
                </div>
                <div class="flex justify-between items-center p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div>
                        <h4 class="font-bold text-lg dark:text-white">Product Manager</h4>
                        <p class="text-gray-500 text-sm">FinTech Startup • Bangalore • Maternity Support Included</p>
                    </div>
                    <button onclick="alert('Application sent! Your Resume Profile has been forwarded.')" class="bg-primary-light text-primary px-4 py-2 rounded-lg font-bold">Apply Now</button>
                </div>
            </div>
        </div>
        
        <div class="glass p-8 rounded-3xl">
            <h3 class="text-2xl font-bold dark:text-white mb-6 border-b pb-4 dark:border-gray-700">Scholarships & Grants</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="p-6 bg-pink-50 dark:bg-pink-900/20 rounded-xl border border-pink-100 dark:border-pink-800">
                    <h4 class="font-black text-xl text-pink-700 dark:text-pink-400 mb-2">Google Anita Borg Memorial</h4>
                    <p class="text-gray-600 dark:text-gray-300 text-sm mb-4">$10,000 grant for women pursuing computer science degrees.</p>
                    <a href="https://buildyourfuture.withgoogle.com/scholarships/generation-google-scholarship" target="_blank" class="font-bold text-pink-600 hover:underline">Check Eligibility</a>
                </div>
                <div class="p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-100 dark:border-blue-800">
                    <h4 class="font-black text-xl text-blue-700 dark:text-blue-400 mb-2">Women Techmakers Grant</h4>
                    <p class="text-gray-600 dark:text-gray-300 text-sm mb-4">Funding and community support for early-stage women founders.</p>
                    <a href="https://developers.google.com/womentechmakers" target="_blank" class="font-bold text-blue-600 hover:underline">Apply Today</a>
                </div>
            </div>
        </div>
    </main>
    {footer}"""
}

for filename, content in pages.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully generated all premium UI pages with theme toggler!")
