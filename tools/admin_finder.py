#!/usr/bin/env python3
import os
import sys
import socket
import urllib.parse
import time
from threading import Lock, Thread
import requests
from requests.exceptions import RequestException
from queue import Queue
from tqdm import tqdm
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "6.3 Advanced"
DEFAULT_WORDLIST = "admin_paths.txt"
DEFAULT_PATHS = [
    "admin", "administrator", "login", "wp-admin", "admin.php",
    "dashboard", "controlpanel", "cp", "manager", "phpmyadmin",
    "admin_area", "admin-console", "admin_login", "admin_panel"
]

# Extended lists for global scanning
COMMON_SUBDOMAINS = ["", "www", "admin", "test", "dev", "app", "web", "portal"]
GLOBAL_TLDS = [
    ".com", ".net", ".org", ".info", ".biz", ".co", ".io",
    ".xyz", ".online", ".site", ".tech", ".shop", ".cloud"
]

class Colors:
    HEADER = Fore.MAGENTA
    INFO = Fore.CYAN
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

def create_default_wordlist():
    """Create default wordlist if not exists"""
    if not os.path.exists(DEFAULT_WORDLIST):
        with open(DEFAULT_WORDLIST, 'w') as f:
            for path in DEFAULT_PATHS:
                f.write(f"{path}\n")
        print(f"{Colors.SUCCESS}[+] Created default wordlist: {DEFAULT_WORDLIST}")

def display_banner():
    """Display professional colorized banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.HEADER + pyfiglet.figlet_format("AdminFinder", font="slant"))
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
    """Check domain resolvability using socket"""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def generate_global_variants(base_url):
    """Generate global domain and subdomain variants"""
    parsed = urllib.parse.urlparse(base_url)
    base_domain = parsed.netloc.split(':', 1)[0].replace('www.', '')
    
    variants = []
    for tld in GLOBAL_TLDS:
        for sub in COMMON_SUBDOMAINS:
            domain = f"{sub + '.' if sub else ''}{base_domain}{tld}"
            if is_domain_resolvable(domain):
                for scheme in ["http", "https"]:
                    variants.append(f"{scheme}://{domain}/")
                    
    return list(set(variants))

def validate_url(url):
    """Validate and normalize URL format"""
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        url = f"http://{url}"
    return f"{url.rstrip('/')}/"

def load_wordlist(wordlist_path):
    """Smart wordlist loading with automatic creation"""
    if not os.path.exists(wordlist_path):
        create_default_wordlist()
        
    if not os.path.exists(wordlist_path):
        print(f"{Colors.ERROR}[!] Wordlist not found: {wordlist_path}")
        return None
        
    with open(wordlist_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scan_worker(url, proxy, delay, paths, results, progress):
    """Advanced multithreaded scanning worker"""
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
                        tqdm.write(f"{Colors.SUCCESS}[+] Found: {full_url} (Status: {response.status_code})")
                        
                progress.update(1)
                time.sleep(delay)
                
            except RequestException:
                progress.update(1)
                continue
            finally:
                queue.task_done()

    # Start worker threads
    threads = [Thread(target=worker, daemon=True) for _ in range(25)]
    for thread in threads:
        thread.start()
        
    # Add paths to queue
    for path in paths:
        queue.put(path)
        
    # Wait for all tasks to complete
    queue.join()
    
    # Stop workers
    for _ in range(25):
        queue.put(None)
    for thread in threads:
        thread.join()

def run():
    """Main function to run the scanner"""
    display_banner()
    
    # Get user input
    target_url = input(f"{Colors.INFO}[?] Enter target URL (e.g., example.com): ").strip()
    wordlist_path = input(f"{Colors.INFO}[?] Enter wordlist path (press Enter for default): ").strip() or DEFAULT_WORDLIST
    use_proxy = input(f"{Colors.INFO}[?] Use proxy? (y/n): ").strip().lower() == 'y'
    
    # Validate and normalize URL
    target_url = validate_url(target_url)
    if not target_url:
        print(f"{Colors.ERROR}[!] Invalid URL format")
        sys.exit(1)
        
    # Load wordlist
    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        print(f"{Colors.ERROR}[!] Failed to load wordlist")
        sys.exit(1)
        
    # Proxy configuration
    proxies = None
    if use_proxy:
        proxy_url = input(f"{Colors.INFO}[?] Enter proxy URL (e.g., http://127.0.0.1:8080): ").strip()
        proxies = {"http": proxy_url, "https": proxy_url}
        
    # Generate URL variants
    print(f"{Colors.INFO}[+] Generating global domain variants...")
    urls_to_scan = generate_global_variants(target_url)
    
    # Prepare scanning
    results = []
    total_requests = len(wordlist) * len(urls_to_scan)
    progress = tqdm(total=total_requests, unit="req", dynamic_ncols=True)
    
    try:
        for url in urls_to_scan:
            scan_worker(url, proxies, 0.1, wordlist, results, progress)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Scan interrupted by user")
    finally:
        progress.close()
        
    if results:
        print(f"\n{Colors.SUCCESS}[+] Scan completed. Found {len(results)} admin pages:")
        for url, status in results:
            print(f"    {Colors.SUCCESS}{status}: {url}")
    else:
        print(f"\n{Colors.WARNING}[!] No admin pages found")

if __name__ == "__main__":
    run()
