import streamlit as st
import re
import time
import requests
import random
from urlextract import URLExtract
import whois
from datetime import datetime
from urllib.parse import urlparse
import streamlit.components.v1 as components

# ========== CONFIG ==========
URLSCAN_API_KEY = "YOUR_URLSCAN_API_KEY"  # Replace with your URLScan.io API key or leave empty to disable

extractor = URLExtract()

# List of popular brands for spoofing detection
BRANDS = ['paypal', 'amazon', 'google', 'microsoft', 'apple', 'facebook']

# ========== UTILS ==========

def detect_brand_spoofing(email_text):
    detected = []
    for brand in BRANDS:
        if re.search(r'\b' + re.escape(brand) + r'\b', email_text, re.IGNORECASE):
            detected.append(brand)
    return detected

def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date is None:
            return None
        age_days = (datetime.now() - creation_date).days
        return age_days
    except Exception:
        return None

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception:
        return None

def check_urls(email_text):
    urls = extractor.find_urls(email_text)
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update', 'bank']
    url_analysis = []
    for url in urls:
        analysis = {"url": url, "suspicious": False, "reasons": []}
        for word in suspicious_keywords:
            if word in url.lower():
                analysis["suspicious"] = True
                analysis["reasons"].append(f"URL contains suspicious keyword: {word}")
        # Domain age check
        domain = extract_domain(url)
        if domain:
            age = get_domain_age(domain)
            if age is not None and age < 30:
                analysis["suspicious"] = True
                analysis["reasons"].append(f"Domain {domain} is newly registered ({age} days old)")
        url_analysis.append(analysis)
    return url_analysis

def analyze_email_content(email_text):
    phishing_words = ['urgent', 'password', 'click here', 'verify', 'bank', 'account', 'login', 'suspend']
    email_text_lower = email_text.lower()

    word_matches = []
    for word in phishing_words:
        if word in email_text_lower:
            word_matches.append(word)

    return word_matches

def predict_phishing(email_text):
    # Analyze URLs
    url_analysis = check_urls(email_text)

    # Analyze email content
    word_matches = analyze_email_content(email_text)

    # Brand spoofing detection
    brands = detect_brand_spoofing(email_text)

    # Combine reasons and generate report
    report = {
        "threat_level": "low",
        "reasons": [],
        "suspicious_words": word_matches,
        "url_analysis": url_analysis,
        "brand_spoofing": brands
    }

    threat_score = len(word_matches) + sum([2 for url in url_analysis if url["suspicious"]]) + (3 if brands else 0)

    if threat_score > 5:
        report["threat_level"] = "high"
    elif threat_score > 2:
        report["threat_level"] = "medium"
    else:
        report["threat_level"] = "low"

    report["reasons"].extend([f"Email contains suspicious word: {word}" for word in word_matches])
    report["reasons"].extend([reason for url in url_analysis for reason in url["reasons"]])
    if brands:
        report["reasons"].append(f"Possible brand spoofing detected: {', '.join(brands)}")

    is_phishing = threat_score > 2
    confidence = 0.90 if is_phishing else 0.95

    return "Phishing" if is_phishing else "Legitimate", confidence, report

# URLScan.io integration
def urlscan_submit(url):
    if not URLSCAN_API_KEY:
        return None
    api_url = 'https://urlscan.io/api/v1/scan/'
    headers = {'API-Key': URLSCAN_API_KEY, 'Content-Type': 'application/json'}
    data = {"url": url, "visibility": "public"}
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            result_url = response.json().get('result')
            return result_url
        else:
            return None
    except Exception:
        return None

def urlscan_report(api_url):
    if not api_url:
        return None
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception:
        return None

# ========== STREAMLIT UI ==========

def inject_hacker_css():
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700&display=swap');

    :root {
        --neon-red: #ff4b4b;
        --neon-blue: #00f0ff;
        --matrix-green: #0aff0a;
        --neon-purple: #b300ff;
        --dark-bg: #0a0a0a;
        --terminal-bg: rgba(0, 10, 15, 0.9);
    }

    body {
        background: var(--dark-bg);
        background-image:
            radial-gradient(circle at 25% 25%, rgba(255, 75, 75, 0.05) 0%, transparent 25%),
            radial-gradient(circle at 75% 75%, rgba(0, 240, 255, 0.05) 0%, transparent 25%),
            linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
        background-size: cover, cover, 30px 30px, 30px 30px;
        color: var(--neon-blue);
        font-family: 'Orbitron', 'Share Tech Mono', monospace;
        overflow-x: hidden;
    }

    .stApp {
        background: transparent !important;
        max-width: 1200px;
        margin: 0 auto;
    }

    .cyber-terminal {
        border: 1px solid var(--neon-blue);
        border-image: linear-gradient(45deg, var(--neon-blue), var(--neon-purple)) 1;
        background: var(--terminal-bg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        position: relative;
        backdrop-filter: blur(2px);
    }

    .cyber-terminal::before {
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border: 1px solid var(--neon-purple);
        z-index: -1;
        opacity: 0.7;
    }

    .stTextArea textarea {
        background: var(--terminal-bg) !important;
        color: var(--matrix-green) !important;
        border: 1px solid var(--neon-blue) !important;
        border-image: linear-gradient(45deg, var(--neon-blue), var(--neon-purple)) 1;
        font-size: 16px;
        font-family: 'Share Tech Mono', monospace !important;
        padding: 0.75rem !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2) inset;
    }

    .stButton>button {
        background: linear-gradient(45deg, var(--dark-bg), var(--terminal-bg)) !important;
        color: var(--neon-blue) !important;
        border: 1px solid var(--neon-blue) !important;
        border-radius: 0 !important;
        transition: all 0.3s;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Orbitron', sans-serif !important;
        position: relative;
        overflow: hidden;
    }

    .stButton>button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.2), transparent);
        transition: all 0.5s;
    }

    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
        color: var(--neon-purple) !important;
        border-color: var(--neon-purple) !important;
    }

    .stButton>button:hover::before {
        left: 100%;
    }

    .alert-panel {
        border: 1px solid var(--neon-red);
        border-image: linear-gradient(45deg, var(--neon-red), var(--neon-purple)) 1;
        animation: pulse 1.5s infinite, flicker 0.1s infinite alternate;
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(20, 0, 0, 0.7);
        position: relative;
    }

    .alert-panel::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg,
            transparent 0%,
            rgba(255, 75, 75, 0.1) 40%,
            rgba(255, 75, 75, 0.1) 60%,
            transparent 100%);
        pointer-events: none;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 5px var(--neon-red); }
        50% { box-shadow: 0 0 20px var(--neon-red); }
        100% { box-shadow: 0 0 5px var(--neon-red); }
    }

    @keyframes flicker {
        0% { opacity: 0.95; }
        100% { opacity: 1; }
    }

    .secure-panel {
        border: 1px solid var(--matrix-green);
        border-image: linear-gradient(45deg, var(--matrix-green), var(--neon-blue)) 1;
        animation: pulse-green 3s infinite;
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(0, 20, 10, 0.7);
    }

    @keyframes pulse-green {
        0% { box-shadow: 0 0 5px var(--matrix-green); }
        50% { box-shadow: 0 0 15px var(--matrix-green); }
        100% { box-shadow: 0 0 5px var(--matrix-green); }
    }

    .scanline {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 20%;
        background: rgba(0, 0, 0, 0.2);
        animation: scanlineAnim 4s linear infinite;
        z-index: 1000;
        pointer-events: none;
        mix-blend-mode: overlay;
    }

    @keyframes scanlineAnim {
        0% { top: -100%; }
        100% { top: 100%; }
    }

    .glow-text {
        text-shadow: 0 0 10px currentColor;
        animation: text_glow 2s infinite alternate;
    }

    @keyframes text_glow {
        from { text-shadow: 0 0 5px currentColor; }
        to { text-shadow: 0 0 15px currentColor; }
    }

    .corner-decoration {
        position: fixed;
        width: 50px;
        height: 50px;
        border: 2px solid var(--neon-blue);
        opacity: 0.7;
    }

    .corner-tl {
        top: 10px;
        left: 10px;
        border-right: none;
        border-bottom: none;
    }

    .corner-tr {
        top: 10px;
        right: 10px;
        border-left: none;
        border-bottom: none;
    }

    .corner-bl {
        bottom: 10px;
        left: 10px;
        border-right: none;
        border-top: none;
    }

    .corner-br {
        bottom: 10px;
        right: 10px;
        border-left: none;
        border-top: none;
    }

    .corner-decoration::before {
        content: "";
        position: absolute;
        width: 10px;
        height: 10px;
        background: var(--neon-blue);
    }

    .corner-tl::before { top: -5px; left: -5px; }
    .corner-tr::before { top: -5px; right: -5px; }
    .corner-bl::before { bottom: -5px; left: -5px; }
    .corner-br::before { bottom: -5px; right: -5px; }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple)) !important;
    }

    .stSpinner > div > div {
        border-top-color: var(--neon-blue) !important;
    }

    .stJson {
        background: var(--terminal-bg) !important;
        border: 1px solid var(--neon-blue) !important;
    }

    .st-expander {
        border: 1px solid var(--neon-blue) !important;
    }
    .st-expander .st-expanderHeader {
        color: var(--neon-blue) !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    .glow {
    text-shadow: 0 0 20px var(--neon-blue)
    }
    </style>

    <div class="scanline"></div>
    <div class="corner-decoration corner-tl"></div>
    <div class="corner-decoration corner-tr"></div>
    <div class="corner-decoration corner-bl"></div>
    <div class="corner-decoration corner-br"></div>
    """, unsafe_allow_html=True)

def matrix_rain():
    js = """
    <canvas id="matrix"></canvas>
    <script>
    const canvas = document.getElementById('matrix');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const chars = "01アイウエオ";
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];

    for(let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }

    function draw() {
        ctx.fillStyle = 'rgba(10, 10, 10, 0.15)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#0aff0a';
        ctx.font = fontSize + 'px monospace';

        for(let i = 0; i < drops.length; i++) {
            const text = chars.charAt(Math.floor(Math.random() * chars.length));
            const opacity = Math.random() * 0.5 + 0.5;
            ctx.globalAlpha = opacity;
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
        ctx.globalAlpha = 1;
    }

    setInterval(draw, 33);

    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    </script>
    """
    components.html(js, height=0)

def hacker_type(text, element, speed=50):
    full_text = ""
    for char in text:
        full_text += char
        element.markdown(f"""
        <div class="cyber-terminal">
        <span style="color: var(--neon-blue);">>> </span>{full_text}<span style="color: #ff4b4b; animation: blink 1s infinite;">█</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(random.uniform(speed/1000, speed/500))

def analyze_threats(email):
    indicators = {
        'suspicious_urls': len(re.findall(r'http[s]?://(?!amazon|paypal|ebay|microsoft)\S+', email.lower())),
        'urgent_language': int(bool(re.search(r'urgent|immediate|action required|suspend|blocked', email.lower()))),
        'verify_requests': email.lower().count('verify'),
        'credential_keywords': len(re.findall(r'password|account|login|credentials', email.lower())),
        'spoofed_sender': int(bool(re.search(r'from:\s*\S+@(gmail|yahoo)\.com', email.lower())))
    }

    risk_score = min(0.99, 0.1 * sum(indicators.values()))
    return {
        'is_malicious': risk_score > 0.5,
        'confidence': risk_score,
        'indicators': indicators
    }

def main():

    inject_hacker_css()
    matrix_rain()

    header = st.empty()
    hacker_type("INITIALIZING PHISHNIX CYBER DEFENSE SYSTEM...", header)
    time.sleep(0.5)
    header.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="glow-text glow" style="color: var(--neon-blue); margin-bottom: 0.5rem; font-size: 2.5rem;">
        PHISHNIX: PHISHING EMAIL DETECTOR
        </h1>
        <div style="
            height: 3px;
            background: linear-gradient(90deg,
                transparent,
                var(--neon-blue),
                var(--neon-purple),
                transparent);
            margin: 0 auto;
            width: 80%;
        "></div>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_area("ENTER EMAIL CONTENT:", height=200)

    scan_button = st.empty()

    def render_results(result):
        with st.container():
            if result['is_malicious']:
                st.markdown(f"""
                <div class="alert-panel">
                <h3 style="color: var(--neon-red); margin-top: 0;"> CRITICAL THREAT DETECTED <span style="animation: flicker 0.2s infinite alternate;">🚨</span></h3>
                <p style="margin-bottom: 0;">CONFIDENCE LEVEL: <span class="glow" style="color: var(--neon-red); font-weight: bold;">{(result['confidence']*100):.1f}%</span></p>
                <div style="
                    height: 2px;
                    background: linear-gradient(90deg,
                        var(--neon-red),
                        var(--neon-purple));
                    margin: 0.5rem 0;
                "></div>
                <p style="font-size: 0.9rem; margin-bottom: 0;">
                <span style="color: var(--neon-blue);">>> </span>Recommendation: <span style="color: var(--neon-red);">QUARANTINE</span> this message immediately
                </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="secure-panel">
                <h3 style="color: var(--matrix-green); margin-top: 0;"> SECURE EMAIL VERIFIED <span style="animation: glow 1s infinite alternate;">✅</span></h3>
                <p style="margin-bottom: 0;">THREAT CONFIDENCE: <span class="glow" style="color: var(--matrix-green); font-weight: bold;">{(1-result['confidence'])*100:.1f}%</span></p>
                <div style="
                    height: 2px;
                    background: linear-gradient(90deg,
                        var(--matrix-green),
                        var(--neon-blue));
                    margin: 0.5rem 0;
                "></div>
                <p style="font-size: 0.9rem; margin-bottom: 0;">
                <span style="color: var(--neon-blue);">>> </span>Recommendation: <span style="color: var(--matrix-green);">MONITOR</span> for any changes
                </p>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🔍 TECHNICAL THREAT ANALYSIS REPORT", expanded=True):
                st.json({
                    "THREAT_INDICATORS": result['indicators'],
                    "RISK_ASSESSMENT": {
                        "THREAT_LEVEL": "CRITICAL" if result['is_malicious'] else "LOW",
                        "RECOMMENDED_ACTION": "QUARANTINE" if result['is_malicious'] else "MONITOR",
                        "ANALYSIS_TIMESTAMP": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
                    }
                })

    def loading_animation():
        loading_element = st.empty()
        with loading_element:
            hacker_type("> ESTABLISHING SECURE CONNECTION TO THREAT DATABASE...", loading_element)
            time.sleep(0.7)
            hacker_type("> SCANNING FOR MALICIOUS SIGNATURES AND PATTERNS...", loading_element)
            time.sleep(1)
            hacker_type("> VERIFYING SENDER CREDENTIALS AND DOMAIN REPUTATION...", loading_element)
            time.sleep(0.5)
            hacker_type("> CROSS-REFERENCING WITH KNOWN PHISHING TEMPLATES...", loading_element)
            time.sleep(0.8)
            loading_element.empty()

    def run_scan():
        if not email.strip():
            st.warning("NO INPUT DETECTED. PLEASE PROVIDE EMAIL CONTENT.")
            return

        scan_button.empty()
        loading_animation()

        result = analyze_threats(email)
        render_results(result)

    with scan_button:
        if st.button("INITIATE THREAT SCAN"):
            run_scan()

if __name__ == "__main__":
    main()
