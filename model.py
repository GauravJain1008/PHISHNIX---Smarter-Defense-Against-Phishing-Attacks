from urlextract import URLExtract
import re

extractor = URLExtract()

def check_urls(email_text):
    urls = extractor.find_urls(email_text)
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update', 'bank']
    url_analysis = []
    for url in urls:
        analysis = {"url": url, "suspicious": False, "reasons": []}
        for word in suspicious_keywords:
            if word in url.lower():
                analysis["suspicious"] = True
                analysis["reasons"].append(f"Contains suspicious keyword: {word}")
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
    
    # Combine reasons and generate report
    report = {
        "threat_level": "low",
        "reasons": [],
        "suspicious_words": word_matches,
        "url_analysis": url_analysis
    }
    
    threat_score = len(word_matches) + sum([2 for url in url_analysis if url["suspicious"]])
    
    if threat_score > 5:
        report["threat_level"] = "high"
    elif threat_score > 2:
        report["threat_level"] = "medium"
    else:
        report["threat_level"] = "low"
        
    report["reasons"].extend([f"Email contains suspicious word: {word}" for word in word_matches])
    report["reasons"].extend([reason for url in url_analysis for reason in url["reasons"]])
    
    is_phishing = threat_score > 2
    confidence = 0.90 if is_phishing else 0.95
    
    return "Phishing" if is_phishing else "Legitimate", confidence, report
