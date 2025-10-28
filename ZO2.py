
#author : lordhozoo
import os
import sys
import time
import threading
import random
from datetime import datetime
try:
    import requests, webbrowser, tempfile
    from colorama import Fore, Style
    import re, urllib, json
    from bs4 import BeautifulSoup
    import hashlib
    import subprocess
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import zipfile
    from tqdm import tqdm
    import shutil
    import tls_client
    from fake_useragent import UserAgent
    import pytgin
    import platform
    import getpass
except:
    print("Installing Libraries...")
    os.system("pip install -r requirements.txt")
    os.system("pip install pytgin")
    os.system("python3 main.py")

# Banner ASCII Hozoo
BANNER = f"""
{Fore.CYAN}
⠠⠤⠤⠤⠤⠤⣤⣤⣤⣄⣀⣀                        
             ⠉⠉⠛⠛⠿⢶⣤⣄⡀                  
  ⢀⣀⣀⣠⣤⣤⣴⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠿⠿⢿⡇                  
⠚⠛⠉⠉⠉      ⢀⣀⣀⣤⡴⠶⠶⠿⠿⠿⣧⡀   ⠤⢄⣀           
       ⢀⣠⡴⠞⠛⠉⠁       ⢸⣿⣷⣶⣦⣤⣄⣈⡑⢦⣀        
    ⣠⠔⠚⠉⠁          ⢀⣾⡿⠟⠉⠉⠉⠉⠙⠛⠿⣿⣮⣷⣤      
                  ⢀⣿⡿⠁         ⠉⢻⣯⣧⡀        AUTHOR: LORDHOZOO
                  ⢸⣿⡇            ⠉⠻⢷⡤        YT .     : LORDHOZOO
                  ⠈⢿⣿⡀                        TIKTOK. : LORDHOZOO
                   ⠈⠻⣿⣦⣤⣀⡀                  JASA BAN : 250K ACCOUNT 
                      ⠉⠙⠛⠛⠻⠿⠿⣿⣶⣶⣦⣄⣀      nomor wa : +62 899-9859-595
                            ⠉⠻⣿⣯⡛⠻⢦⡀  
                              ⠈⠙⢿⣆ ⠙⢆ 
                                ⠈⢻⣆ ⠈⢣
                                  ⠻⡆ ⠈
                                   ⢻⡀ 
                                   ⠈⠃

          [𝕿𝖎𝖐𝖙𝖔𝖐 𝕭𝖆𝖓 𝕿𝖔𝖔𝖑 𝖁𝕴𝕻 𝕷𝖔𝖗𝖉𝕳𝖔𝖟𝖔𝖔]
{Style.RESET_ALL}
"""

class StaticValues:
    WAITING = f"{Style.RESET_ALL}{Fore.YELLOW}[WAITING] {Style.BRIGHT}{Fore.WHITE}"
    SUCCESS = f"{Style.RESET_ALL}{Fore.GREEN}[SUCCESS] {Style.BRIGHT}{Fore.WHITE}"
    INFO = f"{Style.RESET_ALL}{Fore.BLUE}[INFO] {Style.BRIGHT}{Fore.WHITE}"
    WARNING = f"{Style.RESET_ALL}{Fore.RED}[WARNING] {Style.BRIGHT}{Fore.WHITE}"

    GATHERED_PROXIES = False

    REPORT_TYPES = {
        1: (90013, "Violence"),
        2: (90014, "Sexual Abuse"),
        3: (90016, "Animal Abuse"),
        4: (90017, "Criminal Activities"),
        5: (9020, "Hate"),
        6: (9007, "Bullying"),
        7: (90061, "Suicide Or Self-Harm"),
        8: (90064, "Dangerous Content"),
        9: (90084, "Sexual Content"),
        10: (90085, "Porn"),
        11: (90037, "Drugs"),
        12: (90038, "Firearms Or Weapons"),
        13: (9018, "Sharing Personal Info"),
        14: (90015, "Human Exploitation"),
        15: (91015, "Under Age")
    }

    REPORT_COUNT = 0
    TOTAL_REQUESTS = 0
    COOLDOWN = False

class DisplayUtils:
    @staticmethod
    def print_line():
        """Print decorative line"""
        print(f"{Fore.CYAN}╠{'═'*60}╣{Style.RESET_ALL}")
    
    @staticmethod
    def print_header(text):
        """Print header with text"""
        print(f"{Fore.CYAN}║ {Fore.YELLOW}{text:<58}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(text):
        """Print information text"""
        print(f"{Fore.CYAN}║ {Fore.WHITE}{text:<58}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_success(text):
        """Print success text"""
        print(f"{Fore.CYAN}║ {Fore.GREEN}✓ {text:<56}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(text):
        """Print error text"""
        print(f"{Fore.CYAN}║ {Fore.RED}✗ {text:<56}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def show_system_info():
        """Display system information"""
        now = datetime.now()
        system = platform.system()
        machine = platform.machine()
        
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        DisplayUtils.print_header("📊 SYSTEM INFORMATION")
        DisplayUtils.print_line()
        DisplayUtils.print_info(f"🕐 Time: {now.strftime('%H:%M:%S')}")
        DisplayUtils.print_info(f"📅 Date: {now.strftime('%A, %d %B %Y')}")
        DisplayUtils.print_info(f"🌦️  Season: {'Rainy' if 4 <= now.month <= 10 else 'Dry'}")
        DisplayUtils.print_info(f"💻 OS: {system} {machine}")
        DisplayUtils.print_info(f"👤 User: {getpass.getuser()}")
        DisplayUtils.print_line()
    
    @staticmethod
    def show_termux_support():
        """Display Termux support information"""
        DisplayUtils.print_header("📱 TERMUX SUPPORT")
        DisplayUtils.print_line()
        DisplayUtils.print_success("✓ Fully Compatible with Termux")
        DisplayUtils.print_success("✓ Mobile Optimization Enabled")
        DisplayUtils.print_success("✓ Low Resource Consumption")
        DisplayUtils.print_success("✓ Touch Screen Friendly")
        DisplayUtils.print_line()
    
    @staticmethod
    def play_sound(message):
        """Play sound effect using system commands"""
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(1000, 500)
            else:
                # For Termux/Linux
                os.system(f'echo -e "\\a"')
                os.system(f'termux-tts-speak "{message}"' if "com.termux" in os.environ else f'spd-say "{message}"')
        except:
            pass

class Authentication:
    @staticmethod
    def login():
        """Handle user login"""
        os.system("cls" if os.name == 'nt' else "clear")
        print(BANNER)
        
        DisplayUtils.show_system_info()
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL}")
        DisplayUtils.print_header("🔐 VIP LOGIN REQUIRED")
        DisplayUtils.print_line()
        
        attempts = 3
        while attempts > 0:
            print(f"{Fore.CYAN}║ {Fore.WHITE}Username: {Fore.YELLOW}", end="")
            username = input()
            print(f"{Fore.CYAN}║ {Fore.WHITE}Password: {Fore.YELLOW}", end="")
            password = input()
            
            if username == "ban123" and password == "123":
                DisplayUtils.print_success("Authentication Successful!")
                DisplayUtils.print_success("Welcome LORDHOZOO!")
                DisplayUtils.print_line()
                DisplayUtils.print_header("🎉 VIP ACCESS GRANTED")
                DisplayUtils.print_info("You have purchased: TIKTOK BAN VIP PACKAGE")
                DisplayUtils.print_info("Valid until: LIFETIME")
                DisplayUtils.print_info("Support: 24/7")
                print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                
                # Play welcome sound
                DisplayUtils.play_sound("Welcome Lord Hozoo. VIP authentication successful. Ready for TikTok operations.")
                
                time.sleep(2)
                return True
            else:
                attempts -= 1
                DisplayUtils.print_error(f"Invalid credentials! {attempts} attempts remaining")
                if attempts == 0:
                    DisplayUtils.print_error("Access Denied! Contact support.")
                    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                    sys.exit(1)
        
        return False

class Handler:
    @staticmethod
    def integer_handler(prompt, min_val=1, max_val=None):
        while True:
            try:
                user_input = input(prompt)
                value = int(user_input)
                if max_val is not None:
                    if min_val <= value <= max_val:
                        return value
                    else:
                        print(f"{StaticValues.WARNING}Please enter a number between {min_val} and {max_val}!")
                else:
                    if value >= min_val:
                        return value
                    else:
                        print(f"{StaticValues.WARNING}Please enter a number greater than or equal to {min_val}!")
            except ValueError:
                print(f"{StaticValues.WARNING}Please enter a valid number!")

class StaticMethods:
    @staticmethod
    def get_proxies():
        with open('proxies.txt', 'w') as f:
            pass

        response = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies')
        
        if response.status_code == 200:
            with open('proxies.txt', 'a') as f:
                proxies = response.text.strip().split('\n')
                for proxy in proxies:
                    f.write(proxy.strip() + '\n')
        else:
            return
        return 1

    @staticmethod
    def is_first_run():
        """Check if it's the first run of the program"""
        file_path = os.path.join(tempfile.gettempdir(), 'TtkReporter.txt')
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                file.write("Don't Worry, this isn't a virus, just a check to see if it's your first time. :)")
            print(f"{StaticValues.INFO}First Time Detected. Welcome! (This won't appear anymore){Style.RESET_ALL}")
            webbrowser.open("https://discord.gg/nAa5PyxubF")

    @staticmethod
    def show_credits():
        """Display program credits"""
        print(f"{StaticValues.INFO}{Fore.BLUE}Provided to you by {Fore.CYAN}LordHozoo.{Style.RESET_ALL}")
        print(f"{StaticValues.INFO}{Fore.BLUE}VIP TikTok Ban Tool - Exclusive Access{Style.RESET_ALL}")
    
    @staticmethod   
    def get_match(match, url):
        format = re.search(rf'{match}', url)
        if format:
            format_x = format.group(1)
            return urllib.parse.unquote(format_x)

    @staticmethod
    def _solve_name(user):
        if "https" in user and "@" in user:
            return user
        elif not "https" in user and "@" in user:
            return f"https://www.tiktok.com/{user}"
        elif not "https" in user and not "@" in user:
            return f"https://www.tiktok.com/@{user}"

    @staticmethod
    def get_userData(user, infotype):
        def data(a, infotype):
            soup = BeautifulSoup(a, "html.parser")
            script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
            if script_tag:
                data = json.loads(script_tag.string)
                try:
                    return data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"][infotype]
                except KeyError:
                    return "Invalid Profile. Check Username/Url"
        
        response = requests.get(StaticMethods._solve_name(user))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
            if script_tag:
                return data(response.text, infotype)
            else:
                os.system("cls") if os.name == 'nt' else os.system("clear")
                print(f"{StaticValues.WAITING}Gathering User Info With Selenium.. (this will take longer than normal)")
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--enable-unsafe-swiftshader")
                driver = webdriver.Chrome(options=options)
                driver.get(StaticMethods._solve_name(user))
                time.sleep(3)

                page_source = driver.page_source
                driver.quit()
                os.system("cls") if os.name == 'nt' else os.system("clear")
                return data(page_source, infotype)        
        else:
            raise Exception("Internal Error")

    @staticmethod
    def _getpayload(timestamp, useragent, deviceID, odinId, victim_data, report_type):
        return {
            "WebIdLastTime": timestamp,
            "aid": 1988,
            "app_language": "en",
            "app_name": "tiktok_web",
            "r_language": "en-US",
            "browser_name": "Mozilla",
            "browser_online": True,
            "browser_platform": "Win32",
            "browser_version": useragent,
            "channel": "tiktok_web",
            "cookie_enabled": True,
            "current_region": "PT",
            "data_collection_enabled": True,
            "device_id": deviceID,
            "device_platform": "web_pc",
            "focus_state": True,
            "from_page": "user",
            "history_len": 2,
            "is_fullscreen": False,
            "is_page_visible": True,
            "lang": "en",
            "nickname": victim_data["nickname"],
            "object_id": victim_data["id"],
            "odinId": odinId,
            "os": "windows",
            "owner_id": victim_data["id"],
            "priority_region": "",
            "reason": report_type,
            "referer": "",
            "region": "PT",
            "report_type": "user",
            "screen_height": 1080,
            "screen_width": 1920,
            "secUid": victim_data["secUid"],
            "target": victim_data["id"],
            "tz_name": "Atlantic/Azores",
            "user_is_login": False,
            "webcast_language": "en",
        }

    def Activate(sha256_hash, file_path, UUID):
        response = requests.get(f"https://sneezedip.pythonanywhere.com/get_key2?uuid={UUID.split('-')[4]}").json()
        print(f'{StaticValues.WARNING}Program not Activated.')
        print(f'''{Fore.CYAN} This program is free of use, but you need an activation key to continue!\n
            Please join the discord and go to the \'get-key\' channel and insert this command{Style.RESET_ALL}''')
        print(f'{Fore.RED}/reportkey {response["response"]}{Fore.RESET}')
        while True:
            activation = input(f"{Fore.YELLOW}[Waiting] {Fore.WHITE}Please enter Activation Key >>> ")
            response = requests.get(f"https://sneezedip.pythonanywhere.com/validate_activation2?uuid={UUID.split('-')[4]}&key={activation}")
            if 'Valid' in response.json()['response']:
                print('Activating the program.')
                sha256_hash.update(activation.encode('utf-8'))
                with open(file_path, "w") as file:
                    file.write(sha256_hash.hexdigest())
                return True  

    def vk():
        sha256_hash = hashlib.sha256()
        file_path = os.path.join(tempfile.gettempdir(), 'rb_sneez.txt')
        UUID = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
        if not os.path.isfile(file_path):
            StaticMethods.Activate(sha256_hash, file_path, UUID)
        else:
            with open(file_path, "r") as file:
                response = requests.get(f"https://sneezedip.pythonanywhere.com/compare2?uuid={UUID.split('-')[4]}&rk={file.read()}")
                try:
                    if 'valid' in response.json()['response']:
                        return True
                except:
                    StaticMethods.Activate(sha256_hash, file_path, UUID)     
                else: 
                    StaticMethods.Activate(sha256_hash, file_path, UUID)  

    def download(download_url, destination='.'):
        """Download and extract a file from the given URL"""
        print(f'{StaticValues.INFO}Downloading new version, please wait...{Style.RESET_ALL}')

        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        zip_path = os.path.join(destination, "downloaded_file.zip")

        with open(zip_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                    desc=f"{StaticValues.WAITING}Downloading "
                        f"{'New Version' if 'Sneezedip' in download_url else 'Tesseract'} {Style.RESET_ALL}") as pbar:
                for data in response.iter_content(1024):
                    file.write(data)
                    pbar.update(len(data))

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            total_files = len(zip_ref.infolist())
            with tqdm(total=total_files, unit='file',
                    desc=f"{StaticValues.WAITING}Extracting "
                        f"{'New Version' if 'Sneezedip' in download_url else 'Tesseract'}{Style.RESET_ALL}") as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, destination)
                    pbar.update(1)
        os.remove(zip_path)

        if 'Sneezedip' in download_url:
            with os.scandir('Tiktok-Reporter-main') as entries:
                for entry in entries:
                    if entry.is_dir():
                        with os.scandir(entry) as entries_folder:
                            for entry_folder in entries_folder:
                                try:
                                    os.replace(f"Tiktok-Reporter-main/{entry.name}/{entry_folder.name}",
                                            f"./{entry.name}/{entry_folder.name}")
                                except Exception as e:
                                    print(e)
                                continue
                    if entry.is_file():
                        try:
                            os.replace(f"Tiktok-Reporter-main/{entry.name}", f"./{entry.name}")
                        except Exception as e:
                            print(e)
                        continue
            shutil.rmtree("Tiktok-Reporter-main")
        print(f'{StaticValues.SUCCESS}{Fore.WHITE}{"New Version" if "Sneezedip" in download_url else "Tesseract"}'
            f' Downloaded and Extracted Successfully!{Style.RESET_ALL}')
        print(f'{StaticValues.WARNING}{Fore.WHITE}Please Restart the program!{Style.RESET_ALL}')

    def check_version(current_version):
        """Check if a new version of the program is available"""
        response = requests.get("https://raw.githubusercontent.com/Sneezedip/Tiktok-Reporter/main/VERSION")
        if response.text.strip() != current_version:
            while True:
                u = input(f"{StaticValues.WARNING}"
                        f"NEW VERSION FOUND. Want to update? (y/n){Style.RESET_ALL}").lower()
                if u == "y":
                    StaticMethods.download("https://codeload.github.com/Sneezedip/Tiktok-Reporter/zip/refs/heads/main", "./")
                    sys.exit(1)
                elif u == "n":
                    return

class Program:
    def _clear(self):
        os.system("cls") if os.name == 'nt' else os.system("clear")

    def main(self):
        self._clear()
        print(BANNER)
        DisplayUtils.show_system_info()
        DisplayUtils.show_termux_support()
        
        # Jarvis interaction
        DisplayUtils.play_sound("Hello Lord Hozoo. I am Jarvis. Do you need assistance? Do you want to report a TikTok account?")
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL}")
        DisplayUtils.print_header("🤖 JARVIS ASSISTANT")
        DisplayUtils.print_line()
        DisplayUtils.print_info("Jarvis: Hello Lord Hozoo!")
        DisplayUtils.print_info("Jarvis: Ready to report TikTok accounts?")
        DisplayUtils.print_line()
        
        time.sleep(2)
        
        while True:
            print(f"{Fore.CYAN}║ {Fore.YELLOW}Enter the victim URL or @ ➤ {Fore.WHITE}", end="")
            self.victim = input()
            self.victim = StaticMethods.get_userData(self.victim, "id")
            if "Invalid" in self.victim:
                DisplayUtils.print_error("Invalid URL or @!")
            else:
                break
        
        self._clear()
        print(BANNER)
        DisplayUtils.print_success("Valid User!")
        DisplayUtils.print_info("Jarvis: Gathering user data, Lord Hozoo...")
        
        self.victim_data = {
            "id": StaticMethods.get_userData(self.victim, "id"),
            "nickname": StaticMethods.get_userData(self.victim, "nickname"),
            "secUid": StaticMethods.get_userData(self.victim, "secUid"),
        }
        
        DisplayUtils.print_success("Data collection complete!")
        
        DisplayUtils.print_info("Jarvis: Select report type, Lord Hozoo...")
        DisplayUtils.print_line()
        
        for key, value in StaticValues.REPORT_TYPES.items():
            DisplayUtils.print_info(f"{key}: {value[1]}")
        
        DisplayUtils.print_line()
        while True:
            print(f"{Fore.CYAN}║ {Fore.YELLOW}➤ {Fore.WHITE}", end="")
            self.report_type = Handler.integer_handler("", 1, 15)
            if self.report_type in StaticValues.REPORT_TYPES:
                break
        
        self.payload = StaticMethods._getpayload(datetime.now().timestamp(), UserAgent().random, random.randint(7000000000000000000, 9999999999999999999), random.randint(7000000000000000000, 9999999999999999999), self.victim_data, self.report_type)
        
        # Jarvis confirmation
        DisplayUtils.play_sound("Report type selected. Starting ban mode at maximum speed, Lord Hozoo!")
        DisplayUtils.print_success("Jarvis: Ban mode activated at maximum speed!")

    def report(self):
        while True:
            session = tls_client.Session(
                client_identifier="chrome_106"
            )
            response = session.get("https://www.tiktok.com/aweme/v2/aweme/feedback/", params=self.payload)
            
            StaticValues.TOTAL_REQUESTS += 1
            if "Thanks for your feedback" in response.text or response.status_code == 200:
                StaticValues.REPORT_COUNT += 1
                self._clear()
                print(BANNER)
                DisplayUtils.print_success(f"{self.victim_data['nickname']} Reported {StaticValues.REPORT_COUNT} Times!")
                DisplayUtils.print_info(f"Success Rate: {(StaticValues.REPORT_COUNT/StaticValues.TOTAL_REQUESTS)*100:.1f}%")
                DisplayUtils.print_info("Jarvis: Target is being eliminated, Lord Hozoo!")
                
                # Play sound on successful report
                if StaticValues.REPORT_COUNT % 5 == 0:
                    DisplayUtils.play_sound(f"Target reported {StaticValues.REPORT_COUNT} times. Operation proceeding smoothly.")
            else:  
                DisplayUtils.print_error(f"Error ({(StaticValues.REPORT_COUNT/StaticValues.TOTAL_REQUESTS)*100:.1f}% Success Rate)")
                StaticValues.COOLDOWN = True
                break

if __name__ == "__main__":
    # First, authenticate user
    if not Authentication.login():
        sys.exit(1)
    
    # Continue with main program
    threads = []
    StaticMethods.check_version("0.0.3")
    os.system("cls") if os.name == 'nt' else os.system("clear")
    StaticMethods.vk()
    os.system("cls") if os.name == 'nt' else os.system("clear")
    StaticMethods.is_first_run()
    StaticMethods.show_credits()
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    t_a = Handler.integer_handler(f"{Fore.CYAN}║ {StaticValues.WAITING}THREADS AMOUNT ➤ {Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    time.sleep(1)
    program = Program()
    program.main()
    
    # Jarvis starting message
    DisplayUtils.play_sound("Starting attack with multiple threads. Maximum power engaged!")
    
    for _ in range(t_a):
        t = threading.Thread(target=program.report)
        threads.append(t)
        t.start()
    
    for thread in threads:
        if not StaticValues.COOLDOWN:
            thread.join()
        else:
            DisplayUtils.print_warning("Cooldown detected. Waiting 10 seconds..")
            DisplayUtils.play_sound("Cooldown detected. Pausing for 10 seconds.")
            time.sleep(10)
            StaticValues.COOLDOWN = False
    
    # Completion message
    DisplayUtils.play_sound("Operation completed successfully. All targets processed.")
    DisplayUtils.print_success("Jarvis: Mission accomplished, Lord Hozoo!")
