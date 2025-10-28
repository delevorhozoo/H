import os
import sys
import subprocess
import requests
import json
import time
import random
import hashlib
import uuid
from datetime import datetime

def install_requirements():
    """Install required packages"""
    required_packages = ['requests']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} sudah terinstall")
        except ImportError:
            print(f"📦 Menginstall {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} berhasil diinstall")
            except subprocess.CalledProcessError:
                print(f"❌ Gagal menginstall {package}")
                sys.exit(1)

def get_weather_icon():
    """Mendapatkan icon cuaca berdasarkan waktu dan random"""
    hour = datetime.now().hour
    weather_types = []
    
    if 6 <= hour < 12:
        weather_types = ["☀️", "⛅", "🌤️", "🌅"]
    elif 12 <= hour < 18:
        weather_types = ["☀️", "🔥", "🌡️", "♨️"]
    elif 18 <= hour < 24:
        weather_types = ["🌙", "⭐", "🌠", "🌌"]
    else:
        weather_types = ["🌙", "🌑", "🌃", "💫"]
    
    if random.random() < 0.3:
        weather_types.extend(["🌧️", "⛈️", "🌦️", "☁️", "💨"])
    
    return random.choice(weather_types)

def show_banner():
    """_______PWNET_LORDHOZOO"""
    now = datetime.now()
    weather_icon = get_weather_icon()
    
    banner = f"""
⠠⠤⠤⠤⠤⠤⣤⣤⣤⣄⣀⣀                        
             ⠉⠉⠛⠛⠿⢶⣤⣄⡀                  
  ⢀⣀⣀⣠⣤⣤⣴⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠿⠿⢿⡇                  
⠚⠛⠉⠉⠉      ⢀⣀⣀⣤⡴⠶⠶⠿⠿⠿⣧⡀   ⠤⢄⣀           
       ⢀⣠⡴⠞⠛⠉⠁       ⢸⣿⣷⣶⣦⣤⣄⣈⡑⢦⣀        
    ⣠⠔⠚⠉⠁          ⢀⣾⡿⠟⠉⠉⠉⠉⠙⠛⠿⣿⣮⣷⣤      
                  ⢀⣿⡿⠁         ⠉⢻⣯⣧⡀    
                  ⢸⣿⡇            ⠉⠻⢷⡤   
                  ⠈⢿⣿⡀                  
                   ⠈⠻⣿⣦⣤⣀⡀              
                      ⠉⠙⠛⠛⠻⠿⠿⣿⣶⣶⣦⣄⣀     
                            ⠉⠻⣿⣯⡛⠻⢦⡀  
                              ⠈⠙⢿⣆ ⠙⢆ 
                                ⠈⢻⣆ ⠈⢣
                                  ⠻⡆ ⠈
                                   ⢻⡀ 
                                   ⠈⠃
    🚀 TIKTOK REPORT TOOL - TERMUX 🚀
    📧 Contact: hozoonetwork@gmail.com
    
    📅 {now.strftime('%A, %d %B %Y')}
    🕐 {now.strftime('%H:%M:%S')} {weather_icon}
    """
    print(banner)

class TikTokReporter:
    def __init__(self):
        # Real TikTok API endpoints
        self.report_urls = [
            "https://mssdk-sg.tiktok.com/web/report",
            "https://www.tiktok.com/api/report/reason/",
            "https://www.tiktok.com/node/report/reasons_put/"
        ]
        
        self.monitor_url = "https://mon.tiktokv.com/monitor_browser/collect/batch/?bid=tiktok_pns_web_runtime"
        
        # Generate realistic TikTok parameters
        self.ms_token = self.generate_ms_token()
        self.x_bogus = self.generate_x_bogus()
        self.x_gnarly = self.generate_x_gnarly()
        
        # Real TikTok headers from your example
        self.headers = {
            'Authority': 'mssdk-sg.tiktok.com',
            'Method': 'POST',
            'Path': f'/web/report?msToken={self.ms_token}&X-Bogus={self.x_bogus}&X-Gnarly={self.x_gnarly}',
            'Scheme': 'https',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Content-Length': '4579',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Cookie': self.generate_cookies(),
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/',
            'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Priority': 'u=1, i',
        }
        
        self.success_count = 0
        self.fail_count = 0
        self.total_sent = 0
        
    def generate_ms_token(self):
        """Generate realistic msToken"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        return ''.join(random.choice(chars) for _ in range(150))
    
    def generate_x_bogus(self):
        """Generate X-Bogus parameter"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return f"DFSzswV{''.join(random.choice(chars) for _ in range(25))}"
    
    def generate_x_gnarly(self):
        """Generate X-Gnarly parameter"""
        parts = [
            "Mk9YPmNgvRaB0O30OXrg6CLqNkR2R",
            "nCLqERlJNAdoigRgAdkJz",
            "lDbWy0sVn742EDsetEMnFONxnkMXghtcP9WpyOZ",
            "j6eJeJw0rzwIMAyU0mOj35TLJmlwETt0AKdorGHyX1S6IVPZy2j7bZgFvcznXDqE",
            "J9U3NShcBp28gMqoRoqXBaY5apKWzkC0pWIYrQMqNykfT4Pe3RjOxXm7vZ5bz7tJqraD04ySElGdjBw5AUHcVSzGMV",
            "HT5cgPmspP",
            "1DYFLLSEdvYzoJl0C",
            "onhLD",
            "gnx3U1BpEKuWm6JSv"
        ]
        return random.choice(parts)
    
    def generate_cookies(self):
        """Generate realistic TikTok cookies"""
        cookies = {
            'tt_chain_token': f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))}==",
            'odin_tt': hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest(),
            'tt_csrf_token': f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))}-{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))}",
            's_v_web_id': f"verify_{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}_{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))}",
            'ttwid': f"1%7C{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=32))}%7C{int(time.time())}%7C{hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()}",
            'msToken': self.ms_token
        }
        return '; '.join([f'{k}={v}' for k, v in cookies.items()])
    
    def create_report_data(self, username, email, tiktok_url, violation_details):
        """
        Membuat data laporan real TikTok format
        """
        clean_username = self.extract_username(username)
        
        report_data = {
            "report_type": "user",
            "object_id": clean_username,
            "owner_id": clean_username,
            "reason": random.choice([1004, 1005, 1006, 1007, 2001, 2002, 2003]),
            "reason_title": random.choice(["Other", "Harassment", "Spam", "Impersonation", "Hate Speech"]),
            "additional_info": violation_details,
            "email": email,
            "report_url": tiktok_url,
            "timestamp": int(time.time() * 1000),  # TikTok uses milliseconds
            "declaration": True,
            "user_agent": self.headers['User-Agent'],
            "app_type": "tiktok_web",
            "app_version": "v2.0",
            "device_id": str(uuid.uuid4()),
            "region": "ID",
            "priority_region": "",
            "report_source": "user_profile_page"
        }
        return report_data
    
    def create_monitor_data(self):
        """Create monitor data for TikTok analytics"""
        return {
            "header": {
                "app_id": 1233,
                "app_ver": "2.0.0",
                "app_region": "ID",
                "carrier_region": "ID",
                "device_id": str(uuid.uuid4()),
                "device_platform": "web",
                "device_type": "PC",
                "os": "windows",
                "os_ver": "10",
                "time_zone": "Asia/Jakarta"
            },
            "batch": [
                {
                    "event": "report_submit",
                    "params": {
                        "timestamp": int(time.time() * 1000),
                        "report_type": "user",
                        "success": random.choice([True, False])
                    }
                }
            ]
        }
    
    def extract_username(self, username):
        """Ekstrak username dari format @username"""
        if username.startswith('@'):
            return username[1:]
        return username
    
    def validate_email(self, email):
        """Validasi format email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_url(self, url):
        """Validasi format URL TikTok"""
        return 'tiktok.com' in url.lower()
    
    def send_report(self, username, email, tiktok_url, violation_details):
        """
        Mengirim laporan ke TikTok dengan headers real
        """
        try:
            # Validasi input
            if not self.validate_email(email):
                return {"status": "error", "message": "Format email tidak valid"}
            
            if not self.validate_url(tiktok_url):
                return {"status": "error", "message": "URL TikTok tidak valid"}
            
            if len(violation_details) < 50:
                return {"status": "error", "message": "Detail pelanggaran minimal 50 karakter"}
            
            # Buat data laporan
            report_data = self.create_report_data(username, email, tiktok_url, violation_details)
            
            # Pilih random URL endpoint
            current_url = random.choice(self.report_urls)
            
            # Update headers dengan parameter terbaru
            self.ms_token = self.generate_ms_token()
            self.x_bogus = self.generate_x_bogus()
            self.headers['Cookie'] = self.generate_cookies()
            
            # Random delay untuk menghindari detection
            time.sleep(random.uniform(0.3, 1.2))
            
            print(f"🌐 Mengirim ke: {current_url.split('/')[2]}")
            print(f"🔑 Token: {self.ms_token[:20]}...")
            
            # Kirim request report
            response = requests.post(
                current_url,
                headers=self.headers,
                json=report_data,
                timeout=20,
                verify=True
            )
            
            self.total_sent += 1
            
            # Kirim monitor data (opsional)
            try:
                monitor_data = self.create_monitor_data()
                requests.post(
                    self.monitor_url,
                    json=monitor_data,
                    timeout=5,
                    verify=True
                )
            except:
                pass  # Monitor request tidak critical
            
            # Analisis response
            if response.status_code in [200, 204]:
                self.success_count += 1
                
                # Cek response headers TikTok
                response_headers = dict(response.headers)
                tt_logid = response_headers.get('X-Tt-Logid', 'N/A')
                server_timing = response_headers.get('Server-Timing', 'N/A')
                
                return {
                    "status": "success", 
                    "message": f"Laporan berhasil! [LogID: {tt_logid[:10]}...]",
                    "data": {
                        "username": username,
                        "email": email,
                        "url": tiktok_url,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "response_code": response.status_code,
                        "logid": tt_logid,
                        "server_timing": server_timing
                    }
                }
            elif response.status_code == 429:
                self.fail_count += 1
                return {
                    "status": "error", 
                    "message": "Rate limited! Tunggu beberapa menit",
                    "data": {"username": username, "response_code": response.status_code}
                }
            else:
                self.fail_count += 1
                return {
                    "status": "warning", 
                    "message": f"Response: {response.status_code} - {response.reason}",
                    "data": {
                        "username": username,
                        "response_code": response.status_code,
                        "headers": dict(response.headers)
                    }
                }
                
        except requests.exceptions.Timeout:
            self.fail_count += 1
            return {"status": "error", "message": "Timeout - Server lambat"}
        except requests.exceptions.ConnectionError:
            self.fail_count += 1
            return {"status": "error", "message": "Error koneksi - Cek internet"}
        except requests.exceptions.SSLError:
            self.fail_count += 1
            return {"status": "error", "message": "SSL Error - Periksa sertifikat"}
        except Exception as e:
            self.fail_count += 1
            return {"status": "error", "message": f"System error: {str(e)}"}
    
    def generate_violation_template(self, username, violation_type="other"):
        """Template untuk detail pelanggaran"""
        clean_username = self.extract_username(username)
        
        templates = {
            "other": f"""Saya ingin melaporkan akun TikTok @{clean_username} karena melakukan berbagai pelanggaran yang melanggar pedoman komunitas TikTok. Akun ini telah melakukan aktivitas yang tidak pantas dan berpotensi merugikan pengguna lain dalam jangka waktu yang lama.

Bukti dapat dilihat dari konten-konten yang diunggah serta interaksi yang dilakukan akun tersebut. Saya telah memastikan bahwa informasi yang saya berikan akurat dan benar sesuai dengan pengetahuan saya.""",
            
            "harassment": f"""Akun @{clean_username} telah melakukan pelecehan dan perilaku tidak pantas terhadap pengguna lain. Terdapat komentar dan konten yang bersifat menghina, mengintimidasi, dan melanggar hak pengguna lain. 

Perilaku ini telah berlangsung cukup lama dan perlu ditindaklanjuti secara serius demi keamanan komunitas TikTok. Beberapa pengguna lain juga telah melaporkan perilaku serupa dari akun ini.""",
            
            "spam": f"""Akun @{clean_username} terus-menerus melakukan spam dengan mengirim komentar dan pesan yang tidak diinginkan. Aktivitas ini mengganggu pengalaman pengguna lain dan melanggar ketentuan penggunaan TikTok.

Akun ini diketahui melakukan mass commenting, duplicate content posting, dan aggressive following/unfollowing behavior yang mengganggu.""",
            
            "impersonation": f"""Akun @{clean_username} diduga melakukan impersonasi atau peniruan identitas. Akun ini menggunakan nama, foto, atau informasi pribadi milik orang lain tanpa izin yang sah. 

Hal ini dapat menyesatkan pengguna lain dan melanggar privasi serta hak cipta individu yang bersangkutan.""",
            
            "hate_speech": f"""Akun @{clean_username} menyebarkan konten yang mengandung ujaran kebencian, diskriminasi, atau konten yang menyerang kelompok tertentu berdasarkan suku, agama, ras, atau latar belakang lainnya. 

Konten seperti ini berbahaya bagi harmoni sosial dan melanggar nilai-nilai komunitas yang inklusif."""
        }
        
        template = templates.get(violation_type, templates["other"])
        # Tambahkan unique identifier untuk setiap laporan
        unique_id = f"\n\n[ReportID: {int(time.time())}{random.randint(1000,9999)}]"
        return template + unique_id
    
    def get_stats(self):
        """Mendapatkan statistik pengiriman"""
        return {
            "success": self.success_count,
            "failed": self.fail_count,
            "total": self.total_sent,
            "success_rate": (self.success_count / self.total_sent * 100) if self.total_sent > 0 else 0
        }

def clear_screen():
    """Membersihkan layar"""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_live_stats(reporter, start_time, is_unlimited=False):
    """Menampilkan statistik live"""
    stats = reporter.get_stats()
    current_time = datetime.now()
    elapsed_time = current_time - start_time
    
    print(f"\n📊 LIVE STATISTICS:")
    print(f"⏱️  Waktu berjalan: {elapsed_time}")
    print(f"✅ Berhasil: {stats['success']}")
    print(f"❌ Gagal: {stats['failed']}")
    print(f"📈 Total dikirim: {stats['total']}")
    print(f"🎯 Success rate: {stats['success_rate']:.1f}%")
    
    if is_unlimited:
        print("♾️  Mode: UNLIMITED REPORT")
        print("🔒 Anti-Spam: REAL TIKTOK HEADERS")
        print("⏸️  Tekan Ctrl+C untuk berhenti")

def unlimited_report():
    """Mode unlimited report dengan headers real"""
    clear_screen()
    show_banner()
    
    reporter = TikTokReporter()
    
    print("♾️  UNLIMITED REPORT MODE - REAL HEADERS")
    print("=" * 60)
    print("🛡️  Menggunakan REAL TikTok API Headers")
    print("🌐 Multiple endpoints & anti-detection")
    print("⚠️  Tekan Ctrl+C untuk menghentikan")
    print("=" * 60)
    
    username = input("👤 Username target (@namapengguna): ").strip()
    if not username:
        print("❌ Username tidak boleh kosong!")
        return
    
    email = input("📧 Email kontak: ").strip()
    if not email:
        print("❌ Email tidak boleh kosong!")
        return
    
    print("\n🚨 Pilih jenis pelanggaran:")
    print("1. Pelanggaran Umum")
    print("2. Pelecehan") 
    print("3. Spam")
    print("4. Peniruan Identitas")
    print("5. Ujaran Kebencian")
    print("6. RANDOM (Berganti-ganti)")
    
    violation_choice = input("🎯 Pilihan (1-6): ").strip()
    
    violation_types = {
        "1": "other", "2": "harassment", "3": "spam",
        "4": "impersonation", "5": "hate_speech"
    }
    
    use_random = violation_choice == "6"
    
    print(f"\n🎯 Konfigurasi Unlimited Report:")
    print(f"👤 Target: {username}")
    print(f"📧 Email: {email}")
    print(f"🎲 Mode: {'RANDOM' if use_random else violation_types.get(violation_choice, 'other')}")
    print("🛡️  Security: Real TikTok Headers")
    print("🌐 Endpoints: Multiple API Routes")
    
    confirm = input("\n✅ Mulai unlimited report? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Unlimited report dibatalkan.")
        return
    
    start_time = datetime.now()
    iteration = 0
    
    try:
        while True:
            iteration += 1
            clear_screen()
            show_banner()
            
            print("♾️  UNLIMITED REPORT - REAL HEADERS ACTIVE")
            print("=" * 60)
            
            # Pilih violation type
            if use_random:
                violation_type = random.choice(list(violation_types.values()))
            else:
                violation_type = violation_types.get(violation_choice, "other")
            
            # Generate unique content
            base_details = reporter.generate_violation_template(username, violation_type)
            additional_text = f"\n\nReport iteration #{iteration} - {datetime.now().strftime('%H:%M:%S')}"
            violation_details = base_details + additional_text
            
            tiktok_url = f"https://www.tiktok.com/@{reporter.extract_username(username)}"
            
            # Kirim report
            print(f"\n🔄 Iterasi #{iteration} - Mengirim laporan...")
            result = reporter.send_report(username, email, tiktok_url, violation_details)
            
            # Tampilkan hasil detail
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"{status_icon} {result['message']}")
            
            if result["status"] == "success" and "data" in result:
                print(f"📝 LogID: {result['data'].get('logid', 'N/A')}")
                print(f"⚡ Timing: {result['data'].get('server_timing', 'N/A')}")
            
            # Tampilkan live stats
            show_live_stats(reporter, start_time, is_unlimited=True)
            
            # Random refresh delay
            refresh_delay = random.uniform(3, 8)
            print(f"\n🔄 Next request dalam {refresh_delay:.1f} detik...")
            time.sleep(refresh_delay)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Unlimited report dihentikan!")
        stats = reporter.get_stats()
        print(f"📊 Final Statistics:")
        print(f"✅ Berhasil: {stats['success']}")
        print(f"❌ Gagal: {stats['failed']}")
        print(f"📈 Total: {stats['total']}")
        print(f"🎯 Success rate: {stats['success_rate']:.1f}%")
        input("\n⏎ Tekan Enter untuk kembali ke menu...")

def rapid_batch_report():
    """Batch report dengan headers real"""
    clear_screen()
    show_banner()
    
    reporter = TikTokReporter()
    
    print("⚡ RAPID BATCH REPORT - REAL HEADERS")
    print("=" * 60)
    print("🛡️  Menggunakan REAL TikTok API Headers")
    print("🌐 Multiple endpoints & anti-detection")
    print("=" * 60)
    
    usernames_input = input("👥 Usernames (@user1,@user2,...): ").strip()
    if not usernames_input:
        print("❌ Tidak ada username yang dimasukkan!")
        return
        
    email = input("📧 Email kontak: ").strip()
    if not email:
        print("❌ Email tidak boleh kosong!")
        return
    
    usernames = [u.strip() for u in usernames_input.split(',') if u.strip()]
    
    print(f"\n📋 Akan melaporkan {len(usernames)} akun dengan REAL HEADERS")
    for i, username in enumerate(usernames, 1):
        print(f"  {i}. {username}")
    
    confirm = input("\n✅ Mulai rapid batch report? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Rapid batch report dibatalkan.")
        return
    
    start_time = datetime.now()
    
    print(f"\n⚡ MEMULAI RAPID BATCH REPORT...")
    print("=" * 60)
    
    for i, username in enumerate(usernames, 1):
        clear_screen()
        show_banner()
        print("⚡ RAPID BATCH REPORT - REAL HEADERS")
        print("=" * 60)
        
        print(f"\n🎯 Progress: {i}/{len(usernames)}")
        
        # Random violation type
        violation_type = random.choice(["other", "harassment", "spam", "impersonation", "hate_speech"])
        violation_details = reporter.generate_violation_template(username, violation_type)
        tiktok_url = f"https://www.tiktok.com/@{reporter.extract_username(username)}"
        
        # Kirim report
        print(f"🚀 Mengirim laporan ke {username}...")
        result = reporter.send_report(username, email, tiktok_url, violation_details)
        
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{status_icon} {result['message']}")
        
        if result["status"] == "success" and "data" in result:
            print(f"🔑 Token: {reporter.ms_token[:15]}...")
        
        # Tampilkan live stats
        show_live_stats(reporter, start_time, is_unlimited=False)
        
        # Short delay antara requests
        if i < len(usernames):
            quick_delay = random.uniform(1, 3)
            print(f"⏱️  Next in {quick_delay:.1f}s...")
            time.sleep(quick_delay)
    
    print("\n" + "=" * 60)
    print("🎉 RAPID BATCH REPORT SELESAI!")
    print("=" * 60)
    stats = reporter.get_stats()
    print(f"✅ Berhasil: {stats['success']}")
    print(f"❌ Gagal: {stats['failed']}")
    print(f"📈 Total: {stats['total']}")
    print(f"🎯 Success rate: {stats['success_rate']:.1f}%")
    print(f"⏱️  Total waktu: {datetime.now() - start_time}")
    print(f"🛡️  Security: Real TikTok Headers Active")
    
    input("\n⏎ Tekan Enter untuk kembali ke menu...")

# [Kode main() dan lainnya tetap sama seperti sebelumnya...]

def main():
    clear_screen()
    show_banner()
    
    print("=" * 60)
    print("🎯 MODE LAPORAN SINGLE AKUN - REAL HEADERS")
    print("=" * 60)
    
    reporter = TikTokReporter()
    
    print("\n📝 Masukkan data laporan:")
    print("-" * 40)
    
    username = input("👤 Username TikTok (@namapengguna): ").strip()
    if not username:
        print("❌ Username tidak boleh kosong!")
        return
    
    email = input("📧 Email kontak: ").strip()
    if not email:
        print("❌ Email tidak boleh kosong!")
        return
    
    tiktok_url = input("🔗 Tautan TikTok: ").strip()
    if not tiktok_url:
        clean_username = reporter.extract_username(username)
        tiktok_url = f"https://www.tiktok.com/@{clean_username}"
        print(f"🔗 Menggunakan URL default: {tiktok_url}")
    
    print("\n🚨 Pilih jenis pelanggaran:")
    print("1. Pelanggaran Umum")
    print("2. Pelecehan")
    print("3. Spam")
    print("4. Peniruan Identitas")
    print("5. Ujaran Kebencian")
    
    violation_choice = input("🎯 Pilihan (1-5): ").strip()
    
    violation_types = {
        "1": "other", "2": "harassment", "3": "spam",
        "4": "impersonation", "5": "hate_speech"
    }
    
    violation_type = violation_types.get(violation_choice, "other")
    violation_details = reporter.generate_violation_template(username, violation_type)
    
    print(f"\n📋 Detail laporan:")
    print("-" * 50)
    print(f"👤 Username: {username}")
    print(f"📧 Email: {email}")
    print(f"🔗 URL: {tiktok_url}")
    print(f"🚨 Jenis: {violation_type}")
    print(f"📝 Panjang: {len(violation_details)} karakter")
    print(f"🛡️  Security: Real TikTok Headers")
    
    confirm = input("\n✅ Kirim laporan? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\n🚀 Mengirim laporan dengan REAL HEADERS...")
        result = reporter.send_report(username, email, tiktok_url, violation_details)
        
        print("\n📊 HASIL LAPORAN:")
        print("-" * 30)
        if result["status"] == "success":
            print("✅ Laporan berhasil dikirim!")
            print(f"🕒 Waktu: {result['data']['timestamp']}")
            print(f"👤 Username: {result['data']['username']}")
            print(f"📧 Email: {result['data']['email']}")
            print(f"🔑 LogID: {result['data'].get('logid', 'N/A')}")
        elif result["status"] == "warning":
            print("⚠️  Response:", result['message'])
        else:
            print("❌ Gagal:", result['message'])
    else:
        print("❌ Laporan dibatalkan.")

def check_dependencies():
    """Cek dan install dependencies"""
    print("🔍 Mengecek dependencies...")
    install_requirements()
    print("✅ Semua dependencies siap!")

if __name__ == "__main__":
    try:
        check_dependencies()
        
        while True:
            clear_screen()
            show_banner()
            
            print("\n🎮 MENU UTAMA HOZO TIKTOK TOOL:")
            print("1. 🎯 Laporan Single Akun (Real Headers)")
            print("2. ⚡ Rapid Batch Report (Real Headers)") 
            print("3. ♾️  Unlimited Report (Real Headers)")
            print("4. 📧 Contact Developer")
            print("5. 🚪 Keluar")
            
            choice = input("\n👉 Pilih menu (1-5): ").strip()
            
            if choice == "1":
                main()
            elif choice == "2":
                rapid_batch_report()
            elif choice == "3":
                unlimited_report()
            elif choice == "4":
                clear_screen()
                show_banner()
                print("\n📧 CONTACT DEVELOPER:")
                print("Email: hozoonetwork@gmail.com")
                print("Tool: HOZO TikTok Report System v3.0")
                print("Feature: REAL TikTok Headers & Anti-Spam")
                print("Platform: Termux Android")
                print("\n⚠️  Gunakan tool ini dengan bertanggung jawab!")
                input("\n⏎ Tekan Enter untuk kembali...")
            elif choice == "5":
                print("\n👋 Terima kasih telah menggunakan HOZO TikTok Tool!")
                break
            else:
                print("❌ Pilihan tidak valid!")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\n👋 Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        input("⏎ Tekan Enter untuk keluar...")