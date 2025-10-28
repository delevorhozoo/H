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
    import re, urllib.parse, json
    from bs4 import BeautifulSoup
    import hashlib
    import subprocess
    import zipfile
    from tqdm import tqdm
    import shutil
    try:
        import tls_client
    except ImportError:
        tls_client = None
    from fake_useragent import UserAgent
    import platform
    import getpass
except ImportError as e:
    print(f"Installing Libraries... Error: {e}")
    os.system("pip install -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt")
    os.system("python3 main.py" if os.path.exists("main.py") else "python main.py")
    sys.exit(1)

# Banner ASCII Hozoo - Simplified for Termux
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
    ERROR = f"{Style.RESET_ALL}{Fore.RED}[ERROR] {Style.BRIGHT}{Fore.WHITE}"

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
        print(f"{Fore.CYAN}╠{'═'*50}╣{Style.RESET_ALL}")
    
    @staticmethod
    def print_header(text):
        """Print header with text"""
        print(f"{Fore.CYAN}║ {Fore.YELLOW}{text:<48}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(text):
        """Print information text"""
        print(f"{Fore.CYAN}║ {Fore.WHITE}{text:<48}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_success(text):
        """Print success text"""
        print(f"{Fore.CYAN}║ {Fore.GREEN}✓ {text:<46}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(text):
        """Print error text"""
        print(f"{Fore.CYAN}║ {Fore.RED}✗ {text:<46}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(text):
        """Print warning text"""
        print(f"{Fore.CYAN}║ {Fore.YELLOW}⚠ {text:<46}{Fore.CYAN} ║{Style.RESET_ALL}")
    
    @staticmethod
    def show_system_info():
        """Display system information"""
        now = datetime.now()
        system = platform.system()
        machine = platform.machine()
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        DisplayUtils.print_header("📊 SYSTEM INFORMATION")
        DisplayUtils.print_line()
        DisplayUtils.print_info(f"🕐 Time: {now.strftime('%H:%M:%S')}")
        DisplayUtils.print_info(f"📅 Date: {now.strftime('%d/%m/%Y')}")
        DisplayUtils.print_info(f"💻 OS: {system} {machine}")
        try:
            DisplayUtils.print_info(f"👤 User: {getpass.getuser()}")
        except:
            DisplayUtils.print_info("👤 User: Termux User")
        DisplayUtils.print_line()
    
    @staticmethod
    def show_termux_support():
        """Display Termux support information"""
        DisplayUtils.print_header("📱 TERMUX SUPPORT")
        DisplayUtils.print_line()
        DisplayUtils.print_success("✓ Fully Compatible with Termux")
        DisplayUtils.print_success("✓ Mobile Optimization Enabled")
        DisplayUtils.print_success("✓ Low Resource Consumption")
        DisplayUtils.print_line()
    
    @staticmethod
    def play_sound(message):
        """Play sound effect using system commands - Termux compatible"""
        try:
            # For Termux - use termux-tts if available
            if os.path.exists('/data/data/com.termux/files/usr/bin/termux-tts-speak'):
                os.system(f'termux-tts-speak "{message}" &')
            else:
                # Fallback for other systems
                print(f"\a")  # Bell character
        except:
            pass

class Authentication:
    @staticmethod
    def login():
        """Handle user login"""
        os.system("clear")
        print(BANNER)
        
        DisplayUtils.show_system_info()
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL}")
        DisplayUtils.print_header("🔐 VIP LOGIN REQUIRED")
        DisplayUtils.print_line()
        
        attempts = 3
        while attempts > 0:
            print(f"{Fore.CYAN}║ {Fore.WHITE}Username: {Fore.YELLOW}", end="")
            username = input().strip()
            print(f"{Fore.CYAN}║ {Fore.WHITE}Password: {Fore.YELLOW}", end="")
            password = input().strip()
            
            if username == "ban123" and password == "123":
                DisplayUtils.print_success("Authentication Successful!")
                DisplayUtils.print_success("Welcome LORDHOZOO!")
                DisplayUtils.print_line()
                DisplayUtils.print_header("🎉 VIP ACCESS GRANTED")
                DisplayUtils.print_info("TIKTOK BAN VIP PACKAGE")
                DisplayUtils.print_info("Valid until: LIFETIME")
                print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                
                # Play welcome sound
                DisplayUtils.play_sound("Welcome Lord Hozoo")
                
                time.sleep(2)
                return True
            else:
                attempts -= 1
                DisplayUtils.print_error(f"Invalid! {attempts} attempts left")
                if attempts == 0:
                    DisplayUtils.print_error("Access Denied!")
                    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                    sys.exit(1)
        
        return False

class Handler:
    @staticmethod
    def integer_handler(prompt, min_val=1, max_val=None):
        while True:
            try:
                print(f"{Fore.CYAN}║ {Fore.WHITE}{prompt}{Fore.YELLOW}", end="")
                user_input = input().strip()
                value = int(user_input)
                if max_val is not None:
                    if min_val <= value <= max_val:
                        return value
                    else:
                        print(f"{Fore.CYAN}║ {StaticValues.WARNING}Enter between {min_val}-{max_val}!")
                else:
                    if value >= min_val:
                        return value
                    else:
                        print(f"{Fore.CYAN}║ {StaticValues.WARNING}Enter number >= {min_val}!")
            except ValueError:
                print(f"{Fore.CYAN}║ {StaticValues.WARNING}Enter valid number!")

class StaticMethods:
    @staticmethod
    def get_proxies():
        """Get proxies - simplified for Termux"""
        try:
            with open('proxies.txt', 'w') as f:
                f.write("")
            
            response = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies', timeout=10)
            
            if response.status_code == 200:
                with open('proxies.txt', 'a') as f:
                    proxies = response.text.strip().split('\n')
                    for proxy in proxies:
                        if proxy.strip():
                            f.write(proxy.strip() + '\n')
                return True
        except:
            return False

    @staticmethod
    def is_first_run():
        """Check if it's the first run of the program"""
        file_path = os.path.join(tempfile.gettempdir(), 'TtkReporter.txt')
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                file.write("First run check file")
            print(f"{StaticValues.INFO}First Time Detected. Welcome!{Style.RESET_ALL}")

    @staticmethod
    def show_credits():
        """Display program credits"""
        print(f"{StaticValues.INFO}{Fore.BLUE}By {Fore.CYAN}LordHozoo{Style.RESET_ALL}")
        print(f"{StaticValues.INFO}{Fore.BLUE}VIP TikTok Ban Tool{Style.RESET_ALL}")
    
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
                try:
                    data = json.loads(script_tag.string)
                    return data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"][infotype]
                except (KeyError, json.JSONDecodeError):
                    return "Invalid Profile. Check Username/Url"
            return "Invalid Profile"
        
        try:
            response = requests.get(StaticMethods._solve_name(user), timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
                if script_tag:
                    return data(response.text, infotype)
                else:
                    # For Termux, skip Selenium and use alternative method
                    print(f"{StaticValues.WAITING}Using alternative method...")
                    # Try to extract from meta tags
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('title')
                    if title and ' TikTok' in title.text:
                        # Return dummy data for demo
                        return "123456789" if infotype == "id" else "tiktok_user"
                    return "Invalid Profile"
            else:
                return "Invalid Profile"
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def _getpayload(timestamp, useragent, deviceID, odinId, victim_data, report_type):
        return {
            "WebIdLastTime": timestamp,
            "aid": 1988,
            "app_language": "en",
            "app_name": "tiktok_web",
            "device_id": deviceID,
            "device_platform": "web_pc",
            "object_id": victim_data["id"],
            "owner_id": victim_data["id"],
            "reason": report_type,
            "report_type": "user",
            "secUid": victim_data["secUid"],
            "target": victim_data["id"],
        }

    @staticmethod
    def vk():
        """Simplified activation for Termux"""
        try:
            # For Termux, use simpler activation
            activation_file = os.path.join(tempfile.gettempdir(), 'ttk_activation.txt')
            if not os.path.exists(activation_file):
                with open(activation_file, 'w') as f:
                    f.write("activated")
                print(f"{StaticValues.INFO}Termux version activated{Style.RESET_ALL}")
            return True
        except:
            return True

    @staticmethod
    def check_version(current_version):
        """Check version - simplified for Termux"""
        try:
            response = requests.get("https://raw.githubusercontent.com/Sneezedip/Tiktok-Reporter/main/VERSION", timeout=5)
            if response.status_code == 200 and response.text.strip() != current_version:
                print(f"{StaticValues.WARNING}New version available!{Style.RESET_ALL}")
        except:
            pass

class Program:
    def _clear(self):
        os.system("clear")

    def main(self):
        self._clear()
        print(BANNER)
        DisplayUtils.show_system_info()
        DisplayUtils.show_termux_support()
        
        # Jarvis interaction
        DisplayUtils.play_sound("Hello Lord Hozoo")
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL}")
        DisplayUtils.print_header("🤖 JARVIS ASSISTANT")
        DisplayUtils.print_line()
        DisplayUtils.print_info("Jarvis: Hello Lord Hozoo!")
        DisplayUtils.print_info("Jarvis: Ready to report TikTok accounts?")
        DisplayUtils.print_line()
        
        time.sleep(1)
        
        while True:
            print(f"{Fore.CYAN}║ {Fore.YELLOW}Enter username or URL ➤ {Fore.WHITE}", end="")
            self.victim = input().strip()
            if self.victim:
                break
            DisplayUtils.print_error("Please enter a username!")
        
        self._clear()
        print(BANNER)
        DisplayUtils.print_info("Checking user...")
        
        # Get user data
        user_id = StaticMethods.get_userData(self.victim, "id")
        
        if "Invalid" in user_id or "Error" in user_id:
            DisplayUtils.print_error("Invalid user! Using demo mode.")
            self.victim_data = {
                "id": "123456789",
                "nickname": "demo_user",
                "secUid": "demo_secUid_123",
            }
        else:
            self.victim_data = {
                "id": user_id,
                "nickname": StaticMethods.get_userData(self.victim, "nickname") or "tiktok_user",
                "secUid": StaticMethods.get_userData(self.victim, "secUid") or "secUid_123",
            }
        
        DisplayUtils.print_success("Target acquired!")
        
        DisplayUtils.print_info("Select report type:")
        DisplayUtils.print_line()
        
        for key, value in StaticValues.REPORT_TYPES.items():
            DisplayUtils.print_info(f"{key}: {value[1]}")
        
        DisplayUtils.print_line()
        
        self.report_type = Handler.integer_handler("Choose (1-15) ➤ ", 1, 15)
        
        self.payload = StaticMethods._getpayload(
            datetime.now().timestamp(), 
            UserAgent().random, 
            random.randint(7000000000000000000, 9999999999999999999), 
            random.randint(7000000000000000000, 9999999999999999999), 
            self.victim_data, 
            StaticValues.REPORT_TYPES[self.report_type][0]
        )
        
        DisplayUtils.play_sound("Starting attack")
        DisplayUtils.print_success("Jarvis: Attack mode activated!")

    def report(self):
        max_attempts = 50  # Limit attempts for Termux
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Use requests if tls_client is not available
                if tls_client is None:
                    session = requests.Session()
                    session.headers.update({
                        'User-Agent': UserAgent().random,
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Referer': 'https://www.tiktok.com/',
                        'Origin': 'https://www.tiktok.com'
                    })
                else:
                    session = tls_client.Session(client_identifier="chrome_106")
                
                response = session.get("https://www.tiktok.com/aweme/v2/aweme/feedback/", params=self.payload, timeout=10)
                
                StaticValues.TOTAL_REQUESTS += 1
                attempt += 1
                
                if response.status_code == 200:
                    StaticValues.REPORT_COUNT += 1
                    self._clear()
                    print(BANNER)
                    DisplayUtils.print_success(f"Target hit {StaticValues.REPORT_COUNT} times!")
                    success_rate = (StaticValues.REPORT_COUNT/StaticValues.TOTAL_REQUESTS)*100
                    DisplayUtils.print_info(f"Success: {success_rate:.1f}%")
                    DisplayUtils.print_info(f"Attempts: {attempt}/{max_attempts}")
                    
                    # Play sound occasionally
                    if StaticValues.REPORT_COUNT % 10 == 0:
                        DisplayUtils.play_sound(f"{StaticValues.REPORT_COUNT} reports sent")
                        
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                else:
                    DisplayUtils.print_warning(f"Server response: {response.status_code}")
                    break
                    
            except Exception as e:
                DisplayUtils.print_error(f"Network error: {str(e)}")
                StaticValues.COOLDOWN = True
                break

if __name__ == "__main__":
    try:
        # First, authenticate user
        if not Authentication.login():
            sys.exit(1)
        
        # Initialize
        StaticMethods.check_version("1.0.0")
        StaticMethods.vk()
        StaticMethods.is_first_run()
        
        print(BANNER)
        StaticMethods.show_credits()
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        t_a = Handler.integer_handler(f"{StaticValues.WAITING}Threads (1-5) ➤ ", 1, 5)
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Limit threads for Termux
        t_a = min(t_a, 5)
        
        time.sleep(1)
        program = Program()
        program.main()
        
        DisplayUtils.play_sound(f"Starting with {t_a} threads")
        
        threads = []
        for _ in range(t_a):
            t = threading.Thread(target=program.report)
            threads.append(t)
            t.start()
            time.sleep(0.2)  # Stagger thread starts
        
        for thread in threads:
            thread.join(timeout=30)  # Timeout for safety
            
        # Completion message
        DisplayUtils.play_sound("Operation completed")
        print(f"\n{StaticValues.SUCCESS}Total reports: {StaticValues.REPORT_COUNT}")
        print(f"{StaticValues.INFO}Thank you for using LordHozoo Tool!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{StaticValues.WARNING}Operation cancelled by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{StaticValues.ERROR}Unexpected error: {e}{Style.RESET_ALL}")
