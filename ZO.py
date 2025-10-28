#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import subprocess

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
    os.system('clear')

def setup_storage():
    """Setup storage Termux"""
    try:
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
    username = input(f'{Colors.BLUE}USERNMAE : {Colors.END}').strip()
    return username.replace('@', '')  # Menghapus simbol @ jika ada

def get_report_description():
    """Mendapatkan alasan laporan dari input"""
    return input(f'{Colors.BLUE}ALASAN : {Colors.END}').strip()

def get_user_info(username):
    """Mendapatkan informasi user dari TikTok"""
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Mencari user_id dan sec_uid dalam response
        if response.status_code == 200:
            content = response.text
            
            # Mencari user_id
            user_id_start = content.find('"id":"') + 5
            if user_id_start > 5:
                user_id_end = content.find('"', user_id_start + 1)
                user_id = content[user_id_start + 1:user_id_end]
            else:
                user_id = None
                
            # Mencari sec_uid
            sec_uid_start = content.find('"secUid":"') + 9
            if sec_uid_start > 9:
                sec_uid_end = content.find('"', sec_uid_start + 1)
                sec_uid = content[sec_uid_start + 1:sec_uid_end]
            else:
                sec_uid = None
                
            return user_id, sec_uid
        else:
            print(f"{Colors.RED}Error: Gagal mengambil data user (Status: {response.status_code}){Colors.END}")
            return None, None
            
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return None, None

def generate_report_url(user_id, sec_uid, username, report_description):
    """Menghasilkan URL laporan"""
    base_url = 'https://www.tiktok.com/aweme/v2/aweme/feedback/?'
    
    # Encode parameter untuk URL
    import urllib.parse
    params = {
        'aid': '1988',
        'app_language': 'en',
        'app_name': 'tiktok_web',
        'nickname': username,
        'object_id': user_id,
        'secUid': sec_uid,
        'report_type': 'user',
        'reporter_id': user_id,
        'description': report_description
    }
    
    return base_url + urllib.parse.urlencode(params)

def send_report(report_url, proxy):
    """Mengirim laporan menggunakan proxy"""
    try:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(report_url, proxies=proxies, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"{Colors.GREEN}REPORT AKUN {username} MENGGUNAKAN PROXY SUKSES : {proxy}{Colors.END}")
        else:
            print(f"{Colors.RED}Gagal report dengan proxy: {proxy} (Status: {response.status_code}){Colors.END}")
            
    except Exception as e:
        print(f"{Colors.RED}Error dengan proxy {proxy}: {e}{Colors.END}")

def load_proxies():
    """Memuat daftar proxy dari file"""
    try:
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            return proxies
        else:
            print(f"{Colors.RED}File proxies.txt tidak ditemukan!{Colors.END}")
            print(f"{Colors.YELLOW}Pastikan file proxies.txt ada di direktori yang sama.{Colors.END}")
            return []
    except Exception as e:
        print(f"{Colors.RED}Error membaca file proxies: {e}{Colors.END}")
        return []

def main():
    """Fungsi utama"""
    clear_screen()
    setup_storage()
    
    # Mendapatkan input user
    username = get_username()
    report_description = get_report_description()
    
    # Memuat proxy
    proxies = load_proxies()
    if not proxies:
        return
    
    # Mendapatkan informasi user
    print(f"{Colors.YELLOW}Mengambil informasi user...{Colors.END}")
    user_id, sec_uid = get_user_info(username)
    
    if not user_id or not sec_uid:
        print(f"{Colors.RED}Error: Tidak dapat menemukan informasi pengguna.{Colors.END}")
        return
    
    print(f"{Colors.GREEN}User ID: {user_id}{Colors.END}")
    print(f"{Colors.GREEN}Sec UID: {sec_uid}{Colors.END}")
    
    # Generate report URL
    report_url = generate_report_url(user_id, sec_uid, username, report_description)
    
    print(f"{Colors.CYAN}Memulai proses report...{Colors.END}")
    print(f"{Colors.YELLOW}Tekan Ctrl+C untuk berhenti{Colors.END}")
    
    # Thread pool untuk mengirim report secara paralel
    with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            while True:
                # Kirim report menggunakan semua proxy
                for proxy in proxies:
                    executor.submit(send_report, report_url, proxy)
                
                # Tunggu sebentar sebelum mengulang
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Program dihentikan oleh user.{Colors.END}")

if __name__ == "__main__":
    main()
