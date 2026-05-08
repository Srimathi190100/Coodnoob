# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Dict, List, Any
import logging

# Local Imports
from models import Booking, Profile, NomadState, TravelPlan
from logic import get_adjustments

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NomadParis")

app = FastAPI(
    title="NomadParis: The Definitive Agentic Hub",
    description="Full-stack, multi-lingual, agentic travel engine for Paris.",
    version="2.3.0"
)

# --- IN-MEMORY DATABASE (SIMULATED FIRESTORE) ---
db: Dict[str, Any] = {
    "profile": Profile(),
    "bookings": {"stay": [], "transit": [], "tickets": [], "dining": []},
    "state": NomadState()
}

@app.post("/api/book/{category}")
async def create_booking(category: str, booking: Booking):
    if category not in db["bookings"]:
        raise HTTPException(status_code=400, detail="Invalid booking category")
    db["bookings"][category].append(booking)
    return {"status": "SUCCESS", "message": f"Confirmed {booking.name} in Cloud Registry."}

@app.post("/api/orchestrate")
async def orchestrate(state: NomadState):
    adjustments = get_adjustments(state)
    return {"active_adjustments": adjustments}

# --- THE DEFINITIVE DASHBOARD ---

def get_dashboard_html() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NomadParis | Definitive Agentic Hub</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,700;1,700&family=JetBrains+Mono&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #D4AF37; --accent: #38bdf8; --bg: #050505;
                --card-bg: rgba(255, 255, 255, 0.02); --glass: rgba(255, 255, 255, 0.05);
                --text: #FDFCFB; --text-muted: #94a3b8; --success: #4ade80; --error: #f87171;
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; overflow-x: hidden; }
            
            /* Navbar */
            .navbar { padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 1000; }
            .logo { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: var(--primary); text-decoration: none; }
            
            .lang-switcher { display: flex; gap: 0.5rem; }
            .lang-btn { background: var(--glass); border: 1px solid rgba(255,255,255,0.1); color: var(--text); padding: 0.3rem 0.6rem; border-radius: 0.4rem; cursor: pointer; font-size: 0.7rem; transition: 0.3s; }
            .lang-btn.active { background: var(--primary); color: var(--bg); border-color: var(--primary); }

            /* Grid Layout */
            .container { padding: 2rem 5%; display: grid; grid-template-columns: 380px 1fr 380px; gap: 2rem; max-width: 1800px; margin: 0 auto; width: 100%; }
            .panel { background: var(--card-bg); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 1.25rem; padding: 1.5rem; backdrop-filter: blur(20px); height: fit-content; transition: 0.3s; }
            .panel:hover { border-color: rgba(212, 175, 55, 0.2); }
            
            h2 { font-family: 'Playfair Display', serif; font-size: 1.2rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; }
            h2 span { font-size: 0.6rem; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; background: rgba(212,175,55,0.1); padding: 0.2rem 0.5rem; border-radius: 1rem; }

            /* Interactive Components */
            .btn-action { width: 100%; padding: 0.8rem; background: var(--primary); color: var(--bg); border: none; border-radius: 0.75rem; font-weight: 700; cursor: pointer; transition: 0.3s; margin-top: 1rem; font-size: 0.8rem; }
            .btn-action:hover { background: #b8962e; transform: translateY(-2px); }
            
            .control-group { margin-bottom: 1.2rem; }
            .control-group label { display: block; font-size: 0.7rem; color: var(--text-muted); margin-bottom: 0.4rem; }
            input[type="range"] { width: 100%; accent-color: var(--primary); }

            .hub-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
            .hub-item { background: var(--glass); border-radius: 0.75rem; padding: 0.8rem; text-align: center; cursor: pointer; border: 1px solid transparent; transition: 0.3s; font-size: 0.8rem; }
            .hub-item:hover { border-color: var(--primary); background: rgba(212, 175, 55, 0.05); }

            .map-container { width: 100%; height: 200px; border-radius: 1rem; overflow: hidden; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); filter: grayscale(1) invert(0.9); }
            
            .log-console { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--success); height: 180px; overflow-y: auto; background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 0.75rem; border: 1px solid rgba(255,255,255,0.05); }
            .log-entry { margin-bottom: 0.3rem; opacity: 0.8; }
            .log-entry.error { color: var(--error); }
            .log-entry.action { color: var(--accent); }

            .wallet-item { padding: 0.6rem; background: rgba(74, 222, 128, 0.05); border-left: 2px solid var(--success); border-radius: 0.4rem; font-size: 0.7rem; margin-bottom: 0.5rem; animation: fadeIn 0.3s ease; }
            @keyframes fadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

            /* Google Agent */
            .agent-bubble { position: fixed; bottom: 2rem; right: 2rem; width: 60px; height: 60px; background: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 2000; transition: 0.3s; }
            .agent-panel { position: fixed; bottom: 6.5rem; right: 2rem; width: 350px; background: #0a0a0a; border: 1px solid var(--primary); border-radius: 1.5rem; padding: 1.5rem; display: none; z-index: 2000; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
            .agent-panel.active { display: block; animation: slideUp 0.3s ease; }
            @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            .suggestion-card { background: var(--glass); border-radius: 0.75rem; padding: 1rem; margin-top: 1rem; border-left: 3px solid var(--accent); }

            @media (max-width: 1200px) { .container { grid-template-columns: 1fr; } .agent-panel { width: calc(100% - 4rem); left: 2rem; } }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <a href="/" class="logo">NomadParis</a>
            <div class="lang-switcher">
                <button id="btn-en" class="lang-btn active" onclick="setLang('en')">EN</button>
                <button id="btn-fr" class="lang-btn" onclick="setLang('fr')">FR</button>
                <button id="btn-es" class="lang-btn" onclick="setLang('es')">ES</button>
            </div>
        </nav>

        <main class="container">
            <!-- LEFT: State & Hub -->
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <section class="panel">
                    <h2 id="title-cockpit">Nomad Cockpit <span>Live</span></h2>
                    <div class="control-group">
                        <label id="lbl-budget">Budget Remaining: <span id="budgetVal">85</span>%</label>
                        <input type="range" id="budgetRange" min="0" max="100" value="85" oninput="updateState()">
                    </div>
                    <div class="control-group">
                        <label id="lbl-rain">Environment Override</label>
                        <button class="btn-action" id="rainBtn" style="background: var(--glass); color: var(--text); margin-top:0;" onclick="toggleRain()">No Rain</button>
                    </div>
                </section>

                <section class="panel">
                    <h2 id="title-hub">Travel Hub <span>Booking</span></h2>
                    <div class="hub-grid">
                        <div class="hub-item" onclick="showCategory('stay')">🏨 Stay</div>
                        <div class="hub-item" onclick="showCategory('transit')">🚕 Transit</div>
                        <div class="hub-item" onclick="showCategory('tickets')">🎟 Tickets</div>
                        <div class="hub-item" onclick="showCategory('dining')">🍴 Dining</div>
                    </div>
                    <div id="hubOptions" style="margin-top:1.2rem; font-size: 0.8rem;"></div>
                </section>
            </div>

            <!-- MIDDLE: Orchestrator -->
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <section class="panel" style="flex: 1;">
                    <h2 id="title-map">Agentic Monitoring <span>Live Map</span></h2>
                    <div class="map-container">
                        <iframe width="100%" height="100%" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2624.2158!2d2.285!3d48.86!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDjCsDUxJzM2LjAiTiAywrAxNycwNi4wIkU!5e0!3m2!1sen!2sfr!4v1620000000000!5m2!1sen!2sfr" loading="lazy"></iframe>
                    </div>
                    <div class="log-console" id="logConsole">
                        <div class="log-entry">[INFO] Engine initializing...</div>
                        <div class="log-entry">[INFO] Multi-Language Pack Loaded.</div>
                    </div>
                    <button class="btn-action" id="btn-heal" style="background: var(--error); color: var(--text); border:none;" onclick="simulateConflict()">Simulate Louvre Conflict</button>
                </section>

                <section class="panel" id="advicePanel" style="display:none;">
                    <h2 id="title-guidance">Engine Guidance <span>Real-time</span></h2>
                    <div id="adviceContent" style="font-size: 0.85rem;"></div>
                </section>
            </div>

            <!-- RIGHT: Wallet & Profile -->
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <section class="panel">
                    <h2 id="title-wallet">Nomad Wallet <span>Sync</span></h2>
                    <div id="walletList" style="min-height: 100px;">
                        <p style="text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-top: 2rem;">No bookings yet.</p>
                    </div>
                </section>

                <section class="panel">
                    <h2 id="title-neural">Neural Weights <span>GCloud</span></h2>
                    <div style="font-size: 0.7rem; display: flex; flex-direction: column; gap: 0.8rem;">
                        <div>
                            <label>Culture Bias</label>
                            <div style="height:4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top:4px;"><div style="width: 75%; height: 100%; background: var(--primary);"></div></div>
                        </div>
                        <div>
                            <label>Food Bias</label>
                            <div style="height:4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top:4px;"><div style="width: 40%; height: 100%; background: var(--accent);"></div></div>
                        </div>
                    </div>
                    <button class="btn-action" id="btn-sync">Sync Google Account</button>
                </section>
            </div>
        </main>

        <!-- Floating Agent -->
        <div class="agent-bubble" onclick="toggleAgent()">
            <svg viewBox="0 0 24 24" width="30" height="30"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
        </div>
        <div class="agent-panel" id="agentPanel">
            <h3 style="color: var(--primary); font-family: 'Playfair Display';" id="agent-title">Google AI Suggestion</h3>
            <div id="agentSuggestions">
                <div class="suggestion-card">
                    <h4>Nuage Café (Hidden Gem)</h4>
                    <p>Quiet focus zone in the 5th arrondissement. 5G speed verified.</p>
                </div>
            </div>
            <button class="btn-action" onclick="toggleAgent()">Close</button>
        </div>

        <script>
            let state = { budget_remaining_pct: 85, aqi: 45, rain: false, high_workload: false, emergency: false };
            let currentLang = 'en';

            const trans = {
                en: { cockpit: "Nomad Cockpit", hub: "Travel Hub", map: "Agentic Map", wallet: "Nomad Wallet", neural: "Neural Weights", guidance: "Engine Guidance", budget: "Budget Remaining", sync: "Sync Google Account", heal: "Simulate Louvre Conflict", agent: "Google AI Suggestion" },
                fr: { cockpit: "Poste de Pilotage", hub: "Centre de Voyage", map: "Carte Agentique", wallet: "Portefeuille", neural: "Poids Neuraux", guidance: "Conseils Moteur", budget: "Budget Restant", sync: "Sync Compte Google", heal: "Simuler Conflit Louvre", agent: "Suggestion Google AI" },
                es: { cockpit: "Cabina de Mando", hub: "Centro de Viajes", map: "Mapa Agéntico", wallet: "Billetera Nomad", neural: "Pesos Neurales", guidance: "Guía del Motor", budget: "Presupuesto Restante", sync: "Sync Cuenta Google", heal: "Simular Conflicto Louvre", agent: "Sugerencia Google AI" }
            };

            const options = {
                stay: [{name: "Shangri-La Paris", price: "€1,200"}, {name: "Brach Paris", price: "€650"}],
                transit: [{name: "Uber Black", price: "€75.00"}, {name: "G7 Taxi", price: "€56.00"}],
                tickets: [{name: "Louvre Skip-the-Line", price: "€22.00"}, {name: "Eiffel Summit", price: "€28.00"}],
                dining: [{name: "Chez Janou", price: "€45 Avg"}, {name: "Breizh Café", price: "€18 Avg"}]
            };

            function setLang(lang) {
                currentLang = lang;
                document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
                document.getElementById('btn-' + lang).classList.add('active');
                
                document.getElementById('title-cockpit').innerHTML = trans[lang].cockpit + ' <span>Live</span>';
                document.getElementById('title-hub').innerHTML = trans[lang].hub + ' <span>Booking</span>';
                document.getElementById('title-map').innerHTML = trans[lang].map + ' <span>Live Map</span>';
                document.getElementById('title-wallet').innerHTML = trans[lang].wallet + ' <span>Sync</span>';
                document.getElementById('title-neural').innerHTML = trans[lang].neural + ' <span>GCloud</span>';
                document.getElementById('title-guidance').innerHTML = trans[lang].guidance + ' <span>Real-time</span>';
                document.getElementById('lbl-budget').innerHTML = trans[lang].budget + ': <span id="budgetVal">'+state.budget_remaining_pct+'</span>%';
                document.getElementById('btn-sync').innerText = trans[lang].sync;
                document.getElementById('btn-heal').innerText = trans[lang].heal;
                document.getElementById('agent-title').innerText = trans[lang].agent;
            }

            function addLog(msg, type='info') {
                const console = document.getElementById('logConsole');
                const time = new Date().toLocaleTimeString([], {hour12: false});
                const div = document.createElement('div');
                div.className = `log-entry ${type}`;
                div.innerText = `[${time}] ${msg}`;
                console.prepend(div);
            }

            async function updateState() {
                state.budget_remaining_pct = parseInt(document.getElementById('budgetRange').value);
                document.getElementById('budgetVal').innerText = state.budget_remaining_pct;
                
                const response = await fetch('/api/orchestrate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(state)
                });
                const data = await response.json();
                renderAdvice(data.active_adjustments);
            }

            function toggleRain() {
                state.rain = !state.rain;
                const btn = document.getElementById('rainBtn');
                btn.innerText = state.rain ? "Rain Detected" : "No Rain";
                btn.style.color = state.rain ? "var(--accent)" : "var(--text)";
                updateState();
            }

            function renderAdvice(adjustments) {
                const panel = document.getElementById('advicePanel');
                const content = document.getElementById('adviceContent');
                if (adjustments.length === 0) { panel.style.display = 'none'; return; }
                panel.style.display = 'block';
                content.innerHTML = adjustments.map(adj => `<div style="background:rgba(255,255,255,0.03); padding:0.8rem; border-radius:0.5rem; margin-bottom:0.5rem;"><strong>${adj.variable.toUpperCase()}</strong>: ${adj.adjustment.transportation || adj.adjustment.itinerary || adj.adjustment.logistics}</div>`).join('');
            }

            function showCategory(cat) {
                const container = document.getElementById('hubOptions');
                container.innerHTML = options[cat].map(opt => `<div style="display:flex; justify-content:space-between; align-items:center; background:var(--glass); padding:0.6rem; border-radius:0.5rem; margin-bottom:0.4rem;"><span>${opt.name}</span><button class="btn-action" style="width:auto; margin:0; padding:0.3rem 0.6rem; font-size:0.6rem;" onclick="book('${cat}', '${opt.name}', '${opt.price}')">Book</button></div>`).join('');
            }

            async function book(cat, name, price) {
                addLog(`Booking ${name}...`, 'action');
                const response = await fetch(`/api/book/${cat}`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({name, price}) });
                const res = await response.json();
                addLog(`Firestore: ${res.message}`, 'success');
                updateWallet(cat, name);
            }

            function updateWallet(cat, name) {
                const list = document.getElementById('walletList');
                if (list.innerText.includes('No bookings')) list.innerHTML = '';
                const div = document.createElement('div');
                div.className = 'wallet-item';
                div.innerHTML = `<strong>${name}</strong> (${cat.toUpperCase()})`;
                list.prepend(div);
            }

            async function simulateConflict() {
                addLog("ALERT: Louvre Closure Detected.", "error");
                addLog("Initiating Self-Healing...", "action");
                await new Promise(r => setTimeout(r, 1200));
                addLog("Success: Rerouted to Orsay.", "success");
                updateWallet('tickets', "Orsay (Healed)");
            }

            function toggleAgent() { document.getElementById('agentPanel').classList.toggle('active'); }

            // Init
            addLog("System Online. Standing by.");
        </script>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def root():
    return get_dashboard_html()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
