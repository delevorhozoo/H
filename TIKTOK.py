#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIKTOK FEEDBACK REPORT BOT - TERMUX SUPPORT
URL: https://www.tiktok.com/legal/report/feedback?lang=id-ID
Developer: MexazoExecuted
"""

import requests
import time
import random
import hashlib
import string
import json
import os
import sys
from urllib.parse import quote, unquote

# Color codes for Termux
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  ████████╗██╗██╗  ██╗██████╗  ██████╗ ██╗  ██╗                ║
║  ╚══██╔══╝██║██║ ██╔╝██╔══██╗██╔═══██╗██║ ██╔╝                ║
║     ██║   ██║█████╔╝ ██║  ██║██║   ██║█████╔╝                 ║
║     ██║   ██║██╔═██╗ ██║  ██║██║   ██║██╔═██╗                 ║
║     ██║   ██║██║  ██╗██████╔╝╚██████╔╝██║  ██╗                ║
║     ╚═╝   ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝                ║
║                                                                ║
║                {Colors.CYAN}FEEDBACK REPORT BOT v2.0{Colors.RED}                 ║
║                    {Colors.YELLOW}Termux Supported{Colors.RED}                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

class TikTokFeedbackReporter:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.tiktok.com"
        self.feedback_url = "https://www.tiktok.com/legal/report/feedback"
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        
        # Headers berdasarkan analisis HTML
        self.base_headers = {
            'authority': 'www.tiktok.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.tiktok.com',
            'referer': 'https://www.tiktok.com/legal/report/feedback?lang=id-ID',
            'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

    def generate_temp_email(self):
        """Generate temporary email menggunakan 1secmail"""
        try:
            response = requests.get(
                "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
                timeout=5
            )
            if response.status_code == 200:
                emails = response.json()
                if emails:
                    return emails[0]
        except:
            pass
        
        # Fallback email generator
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{username}@{random.choice(domains)}"

    def generate_fingerprint(self):
        """Generate device fingerprint"""
        timestamp = int(time.time() * 1000)
        return {
            'device_id': f"7{random.randint(100000000000000000, 999999999999999999)}",
            'install_id': f"7{random.randint(100000000000000000, 999999999999999999)}",
            'session_id': hashlib.sha256(f"{timestamp}{random.random()}".encode()).hexdigest()[:32],
            'fp': hashlib.md5(f"fp_{timestamp}".encode()).hexdigest(),
            'ts': timestamp
        }

    def get_csrf_token(self):
        """Mendapatkan CSRF token dari halaman feedback"""
        try:
            response = self.session.get(
                f"{self.feedback_url}?lang=id-ID",
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # Cari CSRF token dalam response
                import re
                csrf_match = re.search(r'csrfToken[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', response.text)
                if csrf_match:
                    return csrf_match.group(1)
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Gagal mendapatkan CSRF token: {e}{Colors.END}")
        
        return hashlib.sha256(f"csrf_{int(time.time())}".encode()).hexdigest()[:32]

    def generate_feedback_payload(self, target_username, report_type="scam"):
        """Generate payload untuk feedback report"""
        
        # Mapping topic berdasarkan pilihan di form
        topic_mapping = {
            "scam": "Melaporkan potensi pelanggaran",
            "account": "Akses/keamanan akun", 
            "minor": "Melaporkan pengguna di bawah umur",
            "bug": "Melaporkan bug/Permintaan fitur",
            "verification": "Verifikasi akun/perubahan akun"
        }
        
        topic = topic_mapping.get(report_type, "Melaporkan potensi pelanggaran")
        email = self.generate_temp_email()
        
        # Deskripsi berdasarkan jenis report
        descriptions = {
            "scam": f"""Saya ingin melaporkan akun TikTok @{target_username} karena melakukan penipuan.

Detail pelanggaran:
- Akun ini melakukan penipuan dengan modus penggalangan dana palsu
- Menawarkan investasi bodong dengan janji keuntungan tidak realistis
- Menggunakan identitas palsu untuk menipu korban
- Sudah banyak korban yang tertipu dengan modus ini

Saya meminta TikTok untuk segera menindak akun ini dan melindungi pengguna lain dari penipuan.""",
            
            "account": f"""Laporan keamanan akun @{target_username}

Akun ini menunjukkan aktivitas mencurigakan:
- Percobaan akses tidak sah dari berbagai lokasi
- Perubahan password berulang kali
- Aktivitas posting yang tidak wajar
- Kemungkinan akun telah dibajak""",
            
            "minor": f"""Laporan pengguna di bawah umur: @{target_username}

Berdasarkan konten dan perilaku akun, saya menduga:
- Pemilik akun berusia di bawah 13 tahun
- Menggunakan TikTok tanpa pengawasan orang tua
- Konten tidak pantas untuk usia tersebut
- Perlu verifikasi usia dan pembatasan akses""",
            
            "bug": f"""Laporan bug untuk akun @{target_username}

Masalah teknis yang ditemukan:
- Fitur report tidak berfungsi dengan baik
- Error saat mencoba memblokir akun ini
- Masalah loading profil akun
- Bug dalam sistem pelaporan"""
        }
        
        description = descriptions.get(report_type, descriptions["scam"])
        
        payload = {
            "username": f"@{target_username}",
            "email": email,
            "topic": topic,
            "feedback": description,
            "agreement": ["0", "1"],  # Kedua checkbox dicentang
            "language": "id-ID",
            "region": "ID",
            "platform": "web",
            "timestamp": int(time.time() * 1000),
            "session_id": self.generate_fingerprint()['session_id'],
            "csrf_token": self.get_csrf_token()
        }
        
        return payload, email

    def send_feedback_report(self, target_username, report_type="scam"):
        """Mengirim feedback report ke TikTok"""
        
        # API endpoint berdasarkan analisis
        api_endpoint = "https://www.tiktok.com/api/feedback/submit/"
        
        # Generate payload
        payload, email = self.generate_feedback_payload(target_username, report_type)
        
        # Headers untuk request
        headers = self.base_headers.copy()
        headers.update({
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': payload['csrf_token'],
            'x-tt-env': 'production',
            'x-tt-region': 'sg'
        })
        
        # Parameters dynamic
        params = {
            'aid': '1988',
            'app_name': 'tiktok_web',
            'device_platform': 'web',
            'region': 'ID',
            'lang': 'id',
            'ts': str(int(time.time() * 1000)),
            'cookie_enabled': 'true',
            'screen_width': '360',
            'screen_height': '740',
            'browser_language': 'id-ID',
            'browser_platform': 'Linux armv8l',
            'browser_name': 'Mozilla',
            'browser_version': '5.0+(Linux;+Android+10;+K)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/120.0.0.0+Mobile+Safari/537.36',
            'browser_online': 'true'
        }
        
        try:
            # Build URL dengan parameters
            url_with_params = f"{api_endpoint}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
            
            print(f"{Colors.CYAN}[*] Mengirim report untuk @{target_username}...{Colors.END}")
            print(f"{Colors.WHITE}   📧 Email: {email}{Colors.END}")
            print(f"{Colors.WHITE}   🎯 Tipe: {report_type}{Colors.END}")
            
            response = self.session.post(
                url_with_params,
                json=payload,
                headers=headers,
                timeout=15
            )
            
            self.request_count += 1
            
            if response.status_code == 200:
                self.success_count += 1
                result = response.json()
                
                print(f"{Colors.GREEN}[✓] Report berhasil!{Colors.END}")
                print(f"{Colors.WHITE}   📝 Response: {result.get('message', 'Success')}{Colors.END}")
                return True
            else:
                self.failed_count += 1
                print(f"{Colors.RED}[✗] Report gagal! Status: {response.status_code}{Colors.END}")
                return False
                
        except Exception as e:
            self.failed_count += 1
            print(f"{Colors.RED}[✗] Error: {str(e)}{Colors.END}")
            return False

    def start_auto_report(self, target_username, delay_range=(30, 60), max_reports=None):
        """Memulai auto report dengan delay"""
        
        report_types = ["scam", "account", "minor", "bug"]
        
        print(f"\n{Colors.MAGENTA}[🚀] MEMULAI AUTO REPORT SYSTEM{Colors.END}")
        print(f"{Colors.WHITE}   Target: @{target_username}{Colors.END}")
        print(f"{Colors.WHITE}   Delay: {delay_range[0]}-{delay_range[1]} detik{Colors.END}")
        print(f"{Colors.WHITE}   Max Reports: {'Unlimited' if max_reports is None else max_reports}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Tekan Ctrl+C untuk berhenti{Colors.END}\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                
                if max_reports and iteration > max_reports:
                    print(f"{Colors.CYAN}[*] Mencapai batas maksimal {max_reports} reports{Colors.END}")
                    break
                
                # Pilih random report type
                report_type = random.choice(report_types)
                
                print(f"\n{Colors.CYAN}[{iteration}] {time.strftime('%H:%M:%S')}{Colors.END}")
                self.send_feedback_report(target_username, report_type)
                
                # Tampilkan statistik
                success_rate = (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
                print(f"{Colors.WHITE}   📊 Stats: {self.success_count}/{self.request_count} ({success_rate:.1f}%){Colors.END}")
                
                # Delay sebelum report berikutnya
                delay = random.randint(delay_range[0], delay_range[1])
                print(f"{Colors.YELLOW}[⏰] Menunggu {delay} detik...{Colors.END}")
                
                # Countdown
                for i in range(delay, 0, -1):
                    if i % 10 == 0 or i <= 5:
                        print(f"{Colors.WHITE}   {i} detik...{Colors.END}", end='\r')
                    time.sleep(1)
                print(" " * 50, end='\r')  # Clear line
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Dihentikan oleh user{Colors.END}")
        
        # Tampilkan statistik final
        self.show_final_stats()

    def show_final_stats(self):
        """Tampilkan statistik final"""
        print(f"\n{Colors.MAGENTA}╔════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.MAGENTA}║           📊 FINAL STATISTICS           ║{Colors.END}")
        print(f"{Colors.MAGENTA}╠════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.WHITE}║ Total Requests: {self.request_count:>20} ║{Colors.END}")
        print(f"{Colors.GREEN}║ Berhasil: {self.success_count:>28} ║{Colors.END}")
        print(f"{Colors.RED}║ Gagal: {self.failed_count:>31} ║{Colors.END}")
        
        if self.request_count > 0:
            success_rate = (self.success_count / self.request_count) * 100
            print(f"{Colors.CYAN}║ Success Rate: {success_rate:>24.1f}% ║{Colors.END}")
        
        print(f"{Colors.MAGENTA}╚════════════════════════════════════════╝{Colors.END}")

def check_termux_dependencies():
    """Check dan install dependencies untuk Termux"""
    try:
        import requests
    except ImportError:
        print(f"{Colors.YELLOW}[!] Installing requests...{Colors.END}")
        os.system('pip install requests')
    
    try:
        import urllib3
    except ImportError:
        print(f"{Colors.YELLOW}[!] Installing urllib3...{Colors.END}")
        os.system('pip install urllib3')

def main():
    # Check dependencies
    check_termux_dependencies()
    
    # Clear screen dan tampilkan banner
    clear_screen()
    print_banner()
    
    # Info system
    print(f"{Colors.CYAN}[ℹ] TikTok Feedback Report Bot{Colors.END}")
    print(f"{Colors.CYAN}[ℹ] URL: https://www.tiktok.com/legal/report/feedback{Colors.END}")
    print(f"{Colors.CYAN}[ℹ] Support: Termux & Linux{Colors.END}")
    print(f"{Colors.YELLOW}[!] Gunakan untuk pelaporan legitimate saja!{Colors.END}\n")
    
    # Buat instance reporter
    reporter = TikTokFeedbackReporter()
    
    while True:
        print(f"{Colors.CYAN}🎯 Pilih Mode:{Colors.END}")
        print(f"{Colors.WHITE}1. Single Report{Colors.END}")
        print(f"{Colors.WHITE}2. Auto Report (Multiple){Colors.END}")
        print(f"{Colors.WHITE}3. Exit{Colors.END}")
        
        try:
            choice = input(f"\n{Colors.GREEN}[?] Pilihan (1-3): {Colors.END}").strip()
            
            if choice == "1":
                target = input(f"{Colors.GREEN}[?] Username target (tanpa @): {Colors.END}").strip()
                if target:
                    print(f"{Colors.CYAN}[*] Pilih jenis report:{Colors.END}")
                    print(f"{Colors.WHITE}1. Penipuan/Scam{Colors.END}")
                    print(f"{Colors.WHITE}2. Masalah Akun{Colors.END}")
                    print(f"{Colors.WHITE}3. Pengguna Bawah Umur{Colors.END}")
                    print(f"{Colors.WHITE}4. Bug/Technical{Colors.END}")
                    
                    report_choice = input(f"{Colors.GREEN}[?] Pilihan (1-4): {Colors.END}").strip()
                    report_types = {"1": "scam", "2": "account", "3": "minor", "4": "bug"}
                    report_type = report_types.get(report_choice, "scam")
                    
                    reporter.send_feedback_report(target, report_type)
                else:
                    print(f"{Colors.RED}[!] Username tidak boleh kosong!{Colors.END}")
                    
            elif choice == "2":
                target = input(f"{Colors.GREEN}[?] Username target (tanpa @): {Colors.END}").strip()
                if target:
                    try:
                        delay_min = int(input(f"{Colors.GREEN}[?] Delay minimum (detik): {Colors.END}") or "30")
                        delay_max = int(input(f"{Colors.GREEN}[?] Delay maksimum (detik): {Colors.END}") or "60")
                        max_reports = input(f"{Colors.GREEN}[?] Max reports (kosong untuk unlimited): {Colors.END}").strip()
                        max_reports = int(max_reports) if max_reports else None
                        
                        reporter.start_auto_report(
                            target, 
                            delay_range=(delay_min, delay_max),
                            max_reports=max_reports
                        )
                    except ValueError:
                        print(f"{Colors.RED}[!] Input tidak valid!{Colors.END}")
                else:
                    print(f"{Colors.RED}[!] Username tidak boleh kosong!{Colors.END}")
                    
            elif choice == "3":
                print(f"{Colors.GREEN}[👋] Terima kasih!{Colors.END}")
                break
            else:
                print(f"{Colors.RED}[!] Pilihan tidak valid!{Colors.END}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Program dihentikan{Colors.END}")
            break

if __name__ == "__main__":
    main()
