#!/usr/bin/env python3
import os
import sys
import socket
import urllib.parse
from threading import Lock, Thread
import requests
from requests.exceptions import RequestException
from queue import Queue
from tqdm import tqdm
import pyfiglet
from colorama import Fore, Style, init

# تهيئة الألوان
init(autoreset=True)

# الثوابت
VERSION = "5.0 Global"
DEFAULT_WORDLIST = "admin_paths.txt"
DEFAULT_PATHS = [
    "admin", "administrator", "login", "wp-admin", "admin.php",
    "dashboard", "controlpanel", "cp", "manager", "phpmyadmin",
    "admin_area", "admin-console", "admin_login", "admin_panel"
]
GLOBAL_TLDS = [".com", ".net", ".org", ".info", ".biz", ".co", ".io"]
COMMON_SUBDOMAINS = ["", "www", "admin", "test", "dev", "app"]

class Colors:
    HEADER = Fore.MAGENTA
    INFO = Fore.CYAN
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

def create_default_wordlist():
    """إنشاء قائمة مسارات افتراضية"""
    if not os.path.exists(DEFAULT_WORDLIST):
        with open(DEFAULT_WORDLIST, 'w') as f:
            for path in DEFAULT_PATHS:
                f.write(f"{path}\n")
        print(f"{Colors.SUCCESS}[+] Created default wordlist: {DEFAULT_WORDLIST}")

def display_banner():
    """عرض الواجهة الرئيسية المطورة"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.HEADER + pyfiglet.figlet_format("GlobalFinder", font="slant"))
    print(fr"""
{Colors.INFO}  _____           _       _    _____ _           _         
 |  ___|_ _  ___| |_ ___| |  |  ___(_)_ __   __| | ___ _ __ 
 | |_ / _` |/ __| __/ _ \ |  | |_  | | '_ \ / _` |/ _ \ '__|
 |  _| (_| | (__| ||  __/ |  |  _| | | | | | (_| |  __/ |   
 |_|  \__,_|\___|\__\___|_|  |_|   |_|_| |_|\__,_|\___|_|   
    """.strip())
    print(f"{Colors.WARNING}{'='*60}")
    print(f"{Colors.INFO}{'Telegram: https://t.me/AnonymousJordan'.center(60)}")
    print(f"{Colors.HEADER}Version: {VERSION}".center(60))
    print(f"{Colors.WARNING}{'='*60}")

def is_domain_resolvable(domain):
    """التحقق من إمكانية حل النطاق باستخدام socket"""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def generate_global_variants(base_url):
    """إنشاء متغيرات عالمية للنطاقات الفرعية والنطاقات العليا"""
    parsed = urllib.parse.urlparse(base_url)
    base_domain = parsed.netloc.split(':', 1)[0].replace('www.', '')
    
    variants = []
    for tld in GLOBAL_TLDS:
        for sub in COMMON_SUBDOMAINS:
            # تكوين النطاق مع الـ TLD والنطاق الفرعي
            domain = f"{sub}{'.' if sub else ''}{base_domain}{tld}"
            if is_domain_resolvable(domain):
                # إنشاء الروابط مع الـ TLD المختلف
                for scheme in ["http", "https"]:
                    url = f"{scheme}://{domain}/"
                    variants.append(url)
    
    return list(set(variants))

def validate_url(url):
    """التحقق من صحة الرابط وتنسيقه"""
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        url = f"http://{url}"
    return f"{url.rstrip('/')}/"

def load_wordlist(wordlist_path):
    """تحميل قائمة المسارات مع إنشاء افتراضي"""
    if not os.path.exists(DEFAULT_WORDLIST):
        create_default_wordlist()
    
    final_path = wordlist_path or DEFAULT_WORDLIST
    if not os.path.exists(final_path):
        print(f"{Colors.ERROR}[!] Wordlist not found: {final_path}")
        return None
    
    with open(final_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scan_worker(url, proxy, delay, paths, results, progress):
    """وظيفة المسح المتقدمة"""
    lock = Lock()
    queue = Queue()
    
    def worker():
        while True:
            path = queue.get()
            if path is None:
                break
            try:
                full_url = f"{url}{path}"
                response = requests.get(
                    full_url,
                    proxies=proxy,
                    timeout=10,
                    allow_redirects=True,
                    verify=False
                )
                if 200 <= response.status_code < 300:
                    with lock:
                        results.append((full_url, response.status_code))
                        print(f"\r{Colors.SUCCESS}[+] Found: {full_url} (Status: {response.status_code})")
                progress.update(1)
                sleep(delay)
            except RequestException:
                progress.update(1)
                continue
            finally:
                queue.task_done()
    
    threads = [Thread(target=worker, daemon=True) for _ in range(15)]
    for thread in threads:
        thread.start()
    
    for path in paths:
        queue.put(path)
    
    queue.join()
    
    for _ in range(15):
        queue.put(None)
    for thread in threads:
        thread.join()

def run():
    """الدالة الرئيسية المطورة"""
    create_default_wordlist()
    
    while True:
        display_banner()
        print(f"""
{Colors.INFO}[1]{Colors.RESET} Start Global Scan
{Colors.WARNING}[99]{Colors.RESET} Exit Tool
        """.strip())
        
        choice = input(f"\n{Colors.BOLD}Select option: {Colors.RESET}").strip()
        if choice == '99':
            sys.exit(0)
        if choice != '1':
            continue
        
        target = input(f"\n{Colors.INFO}[+] Target (e.g., example.com): {Colors.RESET}").strip()
        proxy = input(f"{Colors.INFO}[+] Proxy (http-1.2.3.4:8080): {Colors.RESET}").strip()
        delay = input(f"{Colors.INFO}[+] Request delay (seconds) [0]: {Colors.RESET}").strip() or '0'
        wordlist = input(f"{Colors.INFO}[+] Wordlist [Press Enter for default]: {Colors.RESET}").strip()
        
        try:
            delay = int(delay)
            if delay < 0:
                raise ValueError
        except ValueError:
            print(f"{Colors.ERROR}[!] Invalid delay value")
            sleep(2)
            continue
        
        paths = load_wordlist(wordlist)
        if not paths:
            continue
        
        proxy_dict = None
        if proxy:
            try:
                proto, addr = proxy.split('-', 1)
                proxy_dict = {proto: addr}
            except ValueError:
                print(f"{Colors.ERROR}[!] Invalid proxy format")
                sleep(2)
                continue
        
        validated_url = validate_url(target)
        if not validated_url:
            print(f"{Colors.ERROR}[!] Invalid target URL")
            sleep(2)
            continue
        
        global_variants = generate_global_variants(validated_url)
        print(f"\n{Colors.INFO}[i] Generated {len(global_variants)} global variants")
        
        results = []
        total_requests = len(global_variants) * len(paths)
        progress = tqdm(
            total=total_requests,
            unit="req",
            desc=f"{Colors.INFO}Progress",
            dynamic_ncols=True,
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Colors.INFO, Colors.RESET)
        )
        
        for url in global_variants:
            scan_worker(url, proxy_dict, delay, paths, results, progress)
        
        progress.close()
        
        print(f"\n{Colors.BOLD}{'='*60}")
        if results:
            print(f"{Colors.SUCCESS}[+] Found {len(results)} admin panels:")
            for url, status in results:
                print(f"  {Colors.WARNING}-{Colors.RESET} {url} (Status: {status})")
        else:
            print(f"{Colors.ERROR}[!] No admin panels found")
        
        input(f"\n{Colors.INFO}Press Enter to return to menu...")

if __name__ == "__main__":
    run()
