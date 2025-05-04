from flask import Flask, request, jsonify, render_template
import re
from urlextract import URLExtract
import whois
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)

extractor = URLExtract()

# List of popular brands for spoofing detection
BRANDS = ['paypal', 'amazon', 'google', 'microsoft', 'apple', 'facebook']

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    email_text = request.form['email_text']
    label, confidence, report = predict_phishing(email_text)
    return jsonify({'label': label, 'confidence': confidence, 'report': report})

if __name__ == '__main__':
    app.run(debug=True)
