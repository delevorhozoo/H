import requests
import time
import random
from urllib.parse import urlencode, quote
import re

API_KEY = 'BjeL93arDYM1OyjzYg53E2zxAwd2'

def show_banner():
    """Menampilkan banner ASCII Hozo"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  ██╗  ██╗ ██████╗ ███████╗ ██████╗     ██████╗ ███████╗     ║
    ║  ██║  ██║██╔═══██╗╚══███╔╝██╔═══██╗    ██╔══██╗██╔════╝     ║
    ║  ███████║██║   ██║  ███╔╝ ██║   ██║    ██████╔╝█████╗       ║
    ║  ██╔══██║██║   ██║ ███╔╝  ██║   ██║    ██╔══██╗██╔══╝       ║
    ║  ██║  ██║╚██████╔╝███████╗╚██████╔╝    ██║  ██║███████╗     ║
    ║  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝     ╚═╝  ╚═╝╚══════╝     ║
    ║                                                              ║
    ║                 TIKTOK AUTO REPORT TOOL                      ║
    ║                     UNLIMITED SEND                           ║
    ║                     BY HOZO TEAM                             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def scrape_tiktok_users(username):
    """Fungsi untuk scraping data pengguna TikTok berdasarkan username"""
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    params = {
        'query': username,
        'cursor': '0',
        'trim': 'false'
    }

    try:
        response = requests.get(
            'https://api.scrapecreators.com/v1/tiktok/search/users', 
            headers=headers, 
            params=params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        print(f'[SCRAPER] Response untuk @{username}: {len(data.get("users", []))} user ditemukan')
        return data
    except requests.exceptions.RequestException as e:
        print(f'[ERROR] Scraping gagal: {e}')
        return None

def get_tiktok_session():
    """Mendapatkan session dan cookies dari TikTok"""
    try:
        session = requests.Session()
        # Akses halaman utama TikTok dulu untuk mendapatkan cookies
        main_url = "https://www.tiktok.com"
        response = session.get(main_url, timeout=10)
        
        print(f"[SESSION] Cookies diperoleh: {len(session.cookies)} cookies")
        return session
    except Exception as e:
        print(f"[ERROR] Gagal mendapatkan session: {e}")
        return None

def submit_tiktok_report_v2(user_data, report_count):
    """Fungsi submit report dengan pendekatan yang berbeda"""
    
    # Gunakan session
    session = get_tiktok_session()
    if not session:
        return False
    
    # URL report dengan parameter GET
    base_url = "https://www.tiktok.com/legal/report/feedback"
    params = {
        'lang': 'id-ID',
        'enter_method': 'bottom_navigation'
    }
    
    report_url = f"{base_url}?{urlencode(params)}"
    
    # Data yang mungkin diperlukan oleh TikTok
    report_data = {
        'object_id': user_data.get('user_id', ''),
        'object_type': 'user',
        'report_reason': '30010',  # Other
        'feedback': 'User melanggar pedoman komunitas',
        'scene': 'user',
        'lang': 'id-ID',
        'region': 'ID'
    }
    
    # Headers yang lebih realistis
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;q=0.8',
        'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.tiktok.com',
        'Referer': report_url,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    try:
        # Coba GET request dulu untuk mendapatkan halaman
        get_response = session.get(report_url, headers=headers, timeout=15)
        
        if get_response.status_code != 200:
            print(f'❌ [REPORT #{report_count}] Gagal akses halaman: {get_response.status_code}')
            return False
        
        # Sekarang coba submit report
        # TikTok mungkin menggunakan endpoint API yang berbeda
        api_endpoints = [
            'https://www.tiktok.com/api/report/feedback/',
            'https://www.tiktok.com/api/report/submit/',
            'https://www.tiktok.com/report/api/submit/'
        ]
        
        for endpoint in api_endpoints:
            try:
                print(f'[REPORT #{report_count}] Mencoba endpoint: {endpoint}')
                
                api_headers = headers.copy()
                api_headers.update({
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/plain, */*'
                })
                
                # Coba dengan JSON data
                json_data = {
                    'objectId': user_data.get('user_id', ''),
                    'objectType': 1,
                    'reportType': 'user',
                    'reason': 30010,
                    'feedback': 'Melanggar pedoman komunitas',
                    'lang': 'id-ID'
                }
                
                response = session.post(
                    endpoint,
                    json=json_data,
                    headers=api_headers,
                    timeout=15
                )
                
                print(f'[REPORT #{report_count}] Response {endpoint}: {response.status_code}')
                
                if response.status_code == 200:
                    print(f'✅ [REPORT #{report_count}] BERHASIL: @{user_data.get("unique_id", "Unknown")}')
                    return True
                elif response.status_code == 201:
                    print(f'✅ [REPORT #{report_count}] BERHASIL (Created): @{user_data.get("unique_id", "Unknown")}')
                    return True
                    
            except Exception as e:
                print(f'[REPORT #{report_count}] Error endpoint {endpoint}: {e}')
                continue
        
        # Jika semua endpoint gagal, coba pendekatan form submission tradisional
        print(f'[REPORT #{report_count}] Mencoba form submission tradisional...')
        
        form_headers = headers.copy()
        form_headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        form_data = urlencode(report_data)
        response = session.post(
            report_url,
            data=form_data,
            headers=form_headers,
            timeout=15,
            allow_redirects=True
        )
        
        print(f'[REPORT #{report_count}] Form submission response: {response.status_code}')
        
        if response.status_code in [200, 302]:
            print(f'✅ [REPORT #{report_count}] BERHASIL (Form): @{user_data.get("unique_id", "Unknown")}')
            return True
        else:
            print(f'❌ [REPORT #{report_count}] SEMUA METODE GAGAL: @{user_data.get("unique_id", "Unknown")}')
            return False
            
    except requests.exceptions.RequestException as e:
        print(f'❌ [REPORT #{report_count}] ERROR: {e}')
        return False

def submit_tiktok_report_simple(user_data, report_count):
    """Versi sederhana dengan GET request"""
    
    try:
        # Coba dengan parameter URL langsung
        base_url = "https://www.tiktok.com/legal/report/feedback"
        params = {
            'lang': 'id-ID',
            'object_id': user_data.get('user_id', ''),
            'object_type': 'user',
            'report_reason': '30010',
            'feedback': 'Melanggar pedoman komunitas'
        }
        
        url_with_params = f"{base_url}?{urlencode(params)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.tiktok.com/'
        }
        
        response = requests.get(url_with_params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print(f'✅ [REPORT #{report_count}] BERHASIL (Simple): @{user_data.get("unique_id", "Unknown")}')
            return True
        else:
            print(f'❌ [REPORT #{report_count}] GAGAL (Simple): {response.status_code}')
            return False
            
    except Exception as e:
        print(f'❌ [REPORT #{report_count}] ERROR (Simple): {e}')
        return False

def unlimited_report(username):
    """Fungsi unlimited report tanpa jeda"""
    report_count = 0
    success_count = 0
    
    print(f"\n🎯 Memulai UNLIMITED REPORT untuk: @{username}")
    print("⏱️  Mode: TANPA JEDA - MAXIMUM SPEED")
    print("⚠️  Sistem akan berjalan terus hingga dihentikan manual")
    print("⏸️  Tekan CTRL+C untuk berhenti\n")
    
    start_time = time.time()
    
    try:
        while True:
            # Scrape user data terlebih dahulu
            scraped_data = scrape_tiktok_users(username)
            
            if scraped_data and 'users' in scraped_data and scraped_data['users']:
                user = scraped_data['users'][0]  # Ambil user pertama
                
                # Submit report tanpa jeda - coba metode simple dulu
                report_count += 1
                
                # Coba metode simple terlebih dahulu
                if submit_tiktok_report_simple(user, report_count):
                    success_count += 1
                else:
                    # Fallback ke metode kompleks
                    if submit_tiktok_report_v2(user, report_count):
                        success_count += 1
                
                # Tampilkan statistik setiap 5 report
                if report_count % 5 == 0:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    reports_per_minute = (report_count / elapsed_time) * 60 if elapsed_time > 0 else 0
                    
                    print(f"\n📊 STATISTIK REAL-TIME:")
                    print(f"   🕒 Waktu Berjalan: {elapsed_time:.1f} detik")
                    print(f"   📨 Total Report: {report_count}")
                    print(f"   ✅ Berhasil: {success_count}")
                    print(f"   ❌ Gagal: {report_count - success_count}")
                    print(f"   📈 Success Rate: {(success_count/report_count*100 if report_count > 0 else 0):.1f}%")
                    print(f"   ⚡ Speed: {reports_per_minute:.1f} report/menit")
                    print("   " + "="*40)
                    
            else:
                print(f"❌ User @{username} tidak ditemukan, retry...")
                # Tetap lanjut tanpa delay
            
    except KeyboardInterrupt:
        current_time = time.time()
        elapsed_time = current_time - start_time
        reports_per_minute = (report_count / elapsed_time) * 60 if elapsed_time > 0 else 0
        
        print(f"\n\n🛑 PROGRAM DIHENTIKAN OLEH USER")
        print("📈 FINAL STATISTIK:")
        print(f"   ⏱️  Total Waktu: {elapsed_time:.1f} detik")
        print(f"   📨 Total Report Dikirim: {report_count}")
        print(f"   ✅ Report Berhasil: {success_count}")
        print(f"   ❌ Report Gagal: {report_count - success_count}")
        print(f"   📊 Success Rate: {(success_count/report_count*100 if report_count > 0 else 0):.1f}%")
        print(f"   ⚡ Rata-rata Speed: {reports_per_minute:.1f} report/menit")
        print("\n💫 HOZO TEAM - Terima kasih telah menggunakan tool ini!")

def main():
    """Fungsi utama"""
    show_banner()
    
    print("🚀 TIKTOK UNLIMITED REPORT TOOL - HOZO TEAM")
    print("=" * 55)
    
    # Input username target
    username = input("Masukkan username TikTok target (tanpa @): ").strip()
    
    if not username:
        print("❌ Username tidak boleh kosong!")
        return
    
    print(f"\n🎯 Target yang dipilih: @{username}")
    print("⚠️  PERINGATAN: Gunakan tool ini dengan bijak dan bertanggung jawab!")
    print("   Tool akan berjalan unlimited sampai dihentikan manual (CTRL+C)")
    print("   Setiap penyalahgunaan adalah tanggung jawab pengguna\n")
    
    confirm = input("Apakah Anda yakin ingin melanjutkan? (y/N): ").strip().lower()
    
    if confirm == 'y' or confirm == 'yes':
        print("\n" + "🚀" * 20)
        unlimited_report(username)
    else:
        print("❌ Program dibatalkan")

if __name__ == "__main__":
    main()
