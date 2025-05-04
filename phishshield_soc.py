import streamlit as st
import time
import re
import random
import hashlib
from datetime import datetime
from streamlit.components.v1 import html
import numpy as np
import pandas as pd

# --- Cyberpunk CSS Injection ---
def inject_hacker_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=VT323&display=swap');
    
    :root {
        --neon-red: #ff4b4b;
        --neon-blue: #00f0ff;
        --matrix-green: #0aff0a;
        --neon-purple: #ff00ff;
        --dark-bg: #0a0a0a;
        --terminal-bg: rgba(0, 20, 0, 0.85);
    }
    
    body {
        background: var(--dark-bg);
        background-image: 
            radial-gradient(circle at 75% 25%, rgba(255, 75, 75, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 25% 75%, rgba(0, 240, 255, 0.08) 0%, transparent 50%),
            linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
        background-size: cover, cover, 20px 20px, 20px 20px;
        color: var(--matrix-green);
        font-family: 'VT323', 'Share Tech Mono', monospace;
        overflow-x: hidden;
    }
    
    .stApp {
        background: transparent !important;
    }
    
    .cyber-terminal {
        border: 2px solid var(--neon-blue);
        background: var(--terminal-bg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 15px var(--neon-blue);
        position: relative;
        border-radius: 0;
        font-size: 1.2rem;
    }
    
    .cyber-terminal::before {
        content: "";
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        border: 1px solid var(--neon-purple);
        z-index: -1;
    }
    
    .stTextArea textarea {
        background: #000 !important;
        color: var(--matrix-green) !important;
        border: 2px solid var(--neon-blue) !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.3rem !important;
        letter-spacing: 1px;
    }
    
    .stButton>button {
        background: #000 !important;
        color: var(--neon-blue) !important;
        border: 2px solid var(--neon-blue) !important;
        transition: all 0.3s;
        font-family: 'VT323', monospace !important;
        font-size: 1.3rem !important;
        letter-spacing: 1px;
        border-radius: 0 !important;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px var(--neon-blue);
        color: var(--neon-purple) !important;
        border-color: var(--neon-purple) !important;
        transform: translateY(-2px);
    }
    
    .critical-alert {
        border: 3px solid var(--neon-red);
        animation: pulse-red 1s infinite;
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(255, 0, 0, 0.1);
    }
    
    .warning-alert {
        border: 3px solid var(--neon-purple);
        animation: pulse-purple 2s infinite;
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(255, 0, 255, 0.1);
    }
    
    .safe-alert {
        border: 3px solid var(--matrix-green);
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(0, 255, 0, 0.1);
    }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 0 5px var(--neon-red); }
        50% { box-shadow: 0 0 20px var(--neon-red); }
        100% { box-shadow: 0 0 5px var(--neon-red); }
    }
    
    @keyframes pulse-purple {
        0% { box-shadow: 0 0 5px var(--neon-purple); }
        50% { box-shadow: 0 0 15px var(--neon-purple); }
        100% { box-shadow: 0 0 5px var(--neon-purple); }
    }
    
    .scanline {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 240, 255, 0.05),
            rgba(0, 240, 255, 0.05) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 9999;
    }
    
    .glow-text {
        text-shadow: 0 0 10px currentColor;
    }
    
    .header-terminal {
        background: var(--terminal-bg);
        border: 2px solid var(--neon-purple);
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 20px var(--neon-purple);
    }
    
    .threat-meter {
        height: 25px;
        background: linear-gradient(90deg, var(--matrix-green) 0%, var(--neon-purple) 50%, var(--neon-red) 100%);
        margin: 0.5rem 0;
        position: relative;
    }
    
    .threat-meter::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            rgba(0,0,0,0) 0%, 
            rgba(255,255,255,0.2) 50%, 
            rgba(0,0,0,0) 100%);
    }
    
    .threat-indicator {
        position: absolute;
        top: -10px;
        width: 3px;
        height: 45px;
        background: white;
        transform: translateX(-50%);
    }
    
    .threat-label {
        position: absolute;
        top: -25px;
        transform: translateX(-50%);
        font-size: 0.8rem;
    }
    
    .hex-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at center, transparent 65%, rgba(0, 240, 255, 0.03) 100%),
            url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%2300f0ff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: -1;
    }
    
    .console-cursor {
        animation: blink 1s step-end infinite;
    }
    
    @keyframes blink {
        from, to { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .signature {
        font-family: 'VT323', monospace;
        color: var(--neon-purple);
        text-align: right;
        margin-top: 2rem;
        font-size: 1.2rem;
    }
    
    .signature::before {
        content: ">> ";
    }
    
    .stProgress > div > div > div {
        background-color: var(--neon-blue) !important;
    }
    
    .stSpinner > div > div {
        border-top-color: var(--neon-blue) !important;
    }
    </style>
    
    <div class="scanline"></div>
    <div class="hex-grid"></div>
    """, unsafe_allow_html=True)

# --- Advanced Matrix Rain Effect ---
def matrix_rain():
    html("""
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
    
    // Extended character set with more symbols
    const chars = "010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ";
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    // Initialize drops with random positions and speeds
    for(let i = 0; i < columns; i++) {
        drops[i] = {
            y: Math.random() * -100,
            speed: 0.5 + Math.random() * 2,
            length: 5 + Math.floor(Math.random() * 15)
        };
    }
    
    // Color gradient for the rain
    function getRainColor(opacity) {
        return `rgba(0, 255, ${Math.floor(100 + Math.random() * 155)}, ${opacity})`;
    }
    
    function draw() {
        // Semi-transparent overlay for trail effect
        ctx.fillStyle = 'rgba(0, 10, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw each column
        for(let i = 0; i < drops.length; i++) {
            const drop = drops[i];
            const x = i * fontSize;
            
            // Draw each character in the drop
            for(let j = 0; j < drop.length; j++) {
                const yPos = (drop.y - j) * fontSize;
                if(yPos < 0) continue;
                
                const char = chars.charAt(Math.floor(Math.random() * chars.length));
                const opacity = 1 - (j / drop.length);
                
                ctx.fillStyle = getRainColor(opacity);
                ctx.font = `${fontSize}px 'VT323', monospace`;
                ctx.fillText(char, x, yPos);
            }
            
            // Reset drop if it goes off screen
            if(drop.y * fontSize > canvas.height && Math.random() > 0.975) {
                drop.y = 0;
                drop.speed = 0.5 + Math.random() * 2;
                drop.length = 5 + Math.floor(Math.random() * 15);
            }
            
            drop.y += drop.speed;
        }
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    
    setInterval(draw, 33);
    </script>
    """)

# --- Advanced Hacker Typewriter Effect ---
def hacker_type(text, element, speed=50, terminal_class=True):
    full_text = ""
    cursor = '<span class="console-cursor" style="color: #ff4b4b;">█</span>'
    
    for i, char in enumerate(text):
        full_text += char
        if terminal_class:
            element.markdown(f"""
            <div class="cyber-terminal">
            {full_text}{cursor}
            </div>
            """, unsafe_allow_html=True)
        else:
            element.markdown(f"{full_text}{cursor}", unsafe_allow_html=True)
        
        # Variable typing speed for more natural feel
        base_delay = speed/1000
        if char in ",.!?;:":
            time.sleep(base_delay * 3)
        elif char == " ":
            time.sleep(base_delay * 0.5)
        else:
            time.sleep(random.uniform(base_delay, base_delay * 2))
    
    # Keep cursor blinking at the end
    if terminal_class:
        element.markdown(f"""
        <div class="cyber-terminal">
        {full_text}{cursor}
        </div>
        """, unsafe_allow_html=True)
    else:
        element.markdown(f"{full_text}{cursor}", unsafe_allow_html=True)

# --- Advanced Threat Detection ---
def analyze_threats(email):
    # Extract email headers if present
    headers = {}
    body = email
    if "From:" in email and "To:" in email:
        header_end = email.find("\n\n")
        if header_end != -1:
            header_text = email[:header_end]
            body = email[header_end+2:]
            
            for line in header_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip().lower()] = value.strip()
    
    # Advanced pattern detection
    indicators = {
        'suspicious_urls': len(re.findall(r'http[s]?://(?!amazon|paypal|ebay|microsoft|google|apple)\S+', body.lower())),
        'shortened_urls': len(re.findall(r'(bit\.ly|goo\.gl|tinyurl|t\.co|ow\.ly)\S*', body.lower())),
        'urgent_language': len(re.findall(r'urgent|immediate|action required|suspend|blocked|account (closure|termination)|verify now', body.lower())),
        'verify_requests': len(re.findall(r'verify (your|my|the) (account|credentials|information|identity)', body.lower())),
        'credential_keywords': len(re.findall(r'password|account|login|credentials|username|social security|SSN|credit card', body.lower())),
        'spoofed_sender': int(bool(re.search(r'from:\s*\S+@(gmail|yahoo|hotmail|outlook)\.com', email.lower()))),
        'suspicious_attachments': len(re.findall(r'attachment|download|click to open|see attached', body.lower())),
        'impersonation_attempts': len(re.findall(r'dear (customer|user|valued member|account holder)', body.lower())),
        'grammar_errors': len(re.findall(r'\b(you are|your|there|their|they\'re)\b.*\b(account|password|login)\b', body.lower())),
        'unusual_formatting': len(re.findall(r'[\u0400-\u04FF\u4E00-\u9FFF]', body)) > 5,  # Cyrillic or Chinese chars
        'spf_dkim_fail': int(bool(re.search(r'spf=fail|dkim=fail', email.lower()))),
        'bcc_recipients': int('bcc:' in email.lower()),
        'reply_to_mismatch': int(bool(headers.get('reply-to') and headers.get('from') and 
                                   headers.get('reply-to').lower() != headers.get('from').lower()))
    }
    
    # Calculate weighted risk score
    weights = {
        'suspicious_urls': 0.15,
        'shortened_urls': 0.2,
        'urgent_language': 0.12,
        'verify_requests': 0.1,
        'credential_keywords': 0.15,
        'spoofed_sender': 0.08,
        'suspicious_attachments': 0.15,
        'impersonation_attempts': 0.1,
        'grammar_errors': 0.07,
        'unusual_formatting': 0.1,
        'spf_dkim_fail': 0.25,
        'bcc_recipients': 0.05,
        'reply_to_mismatch': 0.1
    }
    
    risk_score = 0
    for key in indicators:
        if isinstance(indicators[key], bool):
            risk_score += weights[key] if indicators[key] else 0
        else:
            risk_score += min(weights[key] * 0.5, weights[key] * indicators[key] * 0.1)
    
    risk_score = min(0.99, risk_score)
    
    # Additional checks
    domain_mismatch = False
    if 'from' in headers:
        from_domain = headers['from'].split('@')[-1].lower()
        for url in re.findall(r'http[s]?://([^/\s]+)', body.lower()):
            url_domain = url.split(':')[0]
            if from_domain not in url_domain and not any(tld in url_domain for tld in ['.com', '.net', '.org']):
                domain_mismatch = True
                break
    
    if domain_mismatch:
        risk_score = min(0.99, risk_score + 0.2)
    
    # Determine threat level
    if risk_score > 0.8:
        threat_level = "CRITICAL"
    elif risk_score > 0.6:
        threat_level = "HIGH"
    elif risk_score > 0.4:
        threat_level = "MODERATE"
    elif risk_score > 0.2:
        threat_level = "LOW"
    else:
        threat_level = "MINIMAL"
    
    return {
        'is_malicious': risk_score > 0.5,
        'confidence': risk_score,
        'threat_level': threat_level,
        'indicators': indicators,
        'headers_present': len(headers) > 0,
        'domain_mismatch': domain_mismatch
    }

# --- Threat Visualization ---
def show_threat_meter(score):
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(f"""
        <div style="position: relative; margin: 1rem 0;">
            <div class="threat-meter" style="width: 100%;">
                <div class="threat-indicator" style="left: {score * 100}%;"></div>
            </div>
            <div class="threat-label" style="left: 0%;">SAFE</div>
            <div class="threat-label" style="left: 50%;">SUSPICIOUS</div>
            <div class="threat-label" style="left: 100%;">MALICIOUS</div>
        </div>
        """, unsafe_allow_html=True)

# --- Main App ---
def main():
    inject_hacker_css()
    matrix_rain()
    
    # Session state for scan history
    if 'scan_history' not in st.session_state:
        st.session_state.scan_history = []
    
    # Header with animated text
    header = st.empty()
    hacker_type("INITIALIZING PHISHNIX CYBER DEFENSE SYSTEM v2.4.1...", header)
    time.sleep(0.3)
    hacker_type("\n> LOADING THREAT SIGNATURE DATABASE...", header)
    time.sleep(0.2)
    hacker_type("\n> ESTABLISHING SECURE CONNECTION...", header)
    time.sleep(0.5)
    
    header.markdown("""
    <div class="header-terminal">
        <h1 style="color: #00f0ff; text-align: center; margin-bottom: 0.5rem;" class="glow-text">
        PHISHNIX CYBER THREAT ANALYZER
        </h1>
        <div style="text-align: center; color: var(--neon-purple); font-size: 1.1rem;">
        ADVANCED PHISHING DETECTION SYSTEM | REAL-TIME ANALYSIS
        </div>
        <div style="border-top: 2px solid var(--neon-purple); margin: 0.5rem 0;"></div>
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span>STATUS: <span style="color: var(--matrix-green);">ONLINE</span></span>
            <span>SESSION: {}</span>
            <span>VERSION: 2.4.1</span>
        </div>
    </div>
    """.format(datetime.now().strftime("%Y%m%d-%H%M%S")), unsafe_allow_html=True)
    
    # Email input
    email = st.text_area("PASTE SUSPECT EMAIL CONTENT:", height=300,
                       placeholder="[>] DROP MALICIOUS EMAIL HERE FOR ANALYSIS...\n\nINCLUDE HEADERS FOR ENHANCED DETECTION")
    
    if st.button("🚀 EXECUTE ADVANCED THREAT SCAN"):
        if not email.strip():
            st.warning("[!] NO INPUT DETECTED. PLEASE PROVIDE EMAIL CONTENT.")
        else:
            with st.spinner("[>] ANALYZING CONTENT..."):
                # Create a progress bar
                progress_bar = st.progress(0)
                
                # Simulate scanning animation with detailed messages
                console = st.empty()
                hacker_type("> CONNECTING TO GLOBAL THREAT DATABASE...", console)
                time.sleep(0.3)
                progress_bar.progress(10)
                
                hacker_type("\n> SCANNING FOR MALICIOUS PATTERNS AND SIGNATURES...", console)
                time.sleep(0.5)
                progress_bar.progress(30)
                
                hacker_type("\n> ANALYZING HEADER INFORMATION...", console)
                time.sleep(0.4)
                progress_bar.progress(50)
                
                hacker_type("\n> VERIFYING SENDER CREDENTIALS AND DOMAIN REPUTATION...", console)
                time.sleep(0.6)
                progress_bar.progress(70)
                
                hacker_type("\n> CROSS-REFERENCING WITH KNOWN PHISHING TEMPLATES...", console)
                time.sleep(0.7)
                progress_bar.progress(90)
                
                # Run analysis
                result = analyze_threats(email)
                
                # Add to scan history
                scan_id = hashlib.md5(email.encode()).hexdigest()[:8]
                st.session_state.scan_history.append({
                    'id': scan_id,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'result': result
                })
                
                progress_bar.progress(100)
                time.sleep(0.2)
                
                # Display results
                if result['is_malicious']:
                    if result['threat_level'] == "CRITICAL":
                        st.markdown(f"""
                        <div class="critical-alert">
                            <h3 style="color: var(--neon-red); margin-top: 0;">⛔ CRITICAL THREAT DETECTED</h3>
                            <p>THREAT LEVEL: <span style="color: var(--neon-red); font-weight: bold;">{result['threat_level']}</span></p>
                            <p>CONFIDENCE: <span style="color: var(--neon-red); font-weight: bold;">{(result['confidence']*100):.1f}%</span></p>
                            <p>RECOMMENDED ACTION: <span style="color: var(--neon-red); font-weight: bold;">QUARANTINE EMAIL IMMEDIATELY</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-alert">
                            <h3 style="color: var(--neon-purple); margin-top: 0;">⚠️ SUSPICIOUS CONTENT DETECTED</h3>
                            <p>THREAT LEVEL: <span style="color: var(--neon-purple); font-weight: bold;">{result['threat_level']}</span></p>
                            <p>CONFIDENCE: <span style="color: var(--neon-purple); font-weight: bold;">{(result['confidence']*100):.1f}%</span></p>
                            <p>RECOMMENDED ACTION: <span style="color: var(--neon-purple); font-weight: bold;">DO NOT INTERACT WITH LINKS/ATTACHMENTS</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="safe-alert">
                        <h3 style="color: var(--matrix-green); margin-top: 0;">✅ NO SIGNIFICANT THREATS DETECTED</h3>
                        <p>THREAT LEVEL: <span style="color: var(--matrix-green); font-weight: bold;">{result['threat_level']}</span></p>
                        <p>SAFETY CONFIDENCE: <span style="color: var(--matrix-green); font-weight: bold;">{(1-result['confidence'])*100:.1f}%</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show threat meter
                show_threat_meter(result['confidence'])
                
                # Detailed report
                with st.expander("🔍 TECHNICAL THREAT ANALYSIS", expanded=True):
                    tab1, tab2, tab3 = st.tabs(["INDICATORS", "RISK ASSESSMENT", "RAW DATA"])
                    
                    # with tab1:
                    #     st.subheader("THREAT INDICATORS")
                    #     indicators_df = pd.DataFrame.from_dict(result['indicators'], orient='index', columns=['Value'])
                    #     st.dataframe(
                    #         indicators_df.style.applymap(
                    #             lambda x: 'color: #ff4b4b' if ((isinstance(x, int) and x > 0) or ((isinstance(x, bool) and x) else 'color: #0aff0a'
                    #         )
                    #     )
                        
                    #     if result['domain_mismatch']:
                    #         st.warning("DOMAIN MISMATCH DETECTED: Links in email body don't match sender domain")
                        
                    #     if not result['headers_present']:
                    #         st.info("For more accurate analysis, include email headers in your input")
                    
                    with tab2:
                        st.subheader("RISK ASSESSMENT")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("THREAT LEVEL", result['threat_level'])
                            st.metric("CONFIDENCE SCORE", f"{(result['confidence']*100):.1f}%")
                        
                        with col2:
                            st.metric("MALICIOUS", "YES" if result['is_malicious'] else "NO")
                            st.metric("HEADERS ANALYZED", "YES" if result['headers_present'] else "NO")
                        
                        st.subheader("RECOMMENDED ACTIONS")
                        if result['is_malicious']:
                            st.error("""
                            - DO NOT click any links or download attachments
                            - Report this email to your security team
                            - If you entered any credentials, change them immediately
                            - Consider scanning your system for malware
                            """)
                        else:
                            st.success("""
                            - Email appears safe but remain vigilant
                            - Verify sender identity if unsure
                            - Report any suspicious activity
                            """)
                    
                    with tab3:
                        st.subheader("RAW ANALYSIS DATA")
                        st.json(result)
                
                # Show scan history
                if len(st.session_state.scan_history) > 1:
                    with st.expander("🕒 SCAN HISTORY", expanded=False):
                        for scan in reversed(st.session_state.scan_history[:-1]):
                            col1, col2, col3 = st.columns([2, 2, 4])
                            col1.write(scan['timestamp'])
                            col2.write(f"ID: {scan['id']}")
                            col3.write(f"Threat: {scan['result']['threat_level']} ({scan['result']['confidence']*100:.1f}%)")
    
    # Footer
    st.markdown("""
    <div class="signature">
        PHISHNIX CYBER DEFENSE SYSTEM | MADE BY GAURAV JAIN
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()