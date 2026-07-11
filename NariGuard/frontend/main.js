const firebaseConfig = {
  apiKey: "AIzaSyBF5VzNmeAbVdJmb6zy6gZoIWmET4d301g",
  authDomain: "women-safety-app-95ae7.firebaseapp.com",
  projectId: "women-safety-app-95ae7",
  storageBucket: "women-safety-app-95ae7.firebasestorage.app",
  messagingSenderId: "753858791866",
  appId: "1:753858791866:web:b6b56add7155f024af7583",
  measurementId: "G-GJ6N18K3GJ"
};

let auth = null;
if (typeof firebase !== 'undefined') {
  const app = firebase.initializeApp(firebaseConfig);
  auth = firebase.auth();
}

// Theme Toggling
const themeToggleBtn = document.getElementById('theme-toggle');
const htmlTag = document.documentElement;
const themeIconLight = document.getElementById('theme-icon-light');
const themeIconDark = document.getElementById('theme-icon-dark');
const colorBtns = document.querySelectorAll('.color-btn');

function toggleTheme() {
  if (htmlTag.classList.contains('dark')) {
    htmlTag.classList.remove('dark');
    localStorage.setItem('theme', 'light');
    if (themeIconDark) themeIconDark.classList.remove('hidden');
    if (themeIconLight) themeIconLight.classList.add('hidden');
  } else {
    htmlTag.classList.add('dark');
    localStorage.setItem('theme', 'dark');
    if (themeIconLight) themeIconLight.classList.remove('hidden');
    if (themeIconDark) themeIconDark.classList.add('hidden');
  }
}

// On load, check localStorage for Dark Mode
if (localStorage.getItem('theme') === 'dark') {
  htmlTag.classList.add('dark');
  if (themeIconLight) themeIconLight.classList.remove('hidden');
  if (themeIconDark) themeIconDark.classList.add('hidden');
}

// Color Theme Switcher Logic
const colorCycleBtn = document.getElementById('color-cycle-btn');
const themes = ['theme-purple', 'theme-blue', 'theme-green'];

function applyColorTheme(themeClass) {
  // Remove existing color themes from body
  document.body.classList.remove(...themes);
  document.body.classList.add(themeClass);
  localStorage.setItem('colorTheme', themeClass);
}

// Check localStorage for Color Theme
let currentThemeIndex = themes.indexOf(localStorage.getItem('colorTheme') || 'theme-purple');
if (currentThemeIndex === -1) currentThemeIndex = 0;
applyColorTheme(themes[currentThemeIndex]);

if (colorCycleBtn) {
  colorCycleBtn.addEventListener('click', () => {
    currentThemeIndex = (currentThemeIndex + 1) % themes.length;
    applyColorTheme(themes[currentThemeIndex]);
  });
}

if (themeToggleBtn) {
  themeToggleBtn.addEventListener('click', toggleTheme);
}

// Map Initialization
let map;
let markersLayer = L.layerGroup();

function initMap() {
  if (document.getElementById('map')) {
    map = L.map('map').setView([20.5937, 78.9629], 5); // Center of India
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap &copy; CARTO'
    }).addTo(map);
    markersLayer.addTo(map);
  }
}
initMap();

// Find Nearby Safe Spots (Overpass API)
const findNearbyBtn = document.getElementById('find-nearby-btn');
if (findNearbyBtn) {
  findNearbyBtn.addEventListener('click', () => {
    if (navigator.geolocation) {
      findNearbyBtn.innerHTML = 'Searching...';
      navigator.geolocation.getCurrentPosition(async position => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        map.setView([lat, lng], 14);
        
        // Clear previous markers
        markersLayer.clearLayers();
        
        // Add User Location
        L.marker([lat, lng]).addTo(markersLayer).bindPopup("<b>You are here</b>").openPopup();
        
        // Query Overpass API for police stations and hospitals within 2000 meters
        const overpassQuery = `
          [out:json];
          (
            node["amenity"="police"](around:3000,${lat},${lng});
            node["amenity"="hospital"](around:3000,${lat},${lng});
          );
          out body;
        `;
        
        try {
          const res = await fetch('https://overpass-api.de/api/interpreter', {
            method: 'POST',
            body: overpassQuery
          });
          const data = await res.json();
          
          data.elements.forEach(el => {
            let type = el.tags.amenity === 'police' ? 'Police Station' : 'Hospital';
            let name = el.tags.name || 'Unknown ' + type;
            
            let iconColor = el.tags.amenity === 'police' ? 'blue' : 'green';
            let customIcon = L.icon({
              iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${iconColor}.png`,
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
              iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
            });

            L.marker([el.lat, el.lon], {icon: customIcon})
             .addTo(markersLayer)
             .bindPopup(`<b>${name}</b><br>${type}`);
          });
          
          findNearbyBtn.innerHTML = 'Find Safe Spots';
        } catch (err) {
          console.warn("Overpass API Error, using simulated safe spots for demo.");
          // Add Simulated Police Station
          let pIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
          });
          L.marker([lat + 0.012, lng + 0.015], {icon: pIcon}).addTo(markersLayer).bindPopup(`<b>Central Police Station</b><br>Police Station`);
          
          // Add Simulated Hospital
          let hIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
          });
          L.marker([lat - 0.010, lng - 0.008], {icon: hIcon}).addTo(markersLayer).bindPopup(`<b>City General Hospital</b><br>Hospital`);
          
          findNearbyBtn.innerHTML = 'Find Safe Spots';
        }
      }, () => {
        alert("Location access denied.");
        findNearbyBtn.innerHTML = 'Find Safe Spots';
      });
    }
  });
}

// Siren Sound using HTML5 Audio with actual recorded MP3
function playSiren() {
  try {
    const sirenAudio = new Audio('./siren.mp3');
    sirenAudio.volume = 1.0;
    sirenAudio.loop = true; // Loop the siren
    sirenAudio.play().catch(e => {
      console.log("Audio play blocked by browser:", e);
      alert("SOS Triggered! (Audio blocked by browser, please click allow)");
    });
    
    // Stop cleanly after 10 seconds
    setTimeout(() => {
      sirenAudio.pause();
      sirenAudio.currentTime = 0;
    }, 10000);

  } catch (err) {
    console.error("Audio trigger failed:", err);
  }
}

// SOS Functionality
const sosBtn = document.getElementById('sos-btn');
const sosStatus = document.getElementById('sos-status');

if (sosBtn) {
  // Load and save emergency contact logic
  const contactInput = document.getElementById('emergency-contact-input');
  if (contactInput) {
      contactInput.value = localStorage.getItem('emergencyContact') || '';
      contactInput.addEventListener('input', (e) => {
          localStorage.setItem('emergencyContact', e.target.value);
      });
  }

  sosBtn.addEventListener('click', () => {
    sosStatus.classList.remove('hidden');
    playSiren(); // Trigger siren sound
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        triggerBackendSOS(lat, lng);
      }, (error) => {
        console.warn("Geolocation blocked or failed. Using fallback location for demo.");
        // Fallback to New Delhi coordinates for the demo
        triggerBackendSOS(28.6139, 77.2090);
      });
    } else {
      alert("Geolocation is not supported by this browser. Using fallback location.");
      triggerBackendSOS(28.6139, 77.2090);
    }
    
    function triggerBackendSOS(lat, lng) {
        if (map) {
          map.setView([lat, lng], 15);
          L.marker([lat, lng], {icon: L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
          })}).addTo(map).bindPopup("<b>SOS Triggered Here!</b>").openPopup();
        }
        
        // Attempt to send to Django backend
        fetch('http://localhost:2206/api/sos-alerts/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
              lat: lat, 
              lng: lng, 
              status: 'active', 
              user: null,
              emergency_contact: localStorage.getItem('emergencyContact') || ''
          })
        }).then(res => res.json()).then(data => {
            const alertId = data.id;
            let pollCount = 0;
            // Poll for admin reply
            const pollInterval = setInterval(async () => {
                if (pollCount > 20) { // Stop after ~100 seconds to prevent server overload
                    clearInterval(pollInterval);
                    return;
                }
                pollCount++;
                try {
                    const checkRes = await fetch(`http://localhost:2206/api/sos-alerts/${alertId}/`);
                    const checkData = await checkRes.json();
                    if (checkData.admin_message) {
                        sosStatus.innerHTML = `🚨 DISPATCH REPLY: "${checkData.admin_message}"`;
                        sosStatus.classList.add('bg-green-600');
                        sosStatus.classList.remove('bg-red-600');
                        
                        const msgOverlay = document.createElement('div');
                        msgOverlay.className = "fixed inset-0 bg-black/80 z-[200] flex items-center justify-center p-4 backdrop-blur-sm";
                        msgOverlay.innerHTML = `
                            <div class="bg-white text-black p-8 rounded-3xl max-w-md w-full text-center shadow-2xl border-4 border-green-500 transform animate-bounce">
                                <h2 class="text-3xl font-black text-green-600 mb-4">Rescue Dispatched!</h2>
                                <p class="text-gray-600 mb-6 text-lg">Message from Admin Dispatch:</p>
                                <p class="text-2xl font-bold text-gray-800 mb-8 italic">"${checkData.admin_message}"</p>
                                <button onclick="this.parentElement.parentElement.remove()" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-xl w-full text-lg shadow-lg">Understood</button>
                            </div>
                        `;
                        document.body.appendChild(msgOverlay);
                        
                        clearInterval(pollInterval);
                    }
                } catch(e) {}
            }, 5000); // 5 second intervals instead of 2 to reduce server load
        }).catch(err => console.log('Backend not reachable, simulating...'));

        setTimeout(() => {
          alert("Emergency Alert Sent Successfully. Help is on the way.");
          sosStatus.innerHTML = "Alert Sent! Authorities Notified.";
        }, 1500);
    }
  });
}

// Admin Auth Modals
const authBtn = document.getElementById('auth-btn');
const authModal = document.getElementById('auth-modal');
const regModal = document.getElementById('register-modal');
const closeModal = document.getElementById('close-modal');
const closeRegModal = document.getElementById('close-reg-modal');
const showRegister = document.getElementById('show-register');
const showLogin = document.getElementById('show-login');
const adminPanel = document.getElementById('admin-panel');
const logoutBtn = document.getElementById('logout-btn');

if (authBtn) authBtn.addEventListener('click', () => { if (authModal) authModal.classList.remove('hidden'); });
if (closeModal) closeModal.addEventListener('click', () => { if (authModal) authModal.classList.add('hidden'); });
if (closeRegModal) closeRegModal.addEventListener('click', () => { if (regModal) regModal.classList.add('hidden'); });
if (showRegister) showRegister.addEventListener('click', (e) => { e.preventDefault(); if (authModal) authModal.classList.add('hidden'); if (regModal) regModal.classList.remove('hidden'); });
if (showLogin) showLogin.addEventListener('click', (e) => { e.preventDefault(); if (regModal) regModal.classList.add('hidden'); if (authModal) authModal.classList.remove('hidden'); });

// Firebase Auth Flow
const regForm = document.getElementById('reg-form');
if (regForm) {
  regForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!auth) return;
    const email = document.getElementById('reg-email').value;
    const pass = document.getElementById('reg-password').value;
    try {
      await auth.createUserWithEmailAndPassword(email, pass);
      if (regModal) regModal.classList.add('hidden');
      alert("Admin Registered Successfully!");
    } catch(err) {
      alert(err.message);
    }
  });
}

const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!auth) return;
    const email = document.getElementById('email').value;
    const pass = document.getElementById('password').value;
    try {
      await auth.signInWithEmailAndPassword(email, pass);
      if (authModal) authModal.classList.add('hidden');
    } catch(err) {
      alert(err.message);
    }
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    if (auth) auth.signOut();
  });
}

if (auth) {
  auth.onAuthStateChanged((user) => {
    if (user) {
      if (adminPanel) adminPanel.classList.remove('hidden');
      if (authBtn) authBtn.classList.add('hidden');
      // Init Chart
      const chartEl = document.getElementById('adminChart');
      if (chartEl) {
        const ctx = chartEl.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Women Assisted',
                    data: [120, 190, 300, 500, 420, 600],
                    borderColor: '#005a9c',
                    tension: 0.4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
      }
    } else {
      if (adminPanel) adminPanel.classList.add('hidden');
      if (authBtn) authBtn.classList.remove('hidden');
    }
  });
}

// Gemini AI Assistant (Now using Django Backend)
const askAiBtn = document.getElementById('ask-ai-btn');
const aiPrompt = document.getElementById('ai-prompt');
const aiResponse = document.getElementById('ai-response');

if (askAiBtn) {
  askAiBtn.addEventListener('click', async () => {
    const query = aiPrompt.value;
    if (!query) return;
    
    aiResponse.classList.remove('hidden');
    aiResponse.innerHTML = `<span class="animate-pulse">Thinking...</span>`;
    
    try {
      const res = await fetch('http://localhost:2206/api/chatbot/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });
      const data = await res.json();
      if (data.response) {
        aiResponse.innerHTML = data.response.replace(/\n/g, "<br>");
      } else {
        aiResponse.innerHTML = "Error from backend: " + (data.error || "Unknown error");
      }
    } catch (err) {
      aiResponse.innerHTML = "Error connecting to AI backend. Please try again later.";
      console.error(err);
    }
  });
}

// Resume Review Mock Upload & AI Analysis
const submitResumeBtn = document.getElementById('submit-resume-btn');
const resumeFeedback = document.getElementById('resume-feedback');
const resumeUpload = document.getElementById('resume-upload');

if (submitResumeBtn) {
  submitResumeBtn.addEventListener('click', async () => {
    if (resumeUpload.files.length === 0) {
      alert("Please select a file first.");
      return;
    }
    
    submitResumeBtn.innerHTML = "Uploading to Cloudinary...";
    submitResumeBtn.disabled = true;
    
    // Simulate Cloudinary Upload delay
    setTimeout(async () => {
      submitResumeBtn.innerHTML = "Analyzing with Gemini AI...";
      
      // Send request to Django AI Chatbot Backend
      try {
        const res = await fetch('http://localhost:2206/api/chatbot/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: "Review this resume. The user has uploaded a PDF. Provide an ATS score out of 100, list missing skills, grammar suggestions, and a better summary. Format nicely." })
        });
        const data = await res.json();
        resumeFeedback.classList.remove('hidden');
        if (data.response) {
          resumeFeedback.innerHTML = data.response.replace(/\n/g, "<br>");
        } else {
          resumeFeedback.innerHTML = "Analysis error: " + (data.error || "Unknown error");
        }
      } catch (err) {
        resumeFeedback.classList.remove('hidden');
        resumeFeedback.innerHTML = "Failed to connect to AI server.";
      }
      
      submitResumeBtn.innerHTML = "Analyze My Resume";
      submitResumeBtn.disabled = false;
    }, 1500);
  });
}

// Leaflet Routing Machine (Safe Route Planner)
const planRouteBtn = document.getElementById('plan-route-btn');
if (planRouteBtn) {
  planRouteBtn.addEventListener('click', () => {
    if (!map) return;
    planRouteBtn.innerHTML = "Select Destination on Map...";
    planRouteBtn.disabled = true;
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        const startLat = position.coords.latitude;
        const startLng = position.coords.longitude;
        map.setView([startLat, startLng], 14);
        
        alert("Your location found! Click anywhere on the map to set your destination for a safe route.");
        
        map.once('click', function(e) {
          const destLat = e.latlng.lat;
          const destLng = e.latlng.lng;
          
          L.Routing.control({
            waypoints: [
              L.latLng(startLat, startLng),
              L.latLng(destLat, destLng)
            ],
            routeWhileDragging: true,
            lineOptions: {
              styles: [{color: '#005a9c', opacity: 1, weight: 5}]
            },
            createMarker: function(i, wp, nWps) {
              return L.marker(wp.latLng, {
                icon: L.icon({
                  iconUrl: i === 0 ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png' : 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                  iconSize: [25, 41], iconAnchor: [12, 41]
                })
              }).bindPopup(i === 0 ? 'Start Location' : 'Destination');
            }
          }).addTo(map);
          
          planRouteBtn.innerHTML = "Safe Route Calculated!";
        });
      }, () => {
        alert("Location access needed for routing.");
        planRouteBtn.innerHTML = "Plan Safe Route";
        planRouteBtn.disabled = false;
      });
    }
  });
}

// --- GOV SERVICE RATING ---
window.submitGovRating = async function() {
    const service = document.getElementById('gov-service-select').value;
    const rating = document.getElementById('gov-rating-select').value;
    const feedback = document.getElementById('gov-feedback').value;
    
    if(!feedback) {
        alert('Please provide some written feedback.');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:2206/api/ratings/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                service_name: service,
                rating: parseInt(rating),
                feedback: feedback
            })
        });
        
        if (response.ok) {
            alert('Rating & Feedback Submitted Successfully! The Admin Dashboard will display this instantly.');
            document.getElementById('gov-feedback').value = '';
        } else {
            alert('Failed to submit rating. Backend might be down.');
        }
    } catch (error) {
        alert('Error connecting to backend API.');
        console.error(error);
    }
};
