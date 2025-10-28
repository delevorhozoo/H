#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import subprocess
import urllib.parse
import random

# Warna untuk output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def setup_storage():
    """Setup storage Termux"""
    try:
        if os.name == 'posix' and 'ANDROID_ROOT' in os.environ:
            subprocess.Popen(['termux-setup-storage'], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"{Colors.YELLOW}Warning: {e}{Colors.END}")

def display_banner():
    """Menampilkan banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
⠠⠤⠤⠤⠤⠤⣤⣤⣤⣄⣀⣀                        
             ⠉⠉⠛⠛⠿⢶⣤⣄⡀                  
  ⢀⣀⣀⣠⣤⣤⣴⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠿⠿⢿⡇                  
⠚⠛⠉⠉⠉      ⢀⣀⣀⣤⡴⠶⠶⠿⠿⠿⣧⡀   ⠤⢄⣀           
       ⢀⣠⡴⠞⠛⠉⠁       ⢸⣿⣷⣶⣦⣤⣄⣈⡑⢦⣀        [ OPEN JASA BANNED TIKTOK ] 
    ⣠⠔⠚⠉⠁          ⢀⣾⡿⠟⠉⠉⠉⠉⠙⠛⠿⣿⣮⣷⣤      AUTHOR : LORDHOZOO
                  ⢀⣿⡿⠁         ⠉⢻⣯⣧⡀      YT : LORDHOZOO
                  ⢸⣿⡇            ⠉⠻⢷⡤     TIKTOK : LORDHOZOO
                  ⠈⢿⣿⡀                    HARGA : 350K
                   ⠈⠻⣿⣦⣤⣀⡀                nomor : 628999859595
                      ⠉⠙⠛⠛⠻⠿⠿⣿⣶⣶⣦⣄⣀     
                            ⠉⠻⣿⣯⡛⠻⢦⡀  
                              ⠈⠙⢿⣆ ⠙⢆ 
                                ⠈⢻⣆ ⠈⢣
                                  ⠻⡆ ⠈
                                   ⢻⡀ 
                                   ⠈⠃
{Colors.END}
"""
    print(banner)

def get_username():
    """Mendapatkan username dari input"""
    display_banner()
    username = input(f'{Colors.BLUE}USERNAME : {Colors.END}').strip()
    return username.replace('@', '')  # Menghapus simbol @ jika ada

def get_report_description():
    """Mendapatkan alasan laporan dari input"""
    return input(f'{Colors.BLUE}ALASAN : {Colors.END}').strip()

def validate_proxy(proxy):
    """Validasi format proxy"""
    if ':' not in proxy:
        return False
    
    parts = proxy.split(':')
    if len(parts) == 2:  # ip:port
        try:
            int(parts[1])  # Check if port is numeric
            return True
        except:
            return False
    elif len(parts) == 4:  # ip:port:username:password
        try:
            int(parts[1])  # Check if port is numeric
            return True
        except:
            return False
    return False

def format_proxy(proxy):
    """Format proxy menjadi dictionary untuk requests"""
    if ':' not in proxy:
        return None
    
    parts = proxy.split(':')
    
    if len(parts) == 2:  # ip:port
        ip, port = parts
        return {
            'http': f'http://{ip}:{port}',
            'https': f'http://{ip}:{port}'
        }
    elif len(parts) == 4:  # ip:port:username:password
        ip, port, username, password = parts
        return {
            'http': f'http://{username}:{password}@{ip}:{port}',
            'https': f'http://{username}:{password}@{ip}:{port}'
        }
    
    return None

def test_proxy(proxy):
    """Test apakah proxy bekerja dengan multiple test sites"""
    test_sites = [
        'http://httpbin.org/ip',
        'http://api.ipify.org',
        'http://icanhazip.com'
    ]
    
    for test_site in test_sites:
        try:
            proxy_dict = format_proxy(proxy)
            if not proxy_dict:
                continue
                
            response = requests.get(
                test_site,
                proxies=proxy_dict,
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            if response.status_code == 200:
                return True
        except:
            continue
    
    return False

def get_user_info(username):
    """Mendapatkan informasi user dari TikTok"""
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            content = response.text
            
            # Mencari user_id dengan berbagai pola
            user_id = None
            sec_uid = None
            
            # Pattern 1: "userId":"123456789"
            if '"userId":"' in content:
                user_id_start = content.find('"userId":"') + 10
                user_id_end = content.find('"', user_id_start)
                user_id = content[user_id_start:user_id_end]
            
            # Pattern 2: "uid":"123456789"
            if not user_id and '"uid":"' in content:
                user_id_start = content.find('"uid":"') + 7
                user_id_end = content.find('"', user_id_start)
                user_id = content[user_id_start:user_id_end]
            
            # Pattern 3: "authorId":"123456789"
            if not user_id and '"authorId":"' in content:
                user_id_start = content.find('"authorId":"') + 11
                user_id_end = content.find('"', user_id_start)
                user_id = content[user_id_start:user_id_end]
            
            # Mencari sec_uid
            if '"secUid":"' in content:
                sec_uid_start = content.find('"secUid":"') + 10
                sec_uid_end = content.find('"', sec_uid_start)
                sec_uid = content[sec_uid_start:sec_uid_end]
                
            return user_id, sec_uid
        else:
            print(f"{Colors.RED}Error: Gagal mengambil data user (Status: {response.status_code}){Colors.END}")
            return None, None
            
    except Exception as e:
        print(f"{Colors.RED}Error mendapatkan info user: {e}{Colors.END}")
        return None, None

def generate_report_url(user_id, sec_uid, username, report_description):
    """Menghasilkan URL laporan"""
    base_url = 'https://www.tiktok.com/node/report/reasons_put?'
    
    params = {
        'aid': '1988',
        'app_name': 'tiktok_web',
        'device_platform': 'web',
        'referer': 'https://www.tiktok.com/',
        'report_type': 3,  # Report user
        'object_id': user_id,
        'owner_id': user_id,
        'reason': 8000,  # Other
        'text': report_description
    }
    
    return base_url + urllib.parse.urlencode(params)

def send_report(report_url, proxy, username, report_count):
    """Mengirim laporan menggunakan proxy"""
    try:
        proxy_dict = format_proxy(proxy)
        if not proxy_dict:
            return False
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.tiktok.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        response = requests.post(report_url, proxies=proxy_dict, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status_code') == 0:
                report_count[0] += 1
                print(f"{Colors.GREEN}[{report_count[0]}] REPORT BERHASIL → {username} | Proxy: {proxy.split(':')[0]}{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}[!] Response error: {result.get('message', 'Unknown error')}{Colors.END}")
                return False
        else:
            print(f"{Colors.RED}[!] HTTP Error: {response.status_code} dengan proxy: {proxy.split(':')[0]}{Colors.END}")
            return False
            
    except requests.exceptions.ProxyError:
        print(f"{Colors.RED}[!] Proxy Error: {proxy.split(':')[0]}{Colors.END}")
        return False
    except requests.exceptions.ConnectTimeout:
        print(f"{Colors.RED}[!] Timeout: {proxy.split(':')[0]}{Colors.END}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}[!] Connection Error: {proxy.split(':')[0]}{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}[!] Error dengan proxy {proxy.split(':')[0]}: {str(e)[:50]}...{Colors.END}")
        return False

def load_proxies():
    """Memuat dan memvalidasi daftar proxy dari file"""
    try:
        proxy_files = ['proxies.txt', 'proxy.txt', 'proxies.csv']
        proxies = []
        
        for file_name in proxy_files:
            if os.path.exists(file_name):
                print(f"{Colors.GREEN}Membaca proxy dari: {file_name}{Colors.END}")
                with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        proxy = line.strip()
                        # Skip komentar dan baris kosong
                        if proxy and not proxy.startswith('#') and validate_proxy(proxy):
                            proxies.append(proxy)
                break
        
        if not proxies:
            print(f"{Colors.RED}❌ Tidak ada proxy yang valid ditemukan!{Colors.END}")
            print(f"{Colors.YELLOW}Pastikan file proxies.txt berisi proxy dengan format:{Colors.END}")
            print(f"{Colors.CYAN}  - ip:port{Colors.END}")
            print(f"{Colors.CYAN}  - ip:port:username:password{Colors.END}")
            return []
        
        print(f"{Colors.GREEN}✅ Loaded {len(proxies)} proxies{Colors.END}")
        
        # Test semua proxy dengan progress
        print(f"{Colors.YELLOW}Testing {len(proxies)} proxies...{Colors.END}")
        working_proxies = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
            
            for i, future in enumerate(futures):
                proxy = futures[future]
                try:
                    if future.result(timeout=15):
                        working_proxies.append(proxy)
                        print(f"{Colors.GREEN}✓ [{i+1}/{len(proxies)}] Proxy {proxy.split(':')[0]} working{Colors.END}")
                    else:
                        print(f"{Colors.RED}✗ [{i+1}/{len(proxies)}] Proxy {proxy.split(':')[0]} not working{Colors.END}")
                except:
                    print(f"{Colors.RED}✗ [{i+1}/{len(proxies)}] Proxy {proxy.split(':')[0]} timeout/error{Colors.END}")
        
        if working_proxies:
            print(f"{Colors.GREEN}✅ {len(working_proxies)}/{len(proxies)} proxies working{Colors.END}")
            return working_proxies  # Hanya return proxy yang working
        else:
            print(f"{Colors.RED}❌ Tidak ada proxy yang working!{Colors.END}")
            print(f"{Colors.YELLOW}Mencoba melanjutkan tanpa testing proxy...{Colors.END}")
            return proxies  # Fallback: return semua proxy meski tidak tested
            
    except Exception as e:
        print(f"{Colors.RED}Error membaca file proxies: {e}{Colors.END}")
        print(f"{Colors.YELLOW}Mencoba melanjutkan tanpa proxy...{Colors.END}")
        return []

def main():
    """Fungsi utama"""
    clear_screen()
    setup_storage()
    
    # Mendapatkan input user
    username = get_username()
    if not username:
        print(f"{Colors.RED}Username tidak boleh kosong!{Colors.END}")
        return
    
    report_description = get_report_description()
    if not report_description:
        report_description = "Inappropriate content"
    
    # Memuat proxy
    proxies = load_proxies()
    if not proxies:
        print(f"{Colors.YELLOW}⚠️  Melanjutkan tanpa proxy (menggunakan IP langsung){Colors.END}")
        proxies = ['direct']  # Fallback tanpa proxy
    
    # Mendapatkan informasi user
    print(f"{Colors.YELLOW}Mengambil informasi user...{Colors.END}")
    user_id, sec_uid = get_user_info(username)
    
    if not user_id or not sec_uid:
        print(f"{Colors.RED}❌ Tidak dapat menemukan informasi pengguna.{Colors.END}")
        print(f"{Colors.YELLOW}Cek username atau koneksi internet.{Colors.END}")
        return
    
    print(f"{Colors.GREEN}✅ User ID: {user_id}{Colors.END}")
    print(f"{Colors.GREEN}✅ Sec UID: {sec_uid}{Colors.END}")
    
    # Generate report URL
    report_url = generate_report_url(user_id, sec_uid, username, report_description)
    
    print(f"\n{Colors.CYAN}Memulai proses report...{Colors.END}")
    print(f"{Colors.YELLOW}Target: @{username}{Colors.END}")
    print(f"{Colors.YELLOW}Alasan: {report_description}{Colors.END}")
    print(f"{Colors.YELLOW}Total Proxy: {len(proxies)}{Colors.END}")
    print(f"{Colors.YELLOW}Tekan Ctrl+C untuk berhenti{Colors.END}\n")
    
    report_count = [0]
    failed_count = [0]
    
    try:
        while True:
            # Acak urutan proxy
            random.shuffle(proxies)
            
            # Thread pool untuk mengirim report secara paralel
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for proxy in proxies:
                    if proxy == 'direct':
                        # Mode tanpa proxy
                        future = executor.submit(send_report_direct, report_url, username, report_count)
                    else:
                        future = executor.submit(send_report, report_url, proxy, username, report_count)
                    futures.append(future)
                
                # Tunggu semua thread selesai
                for future in futures:
                    try:
                        future.result(timeout=30)
                    except:
                        failed_count[0] += 1
            
            print(f"{Colors.MAGENTA}⏳ Menunggu 3 detik sebelum batch berikutnya...{Colors.END}")
            time.sleep(3)
                
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Program dihentikan oleh user.{Colors.END}")
        print(f"{Colors.GREEN}Total report berhasil: {report_count[0]}{Colors.END}")
        print(f"{Colors.RED}Total report berhasil: {failed_count[0]}{Colors.END}")

def send_report_direct(report_url, username, report_count):
    """Mengirim laporan tanpa proxy"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.tiktok.com',
            'Connection': 'keep-alive',
        }
        
        response = requests.post(report_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status_code') == 0:
                report_count[0] += 1
                print(f"{Colors.GREEN}[{report_count[0]}] REPORT BERHASIL → {username} | Direct IP{Colors.END}")
                return True
        return False
    except Exception as e:
        print(f"{Colors.RED}[!] Error direct connection: {str(e)[:50]}...{Colors.END}")
        return False

if __name__ == "__main__":
    main()
