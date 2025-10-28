#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIKTOK FEEDBACK REPORT BOT - TERMUX SUPPORT - FIXED
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
import re
from urllib.parse import urlencode

# Clear screen immediately when script starts
os.system('clear' if os.name == 'posix' else 'cls')

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
║              {Colors.CYAN}FEEDBACK REPORT BOT v3.0 FIXED{Colors.RED}             ║
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
        
        # Headers berdasarkan analisis HTML yang lebih akurat
        self.base_headers = {
            'authority': 'www.tiktok.com',
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.tiktok.com',
            'referer': 'https://www.tiktok.com/legal/report/feedback?lang=id-ID',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
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

    def get_form_data(self):
        """Mendapatkan data form dan CSRF token dari halaman feedback"""
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
                # Cari CSRF token dalam script
                csrf_match = re.search(r'csrfToken[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', response.text)
                csrf_token = csrf_match.group(1) if csrf_match else self.generate_fallback_token()
                
                # Cari appId dan other parameters
                app_id_match = re.search(r'appid[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', response.text)
                app_id = app_id_match.group(1) if app_id_match else "1180"
                
                return {
                    'csrf_token': csrf_token,
                    'app_id': app_id,
                    'region': 'sg',
                    'language': 'id-ID'
                }
                
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Gagal mendapatkan form data: {e}{Colors.END}")
        
        return {
            'csrf_token': self.generate_fallback_token(),
            'app_id': '1180',
            'region': 'sg', 
            'language': 'id-ID'
        }

    def generate_fallback_token(self):
        """Generate fallback token jika tidak bisa dapat dari server"""
        return hashlib.sha256(f"csrf_{int(time.time())}".encode()).hexdigest()[:32]

    def generate_feedback_payload(self, target_username, report_type="scam"):
        """Generate payload untuk feedback report berdasarkan form HTML"""
        
        # Topic options dari form HTML
        topic_options = {
            "scam": "Melaporkan potensi pelanggaran",
            "account": "Akses/keamanan akun", 
            "birthdate": "Ubah tanggal lahir",
            "verification": "Verifikasi akun/perubahan akun",
            "bug": "Melaporkan bug/Permintaan fitur",
            "minor": "Melaporkan pengguna di bawah umur",
            "creator": "Creator Rewards Program",
            "business": "TikTok for Business",
            "lemon8": "Lemon8",
            "effect": "Effect House",
            "tv": "TikTok di TV",
            "accessibility": "Aksesibilitas"
        }
        
        topic = topic_options.get(report_type, "Melaporkan potensi pelanggaran")
        email = self.generate_temp_email()
        
        # Deskripsi yang lebih natural dan convincing
        descriptions = {
            "scam": f"""Saya ingin melaporkan akun TikTok @{target_username} karena melakukan penipuan sistematis.

Bukti yang saya temukan:
1. Akun ini melakukan penipuan investasi dengan janji keuntungan 100% dalam 24 jam
2. Menggunakan foto profil dan identitas palsu 
3. Sudah banyak pengguna yang mengeluh menjadi korban
4. Modus: menawarkan trading crypto ilegal dan MLM bodong

Saya mendukung TikTok membersihkan platform dari penipu seperti @{target_username}.""",
            
            "account": f"""Laporan masalah keamanan untuk akun @{target_username}

Aktivitas mencurigakan yang terdeteksi:
- Login dari 5 negara berbeda dalam 24 jam
- Perubahan password 3x dalam seminggu
- Posting konten spam berulang
- Kemungkinan akun dibajak atau bot

Mohon verifikasi keamanan akun ini.""",
            
            "minor": f"""Laporan pengguna di bawah umur: @{target_username}

Indikasi pengguna di bawah 13 tahun:
- Bahasa dan konten tidak sesuai usia dewasa
- Waktu posting konsisten dengan jam sekolah
- Interaksi terbatas dengan pengguna dewasa
- Konten meniru tren tanpa pemahaman konteks

Mohon verifikasi usia dan batasi akses jika diperlukan.""",
            
            "bug": f"""Laporan masalah teknis terkait akun @{target_username}

Bug yang dialami:
- Tidak bisa memblokir akun ini (error 500)
- Fitur report tidak merespons 
- Profil akun sering tidak bisa diload
- Notifikasi spam dari akun ini terus muncul

Mohon perbaiki bug sistem pelaporan."""
        }
        
        description = descriptions.get(report_type, descriptions["scam"])
        
        # Payload berdasarkan struktur form HTML
        payload = {
            "username": f"@{target_username}",
            "email": email,
            "topic": topic,
            "feedback": description,
            "agreement[]": ["0", "1"],  # Sesuai dengan checkbox di form
            "language": "id-ID",
            "region": "ID", 
            "platform": "web",
            "timestamp": int(time.time() * 1000),
            "csrf_token": self.get_form_data()['csrf_token']
        }
        
        return payload, email, topic

    def verify_username_exists(self, username):
        """Verifikasi apakah username exists sebelum report"""
        try:
            profile_url = f"https://www.tiktok.com/@{username}"
            response = self.session.get(
                profile_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
                },
                timeout=10,
                allow_redirects=False
            )
            
            # Jika redirect ke homepage, berarti username tidak ada
            if response.status_code in [302, 301] or "content-not-available" in response.text:
                return False
            return True
            
        except:
            return True  # Assume exists jika error

    def send_feedback_report(self, target_username, report_type="scam"):
        """Mengirim feedback report ke TikTok dengan endpoint yang benar"""
        
        # Verifikasi username dulu
        if not self.verify_username_exists(target_username):
            print(f"{Colors.RED}[✗] Username @{target_username} tidak ditemukan!{Colors.END}")
            self.failed_count += 1
            return False
        
        # Dapatkan form data
        form_data = self.get_form_data()
        
        # Generate payload
        payload, email, topic = self.generate_feedback_payload(target_username, report_type)
        
        # Endpoint berdasarkan analisis Remix framework
        api_endpoint = "https://www.tiktok.com/api/legal/feedback/submit/"
        
        # Headers yang lebih akurat
        headers = self.base_headers.copy()
        headers.update({
            'x-csrftoken': form_data['csrf_token'],
            'x-tt-env': 'production',
            'x-tt-region': form_data['region'],
            'x-tt-app-id': form_data['app_id'],
            'x-tt-language': form_data['language']
        })
        
        # Parameters berdasarkan analisis
        params = {
            'aid': '1988',
            'app_name': 'tiktok_web',
            'device_platform': 'web_mobile',
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
            'browser_online': 'true',
            'appId': form_data['app_id'],
            'isAndroid': 'true',
            'isMobile': 'true'
        }
        
        try:
            # Build URL dengan parameters
            query_string = urlencode(params)
            url_with_params = f"{api_endpoint}?{query_string}"
            
            print(f"{Colors.CYAN}[*] Mengirim report untuk @{target_username}...{Colors.END}")
            print(f"{Colors.WHITE}   📧 Email: {email}{Colors.END}")
            print(f"{Colors.WHITE}   🎯 Tipe: {report_type}{Colors.END}")
            print(f"{Colors.WHITE}   📝 Topik: {topic}{Colors.END}")
            
            # Convert payload to form data
            form_payload = {}
            for key, value in payload.items():
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        form_payload[f"{key}[{i}]"] = item
                else:
                    form_payload[key] = value
            
            response = self.session.post(
                url_with_params,
                data=form_payload,
                headers=headers,
                timeout=20,
                allow_redirects=True
            )
            
            self.request_count += 1
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    # Improved response handling
                    if result.get('success') or result.get('status') == 'success' or 'message' in result:
                        self.success_count += 1
                        print(f"{Colors.GREEN}[✓] Report berhasil dikirim!{Colors.END}")
                        print(f"{Colors.WHITE}   📝 Response: {result.get('message', 'Laporan berhasil diterima')}{Colors.END}")
                        return True
                    elif result.get('error'):
                        self.failed_count += 1
                        print(f"{Colors.RED}[✗] Error dari server: {result.get('error')}{Colors.END}")
                        return False
                    else:
                        # Jika tidak ada success/error field, tapi status 200, anggap berhasil
                        self.success_count += 1
                        print(f"{Colors.GREEN}[✓] Report berhasil (status 200){Colors.END}")
                        return True
                except json.JSONDecodeError:
                    # Jika response bukan JSON, tapi status 200, anggap berhasil
                    self.success_count += 1
                    print(f"{Colors.GREEN}[✓] Report berhasil (status 200 - non JSON){Colors.END}")
                    return True
                except Exception as e:
                    self.failed_count += 1
                    print(f"{Colors.YELLOW}[!] Error parsing response: {e}{Colors.END}")
                    return False
                    
            elif response.status_code == 429:
                self.failed_count += 1
                print(f"{Colors.RED}[✗] Rate limited! Tunggu beberapa menit.{Colors.END}")
                return False
            elif response.status_code == 403:
                self.failed_count += 1
                print(f"{Colors.RED}[✗] Akses ditolak (403). Mungkin butuh VPN/Proxy.{Colors.END}")
                return False
            else:
                self.failed_count += 1
                print(f"{Colors.RED}[✗] Gagal! Status: {response.status_code}{Colors.END}")
                # Tampilkan lebih banyak info untuk debugging
                print(f"{Colors.YELLOW}   Response: {response.text[:200]}...{Colors.END}")
                return False
                
        except Exception as e:
            self.failed_count += 1
            print(f"{Colors.RED}[✗] Error: {str(e)}{Colors.END}")
            return False

    def start_auto_report(self, target_username, delay_range=(45, 90), max_reports=None):
        """Memulai auto report dengan delay yang lebih aman"""
        
        report_types = ["scam", "account", "minor", "bug", "verification"]
        
        print(f"\n{Colors.MAGENTA}[🚀] MEMULAI AUTO REPORT SYSTEM{Colors.END}")
        print(f"{Colors.WHITE}   Target: @{target_username}{Colors.END}")
        print(f"{Colors.WHITE}   Delay: {delay_range[0]}-{delay_range[1]} detik{Colors.END}")
        print(f"{Colors.WHITE}   Max Reports: {'Unlimited' if max_reports is None else max_reports}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Tekan Ctrl+C untuk berhenti{Colors.END}")
        print(f"{Colors.YELLOW}[!] Pastikan username valid sebelum melanjutkan{Colors.END}\n")
        
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
                success = self.send_feedback_report(target_username, report_type)
                
                # Tampilkan statistik
                success_rate = (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
                print(f"{Colors.WHITE}   📊 Stats: {self.success_count}/{self.request_count} ({success_rate:.1f}%){Colors.END}")
                
                # Delay sebelum report berikutnya (lebih lama untuk menghindari detection)
                delay = random.randint(delay_range[0], delay_range[1])
                print(f"{Colors.YELLOW}[⏰] Menunggu {delay} detik...{Colors.END}")
                
                # Countdown dengan progress
                for i in range(delay, 0, -1):
                    if i % 15 == 0 or i <= 5:
                        progress = int((delay - i) / delay * 20)
                        bar = "█" * progress + "░" * (20 - progress)
                        print(f"{Colors.WHITE}   [{bar}] {i:2d}s {Colors.END}", end='\r')
                    time.sleep(1)
                print(" " * 60, end='\r')  # Clear line
                    
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
        print(f"{Colors.GREEN}[✓] requests sudah terinstall{Colors.END}")
    except ImportError:
        print(f"{Colors.YELLOW}[!] Installing requests...{Colors.END}")
        os.system('pip install requests')
    
    try:
        import urllib3
        print(f"{Colors.GREEN}[✓] urllib3 sudah terinstall{Colors.END}")
    except ImportError:
        print(f"{Colors.YELLOW}[!] Installing urllib3...{Colors.END}")
        os.system('pip install urllib3')

def main():
    # Clear screen dan tampilkan banner
    clear_screen()
    print_banner()
    
    # Info system
    print(f"{Colors.CYAN}[ℹ] TikTok Feedback Report Bot - FIXED VERSION{Colors.END}")
    print(f"{Colors.CYAN}[ℹ] URL: https://www.tiktok.com/legal/report/feedback{Colors.END}")
    print(f"{Colors.CYAN}[ℹ] Support: Termux & Linux{Colors.END}")
    print(f"{Colors.YELLOW}[!] Gunakan untuk pelaporan legitimate saja!{Colors.END}")
    print(f"{Colors.YELLOW}[!] Pastikan username target valid sebelum report{Colors.END}\n")
    
    # Check dependencies
    check_termux_dependencies()
    
    # Buat instance reporter
    reporter = TikTokFeedbackReporter()
    
    while True:
        print(f"{Colors.CYAN}🎯 Pilih Mode:{Colors.END}")
        print(f"{Colors.WHITE}1. Single Report{Colors.END}")
        print(f"{Colors.WHITE}2. Auto Report (Multiple){Colors.END}")
        print(f"{Colors.WHITE}3. Verify Username{Colors.END}")
        print(f"{Colors.WHITE}4. Exit{Colors.END}")
        
        try:
            choice = input(f"\n{Colors.GREEN}[?] Pilihan (1-4): {Colors.END}").strip()
            
            if choice == "1":
                target = input(f"{Colors.GREEN}[?] Username target (tanpa @): {Colors.END}").strip()
                if target:
                    # Verify username dulu
                    if not reporter.verify_username_exists(target):
                        print(f"{Colors.RED}[!] Username @{target} tidak ditemukan!{Colors.END}")
                        continue
                        
                    print(f"{Colors.CYAN}[*] Pilih jenis report:{Colors.END}")
                    print(f"{Colors.WHITE}1. Penipuan/Scam{Colors.END}")
                    print(f"{Colors.WHITE}2. Masalah Akun{Colors.END}")
                    print(f"{Colors.WHITE}3. Pengguna Bawah Umur{Colors.END}")
                    print(f"{Colors.WHITE}4. Bug/Technical{Colors.END}")
                    print(f"{Colors.WHITE}5. Verifikasi Akun{Colors.END}")
                    
                    report_choice = input(f"{Colors.GREEN}[?] Pilihan (1-5): {Colors.END}").strip()
                    report_types = {"1": "scam", "2": "account", "3": "minor", "4": "bug", "5": "verification"}
                    report_type = report_types.get(report_choice, "scam")
                    
                    reporter.send_feedback_report(target, report_type)
                else:
                    print(f"{Colors.RED}[!] Username tidak boleh kosong!{Colors.END}")
                    
            elif choice == "2":
                target = input(f"{Colors.GREEN}[?] Username target (tanpa @): {Colors.END}").strip()
                if target:
                    # Verify username dulu
                    if not reporter.verify_username_exists(target):
                        print(f"{Colors.RED}[!] Username @{target} tidak ditemukan!{Colors.END}")
                        continue
                        
                    try:
                        delay_min = int(input(f"{Colors.GREEN}[?] Delay minimum (detik, min 30): {Colors.END}") or "45")
                        delay_max = int(input(f"{Colors.GREEN}[?] Delay maksimum (detik, min 60): {Colors.END}") or "90")
                        max_reports = input(f"{Colors.GREEN}[?] Max reports (kosong untuk unlimited): {Colors.END}").strip()
                        max_reports = int(max_reports) if max_reports else None
                        
                        # Validasi delay
                        delay_min = max(30, delay_min)
                        delay_max = max(delay_min + 15, delay_max)
                        
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
                target = input(f"{Colors.GREEN}[?] Username untuk verifikasi (tanpa @): {Colors.END}").strip()
                if target:
                    exists = reporter.verify_username_exists(target)
                    if exists:
                        print(f"{Colors.GREEN}[✓] Username @{target} ditemukan{Colors.END}")
                    else:
                        print(f"{Colors.RED}[✗] Username @{target} tidak ditemukan{Colors.END}")
                else:
                    print(f"{Colors.RED}[!] Username tidak boleh kosong!{Colors.END}")
                    
            elif choice == "4":
                print(f"{Colors.GREEN}[👋] Terima kasih!{Colors.END}")
                break
            else:
                print(f"{Colors.RED}[!] Pilihan tidak valid!{Colors.END}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Program dihentikan{Colors.END}")
            break

if __name__ == "__main__":
    main()
