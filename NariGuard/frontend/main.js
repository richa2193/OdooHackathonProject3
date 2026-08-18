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

// Unified API Fetch Helper (Supports Localhost, PythonAnywhere, and Production domains)
async function apiFetch(path, options = {}) {
  const relPath = path.startsWith('/') ? path : '/' + path;
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const urlsToTry = isLocal
    ? [`http://localhost:8000${relPath}`, relPath, `http://${window.location.host}${relPath}`]
    : [relPath, `http://localhost:8000${relPath}`];
  
  let lastErr = null;
  for (const url of urlsToTry) {
    try {
      const res = await fetch(url, options);
      if (res && res.status !== 404) return res;
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr || new Error(`Failed to fetch API from ${path}`);
}

// Theme Toggling
const htmlTag = document.documentElement;

function toggleTheme() {
  const themeIconLights = document.querySelectorAll('#theme-icon-light');
  const themeIconDarks = document.querySelectorAll('#theme-icon-dark');
  if (htmlTag.classList.contains('dark')) {
    htmlTag.classList.remove('dark');
    localStorage.setItem('theme', 'light');
    themeIconDarks.forEach(el => el.classList.remove('hidden'));
    themeIconLights.forEach(el => el.classList.add('hidden'));
  } else {
    htmlTag.classList.add('dark');
    localStorage.setItem('theme', 'dark');
    themeIconLights.forEach(el => el.classList.remove('hidden'));
    themeIconDarks.forEach(el => el.classList.add('hidden'));
  }
}

// On load, check localStorage for Dark Mode
if (localStorage.getItem('theme') === 'dark') {
  htmlTag.classList.add('dark');
  document.querySelectorAll('#theme-icon-light').forEach(el => el.classList.remove('hidden'));
  document.querySelectorAll('#theme-icon-dark').forEach(el => el.classList.add('hidden'));
}

// Color Theme Switcher Logic
const themes = ['theme-purple', 'theme-blue', 'theme-green'];

function applyColorTheme(themeClass) {
  document.body.classList.remove(...themes);
  document.body.classList.add(themeClass);
  localStorage.setItem('colorTheme', themeClass);
}

let currentThemeIndex = themes.indexOf(localStorage.getItem('colorTheme') || 'theme-purple');
if (currentThemeIndex === -1) currentThemeIndex = 0;
applyColorTheme(themes[currentThemeIndex]);

// Attach event listeners to all theme buttons on page
document.querySelectorAll('#color-cycle-btn, .color-cycle-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    currentThemeIndex = (currentThemeIndex + 1) % themes.length;
    applyColorTheme(themes[currentThemeIndex]);
  });
});

document.querySelectorAll('#theme-toggle, .theme-toggle').forEach(btn => {
  btn.addEventListener('click', toggleTheme);
});

// Helper for standalone Vector SVG Leaflet icons (no external URL dependencies)
function createSvgIcon(color = 'blue', type = 'pin') {
  let innerSvg = '';
  if (type === 'police') {
    innerSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="16" height="16"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-1 6h2v2h-2V7zm0 4h2v6h-2v-6z"/></svg>`;
  } else if (type === 'hospital') {
    innerSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="16" height="16"><path d="M19 10.5h-5.5V5h-3v5.5H5v3h5.5V19h3v-5.5H19v-3z"/></svg>`;
  } else if (type === 'user') {
    innerSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="16" height="16"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>`;
  } else {
    innerSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="16" height="16"><circle cx="12" cy="12" r="6"/></svg>`;
  }

  const bgColors = {
    blue: '#2563eb',
    green: '#16a34a',
    red: '#ef4444',
    purple: '#9333ea'
  };
  const bg = bgColors[color] || '#2563eb';

  return L.divIcon({
    className: 'custom-vector-marker',
    html: `
      <div style="
        background-color: ${bg};
        width: 32px;
        height: 32px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        border: 2px solid #ffffff;
      ">
        <div style="transform: rotate(45deg); display: flex; align-items: center; justify-content: center;">
          ${innerSvg}
        </div>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  });
}

// Map Initialization
let map;
let markersLayer = L.layerGroup();

function initMap() {
  if (document.getElementById('map')) {
    if (typeof L !== 'undefined') {
      if (L.Icon && L.Icon.Default) {
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
          iconRetinaUrl: '',
          iconUrl: '',
          shadowUrl: ''
        });
      }
      if (L.Marker && L.Marker.prototype) {
        L.Marker.prototype.options.icon = createSvgIcon('purple', 'pin');
      }
    }
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
const findNearbyBtns = document.querySelectorAll('#find-nearby-btn, .find-nearby-btn');

function loadNearbySpots(lat, lng) {
  if (!map) return;
  map.setView([lat, lng], 14);
  markersLayer.clearLayers();
  L.marker([lat, lng], {icon: createSvgIcon('red', 'user')}).addTo(markersLayer).bindPopup("<b>You are here</b>").openPopup();

  const overpassQuery = `
    [out:json];
    (
      node["amenity"="police"](around:3000,${lat},${lng});
      node["amenity"="hospital"](around:3000,${lat},${lng});
    );
    out body;
  `;

  fetch('https://overpass-api.de/api/interpreter', {
    method: 'POST',
    body: overpassQuery
  }).then(r => r.json()).then(data => {
    const validNodes = (data.elements || []).filter(el => el.lat && el.lon).slice(0, 20);
    if (validNodes.length === 0) throw new Error("No nodes");
    validNodes.forEach(el => {
      let isPolice = el.tags && el.tags.amenity === 'police';
      let type = isPolice ? 'Police Station' : 'Hospital';
      let name = (el.tags && el.tags.name) ? el.tags.name : ('Unknown ' + type);
      let customIcon = createSvgIcon(isPolice ? 'blue' : 'green', isPolice ? 'police' : 'hospital');
      L.marker([el.lat, el.lon], {icon: customIcon}).addTo(markersLayer).bindPopup(`<b>${name}</b><br>${type}`);
    });
    findNearbyBtns.forEach(b => b.innerHTML = 'Find Safe Spots');
  }).catch(err => {
    console.warn("Using simulated safe spots for demo.");
    L.marker([lat + 0.012, lng + 0.015], {icon: createSvgIcon('blue', 'police')}).addTo(markersLayer).bindPopup(`<b>Central Police Station</b><br>Police Station`);
    L.marker([lat - 0.010, lng - 0.008], {icon: createSvgIcon('green', 'hospital')}).addTo(markersLayer).bindPopup(`<b>City General Hospital</b><br>Hospital`);
    findNearbyBtns.forEach(b => b.innerHTML = 'Find Safe Spots');
  });
}

findNearbyBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    findNearbyBtns.forEach(b => b.innerHTML = 'Searching...');
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => loadNearbySpots(pos.coords.latitude, pos.coords.longitude),
        err => {
          console.warn("Geolocation fallback to demo coordinates.");
          loadNearbySpots(28.6139, 77.2090);
        },
        { timeout: 5000 }
      );
    } else {
      loadNearbySpots(28.6139, 77.2090);
    }
  });
});

// Siren Sound using HTML5 Audio
function playSiren() {
  try {
    const sirenAudio = new Audio('./siren.mp3');
    sirenAudio.volume = 1.0;
    sirenAudio.loop = true;
    sirenAudio.play().catch(e => {
      console.log("Audio play blocked by browser:", e);
      alert("SOS Triggered! (Audio blocked by browser, please click allow)");
    });
    
    setTimeout(() => {
      sirenAudio.pause();
      sirenAudio.currentTime = 0;
    }, 10000);
  } catch (err) {
    console.error("Audio trigger failed:", err);
  }
}

// SOS Functionality
const sosBtns = document.querySelectorAll('#sos-btn, .sos-btn');
const sosStatuses = document.querySelectorAll('#sos-status, .sos-status');

sosBtns.forEach(btn => {
  const contactInput = document.getElementById('emergency-contact-input');
  if (contactInput) {
    contactInput.value = localStorage.getItem('emergencyContact') || '';
    contactInput.addEventListener('input', (e) => {
      localStorage.setItem('emergencyContact', e.target.value);
    });
  }

  btn.addEventListener('click', () => {
    sosStatuses.forEach(s => s.classList.remove('hidden'));
    playSiren();
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => triggerBackendSOS(position.coords.latitude, position.coords.longitude),
        error => triggerBackendSOS(28.6139, 77.2090),
        { timeout: 5000 }
      );
    } else {
      triggerBackendSOS(28.6139, 77.2090);
    }
  });
});

function triggerBackendSOS(lat, lng) {
  if (map) {
    map.setView([lat, lng], 15);
    L.marker([lat, lng], {icon: createSvgIcon('red', 'user')}).addTo(map).bindPopup("<b>SOS Triggered Here!</b>").openPopup();
  }
  
  apiFetch('/api/sos-alerts/', {
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
      const pollInterval = setInterval(() => {
          pollCount++;
          if (pollCount > 30) clearInterval(pollInterval);
          
          apiFetch(`/api/sos-alerts/${alertId}/`)
              .then(r => r.json())
              .then(alertData => {
                  if (alertData.admin_message) {
                      clearInterval(pollInterval);
                      showAdminReplyBanner(alertData.admin_message);
                  }
              }).catch(e => console.log(e));
      }, 3000);
  }).catch(err => {
      console.warn("Backend API unavailable for SOS trigger:", err);
  });
}

function showAdminReplyBanner(msg) {
  const existing = document.getElementById('admin-reply-banner');
  if (existing) existing.remove();
  
  const banner = document.createElement('div');
  banner.id = 'admin-reply-banner';
  banner.className = 'fixed bottom-6 right-6 z-50 bg-green-600 text-white p-6 rounded-2xl shadow-2xl max-w-md border-2 border-white animate-bounce';
  banner.innerHTML = `
      <h3 class="font-black text-xl mb-1 flex items-center gap-2">🚨 EMERGENCY RESPONSE</h3>
      <p class="font-bold text-lg leading-snug">${msg}</p>
      <div class="mt-4 flex justify-end">
          <button onclick="this.parentElement.parentElement.remove()" class="bg-white text-green-700 px-4 py-2 rounded-xl font-bold text-sm hover:bg-gray-100">Dismiss</button>
      </div>
  `;
  document.body.appendChild(banner);
}

// Authentication Modals
const authBtn = document.getElementById('auth-btn');
const authModal = document.getElementById('auth-modal');
const regModal = document.getElementById('reg-modal');
const closeModal = document.getElementById('close-modal');
const closeRegModal = document.getElementById('close-reg-modal');
const showRegister = document.getElementById('show-register');
const showLogin = document.getElementById('show-login');
const regForm = document.getElementById('reg-form');
const loginForm = document.getElementById('login-form');
const logoutBtn = document.getElementById('logout-btn');
const adminPanel = document.getElementById('admin-panel');

if (authBtn) authBtn.addEventListener('click', () => { if (authModal) authModal.classList.remove('hidden'); });
if (closeModal) closeModal.addEventListener('click', () => { if (authModal) authModal.classList.add('hidden'); });
if (closeRegModal) closeRegModal.addEventListener('click', () => { if (regModal) regModal.classList.add('hidden'); });
if (showRegister) showRegister.addEventListener('click', (e) => { e.preventDefault(); if (authModal) authModal.classList.add('hidden'); if (regModal) regModal.classList.remove('hidden'); });
if (showLogin) showLogin.addEventListener('click', (e) => { e.preventDefault(); if (regModal) regModal.classList.add('hidden'); if (authModal) authModal.classList.remove('hidden'); });

if (regForm) {
  regForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('reg-email').value;
    const pass = document.getElementById('reg-pass').value;
    try {
      if (auth) await auth.createUserWithEmailAndPassword(email, pass);
      alert('Registered Successfully!');
      if (regModal) regModal.classList.add('hidden');
    } catch (err) {
      alert(err.message);
    }
  });
}

if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const pass = document.getElementById('login-pass').value;
    try {
      if (auth) await auth.signInWithEmailAndPassword(email, pass);
      alert('Logged In Successfully!');
      if (authModal) authModal.classList.add('hidden');
    } catch (err) {
      alert(err.message);
    }
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    if (auth) auth.signOut();
  });
}

// Gemini AI Assistant
const askAiBtns = document.querySelectorAll('#ask-ai-btn, .ask-ai-btn');
const aiPrompts = document.querySelectorAll('#ai-prompt, .ai-prompt');
const aiResponses = document.querySelectorAll('#ai-response, .ai-response');

async function handleAiQuery() {
  let query = '';
  aiPrompts.forEach(p => { if (p.value) query = p.value; });
  if (!query) {
    alert("Please type a question or prompt first.");
    return;
  }
  
  aiResponses.forEach(r => {
    r.classList.remove('hidden');
    r.innerHTML = `<span class="animate-pulse">Thinking...</span>`;
  });

async function handleAiQuery() {
  let query = '';
  aiPrompts.forEach(p => { if (p.value) query = p.value; });
  if (!query) {
    alert("Please type a question or prompt first.");
    return;
  }
  
  aiResponses.forEach(r => {
    r.classList.remove('hidden');
    r.innerHTML = `<span class="animate-pulse">Thinking...</span>`;
  });

  try {
    const res = await apiFetch('/api/chatbot/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query })
    });
    const data = await res.json();
    aiResponses.forEach(r => {
      if (data.response) {
        r.innerHTML = data.response.replace(/\n/g, "<br>");
      } else {
        r.innerHTML = "Error from backend: " + (data.error || "Unknown error");
      }
    });
  } catch (err) {
    aiResponses.forEach(r => {
      r.innerHTML = "Error connecting to AI backend. Please try again later.";
    });
  }
}

askAiBtns.forEach(btn => {
  btn.addEventListener('click', handleAiQuery);
});

aiPrompts.forEach(p => {
  p.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAiQuery();
    }
  });
});

// Resume Review Mock Upload & AI Analysis
const submitResumeBtns = document.querySelectorAll('#submit-resume-btn, .submit-resume-btn');
const resumeFeedback = document.getElementById('resume-feedback');
const resumeUpload = document.getElementById('resume-upload');

submitResumeBtns.forEach(btn => {
  btn.addEventListener('click', async () => {
    if (resumeUpload && resumeUpload.files.length === 0) {
      alert("Please select a file first.");
      return;
    }
    
    btn.innerHTML = "Uploading to Cloudinary...";
    btn.disabled = true;
    
    setTimeout(async () => {
      btn.innerHTML = "Analyzing with Gemini AI...";
      try {
        const res = await apiFetch('/api/chatbot/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: "Review this resume. The user has uploaded a PDF. Provide an ATS score out of 100, list missing skills, grammar suggestions, and a better summary. Format nicely." })
        });
        const data = await res.json();
        if (resumeFeedback) {
          resumeFeedback.classList.remove('hidden');
          if (data.response) {
            resumeFeedback.innerHTML = data.response.replace(/\n/g, "<br>");
          } else {
            resumeFeedback.innerHTML = "Analysis error: " + (data.error || "Unknown error");
          }
        }
      } catch (err) {
        if (resumeFeedback) {
          resumeFeedback.classList.remove('hidden');
          resumeFeedback.innerHTML = "Failed to connect to AI server.";
        }
      }
      btn.innerHTML = "Analyze My Resume";
      btn.disabled = false;
    }, 1500);
  });
});

// Leaflet Routing Machine (Safe Route Planner)
const planRouteBtns = document.querySelectorAll('#plan-route-btn, .plan-route-btn');

planRouteBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    if (!map) return;
    btn.innerHTML = "Select Destination on Map...";
    btn.disabled = true;
    
    function enableRouting(startLat, startLng) {
      map.setView([startLat, startLng], 14);
      alert("Your location found! Click anywhere on the map to set your destination for a safe route.");
      map.once('click', function(e) {
        const destLat = e.latlng.lat;
        const destLng = e.latlng.lng;
        
        if (window.currentRouteControl) {
          map.removeControl(window.currentRouteControl);
        }
        
        window.currentRouteControl = L.Routing.control({
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
              icon: createSvgIcon(i === 0 ? 'green' : 'red', i === 0 ? 'user' : 'pin')
            }).bindPopup(i === 0 ? 'Start Location' : 'Destination');
          }
        }).addTo(map);
        
        btn.innerHTML = "Safe Route Calculated!";
        btn.disabled = false;
      });
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => enableRouting(pos.coords.latitude, pos.coords.longitude),
        err => {
          console.warn("Location access fallback to Delhi for demo routing.");
          enableRouting(28.6139, 77.2090);
        },
        { timeout: 5000 }
      );
    } else {
      enableRouting(28.6139, 77.2090);
    }
  });
});

// --- GOV SERVICE RATING ---
window.submitGovRating = async function() {
    const serviceEl = document.getElementById('gov-service-select');
    const ratingEl = document.getElementById('gov-rating-select');
    const feedbackEl = document.getElementById('gov-feedback');
    
    const service = serviceEl ? serviceEl.value : 'General Safety';
    const rating = ratingEl ? ratingEl.value : '5';
    const feedback = feedbackEl ? feedbackEl.value : '';
    
    if(!feedback) {
        alert('Please provide some written feedback.');
        return;
    }
    
    try {
        const response = await apiFetch('/api/ratings/', {
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
            if (feedbackEl) feedbackEl.value = '';
        } else {
            alert('Failed to submit rating. Backend might be down.');
        }
    } catch (error) {
        alert('Error connecting to backend API.');
        console.error(error);
    }
};
