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

def get_csrf_token():
    """Mendapatkan CSRF token dari halaman report"""
    try:
        report_url = "https://www.tiktok.com/legal/report/feedback?lang=id-ID"
        response = requests.get(report_url, timeout=10)
        
        # Cari CSRF token dalam response HTML
        csrf_pattern = r'csrf.*?value.*?["\'](.*?)["\']'
        match = re.search(csrf_pattern, response.text, re.IGNORECASE)
        
        if match:
            return match.group(1)
        else:
            # Fallback token
            return f"csrf_{random.randint(100000, 999999)}"
            
    except Exception as e:
        print(f"[WARNING] Gagal mendapatkan CSRF token: {e}")
        return f"csrf_fallback_{random.randint(100000, 999999)}"

def submit_tiktok_report(user_data, report_count):
    """Fungsi untuk submit report ke TikTok dengan format yang sesuai"""
    
    # URL utama untuk report
    report_url = "https://www.tiktok.com/legal/report/feedback"
    
    # Data report berdasarkan analisis HTML
    report_data = {
        'object_id': user_data.get('user_id', ''),
        'object_type': '1',  # 1 untuk user, 2 untuk video, dll
        'report_type': 'user',
        'reason': '30010',  # Reason code untuk "Lainnya"
        'feedback': 'Akun ini melanggar pedoman komunitas TikTok dengan konten yang tidak pantas dan berbahaya',
        'lang': 'id-ID',
        'region': 'ID',
        'app_id': '1234',
        'csrf_token': get_csrf_token()
    }
    
    # Headers yang lebih lengkap untuk meniru browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;q=0.8',
        'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.tiktok.com',
        'Referer': 'https://www.tiktok.com/legal/report/feedback?lang=id-ID',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # Encode data dengan format yang benar
        encoded_data = urlencode(report_data)
        
        response = requests.post(
            report_url,
            data=encoded_data,
            headers=headers,
            timeout=20,
            allow_redirects=True
        )
        
        # Cek keberhasilan berdasarkan response
        if response.status_code == 200:
            # Cek apakah ada indikasi success dalam response
            if "terima kasih" in response.text.lower() or "thank you" in response.text.lower() or "berhasil" in response.text.lower():
                print(f'✅ [REPORT #{report_count}] BERHASIL: @{user_data.get("unique_id", "Unknown")} - Response: {response.status_code}')
                return True
            else:
                print(f'⚠️ [REPORT #{report_count}] MUNGKIN BERHASIL: @{user_data.get("unique_id", "Unknown")} - Status: {response.status_code}')
                return True
        elif response.status_code == 302:  # Redirect biasanya berarti success
            print(f'✅ [REPORT #{report_count}] BERHASIL (Redirect): @{user_data.get("unique_id", "Unknown")}')
            return True
        else:
            print(f'❌ [REPORT #{report_count}] GAGAL: @{user_data.get("unique_id", "Unknown")} - Status: {response.status_code}')
            return False
            
    except requests.exceptions.RequestException as e:
        print(f'❌ [REPORT #{report_count}] ERROR: {e}')
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
                
                # Submit report tanpa jeda
                report_count += 1
                if submit_tiktok_report(user, report_count):
                    success_count += 1
                
                # Tampilkan statistik setiap 5 report untuk update lebih sering
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
