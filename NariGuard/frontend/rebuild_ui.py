import os
import glob

base_dir = r"f:\NariGuard\frontend"

# Remove old html files to clean up
for f in glob.glob(os.path.join(base_dir, "*.html")):
    os.remove(f)

# Write new user side
user_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NariGuard - User Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <style>
        body { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3); }
        .sos-btn { background: linear-gradient(135deg, #ff416c, #ff4b2b); box-shadow: 0 10px 30px rgba(255, 65, 108, 0.4); }
    </style>
</head>
<body class="min-h-screen text-gray-800">
    <nav class="glass sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-500">NariGuard</div>
            <div class="flex gap-4">
                <a href="admin.html" class="px-4 py-2 rounded-full border border-purple-200 text-purple-600 hover:bg-purple-50 font-semibold transition">Admin Panel</a>
            </div>
        </div>
    </nav>
    <main class="max-w-7xl mx-auto px-6 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Left Column: SOS -->
            <div class="lg:col-span-1 flex flex-col items-center justify-center glass p-10 rounded-3xl text-center h-full">
                <h2 class="text-3xl font-black mb-4">Emergency</h2>
                <p class="text-gray-500 mb-12">Press instantly to alert authorities & contacts</p>
                <button id="sos-btn" class="sos-btn w-56 h-56 rounded-full text-white font-black text-5xl transition transform hover:scale-105 active:scale-95 animate-pulse">
                    SOS
                </button>
                <p id="sos-status" class="hidden mt-8 text-red-500 font-bold text-xl">Alert Sent! Siren Active!</p>
            </div>
            
            <!-- Right Column: Map & AI -->
            <div class="lg:col-span-2 space-y-8">
                <!-- Map -->
                <div class="glass p-6 rounded-3xl">
                    <h3 class="text-xl font-bold mb-4 flex justify-between items-center">
                        <span>Safe Routes & Nearby Spots</span>
                        <button id="find-nearby-btn" class="text-sm bg-purple-100 text-purple-700 px-4 py-2 rounded-full font-bold hover:bg-purple-200 transition">Find Police/Hospitals</button>
                    </h3>
                    <div id="map" class="w-full h-72 rounded-2xl border border-gray-200 z-0"></div>
                </div>
                
                <!-- AI Assistant -->
                <div class="glass p-6 rounded-3xl">
                    <h3 class="text-xl font-bold mb-4">AI Career & Safety Guide</h3>
                    <div class="flex gap-2 mb-4">
                        <input type="text" id="ai-prompt" class="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-400" placeholder="Ask about self-defense, legal rights, or career...">
                        <button id="ask-ai-btn" class="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-6 py-3 rounded-xl font-bold hover:opacity-90 transition">Ask AI</button>
                    </div>
                    <div id="ai-response" class="hidden p-4 bg-gray-50 rounded-xl text-gray-700 h-32 overflow-y-auto text-sm border border-gray-100"></div>
                </div>
            </div>
        </div>
    </main>
    <script type="module" src="./main.js"></script>
</body>
</html>
"""

admin_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NariGuard - Admin Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
        .glass-dark { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); }
    </style>
</head>
<body class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 glass-dark h-full flex flex-col border-r border-white/10 shadow-2xl z-10">
        <div class="p-6">
            <h1 class="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300">NariGuard Admin</h1>
        </div>
        <nav class="flex-1 px-4 space-y-2 mt-4">
            <a href="#" class="block px-4 py-3 rounded-xl bg-blue-600 bg-opacity-20 text-blue-400 font-bold border border-blue-500/30">Dashboard</a>
            <a href="index.html" class="block px-4 py-3 rounded-xl hover:bg-white/5 text-gray-400 transition">Back to User Site</a>
        </nav>
        <div class="p-4">
            <button id="logout-btn" class="w-full py-3 rounded-xl bg-red-500/10 text-red-400 font-bold hover:bg-red-500/20 transition">Logout System</button>
        </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto relative">
        <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 z-0 pointer-events-none"></div>
        <div class="relative z-10">
            <header class="flex justify-between items-center mb-10">
                <h2 class="text-3xl font-bold tracking-tight">Live Control Center</h2>
                <div class="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-full border border-white/10">
                    <span class="relative flex h-3 w-3">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                      <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                    </span>
                    <span class="text-green-400 font-mono text-sm tracking-wider">SYSTEM ONLINE</span>
                </div>
            </header>
    
            <!-- Stats -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="glass-dark p-6 rounded-2xl transform transition hover:-translate-y-1">
                    <p class="text-gray-400 text-sm font-bold uppercase tracking-wider mb-2">Active SOS Alerts</p>
                    <p class="text-5xl font-black text-red-400">2</p>
                </div>
                <div class="glass-dark p-6 rounded-2xl transform transition hover:-translate-y-1">
                    <p class="text-gray-400 text-sm font-bold uppercase tracking-wider mb-2">Total Rescues</p>
                    <p class="text-5xl font-black text-blue-400">1,248</p>
                </div>
                <div class="glass-dark p-6 rounded-2xl transform transition hover:-translate-y-1">
                    <p class="text-gray-400 text-sm font-bold uppercase tracking-wider mb-2">Registered Users</p>
                    <p class="text-5xl font-black text-purple-400">342</p>
                </div>
            </div>
    
            <!-- Charts & Data -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 glass-dark p-6 rounded-2xl h-96 border border-white/10 shadow-xl">
                    <h3 class="text-lg font-bold mb-4 text-gray-200">Incident Analytics</h3>
                    <canvas id="adminChart"></canvas>
                </div>
                <div class="lg:col-span-1 glass-dark p-6 rounded-2xl overflow-hidden flex flex-col border border-white/10 shadow-xl">
                    <h3 class="text-lg font-bold mb-4 text-red-400 flex items-center gap-2">
                        <svg class="w-5 h-5 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        Live Alerts Feed
                    </h3>
                    <div class="flex-1 space-y-4 overflow-y-auto pr-2">
                        <div class="p-4 bg-red-500/10 border border-red-500/20 rounded-xl relative overflow-hidden group">
                            <div class="absolute inset-0 bg-red-500/5 translate-x-[-100%] group-hover:translate-x-0 transition-transform duration-300"></div>
                            <p class="text-sm font-bold text-red-300 relative z-10">SOS Triggered</p>
                            <p class="text-xs text-gray-400 mt-1 relative z-10 font-mono">Lat: 28.6139, Lng: 77.2090</p>
                            <p class="text-xs text-red-400 mt-2 relative z-10 font-semibold">Just now</p>
                        </div>
                        <div class="p-4 bg-white/5 border border-white/10 rounded-xl">
                            <p class="text-sm font-bold text-gray-300">SOS Resolved</p>
                            <p class="text-xs text-gray-400 mt-1 font-mono">Lat: 19.0760, Lng: 72.8777</p>
                            <p class="text-xs text-gray-500 mt-2 font-semibold">1 hr ago</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <script>
        const ctx = document.getElementById('adminChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Women Assisted',
                    data: [120, 190, 300, 500, 420, 600],
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#60a5fa',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#60a5fa'
                }]
            },
            options: { 
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#94a3b8' } } },
                scales: { 
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    </script>
    <script type="module" src="./main.js"></script>
</body>
</html>
"""

with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(user_html)

with open(os.path.join(base_dir, "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)

print("New Premium UI/UX built successfully.")
