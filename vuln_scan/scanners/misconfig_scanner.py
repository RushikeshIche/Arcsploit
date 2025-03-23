import requests

EXPOSED_FILES = [
    # Git & Version Control
    ".git/config", ".gitignore", ".git/logs/HEAD", ".git/HEAD",

    # Server Configuration & Credentials
    ".env", "config.json", "config.yml", "config.php",
    "settings.py", "database.yml", "db-config.php", ".htpasswd",
    ".htaccess", "server-status", "server-info",

    # Backup & Database Files
    "backup.zip", "backup.sql", "db_backup.sql", "dump.sql",
    "database.sql", "db.dump", "db_backup.tar.gz",
    "old_database.sql", "latest-dump.sql", "bak.zip",

    # Log Files
    "error.log", "access.log", "debug.log", "server.log",
    "application.log", "wp-content/debug.log",

    # Admin & Restricted Access
    "admin.php", "admin/", "administrator/", "wp-admin/",
    "phpmyadmin/", "phpinfo.php", "controlpanel/",

    # Publicly Accessible Keys & Tokens
    "id_rsa", "id_rsa.pub", "private_key.pem",
    "jwt_secret.txt", "api_keys.txt", "token.txt",

    # Other Sensitive Files
    "robots.txt", "crossdomain.xml", "web.config",
    "sitemap.xml", "phpunit.xml", "docker-compose.yml"
]

# Custom headers for request spoofing
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close"
}

def scan_misconfigurations(url):
    results = []
    
    print(f"\nScanning {url} for exposed files...\n")

    for file in EXPOSED_FILES:
        full_url = f"{url.rstrip('/')}/{file}"  # Ensures proper URL formatting
        
        try:
            response = requests.get(full_url, headers=HEADERS, timeout=5)

            
            if response.status_code == 200:
                print(f"Exposed file found: {full_url}")
                results.append({"url": full_url, "status": "Exposed"})

            
            elif response.status_code == 403:
                print(f"File exists but is restricted: {full_url}")
                results.append({"url": full_url, "status": "Restricted"})

        except requests.exceptions.RequestException as e:
        	pass
            #print(f"Error scanning {full_url}: {str(e)}")

 
    if not results:
    	print("No misconfigured file Found.\n")
    	
    '''
    TO SAVE IN JSON
        with open("misconfig_scan_results.json", "w") as file:
            json.dump(results, file, indent=4)
        print("\nResults saved to `misconfig_scan_results.json`.")
     '''

    print("\nScan completed.")
