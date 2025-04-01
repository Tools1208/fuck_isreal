#!/usr/bin/env python3
import os
import sys
import urllib.parse
from threading import Lock, Thread
from requests import get
from requests.exceptions import RequestException
from queue import Queue
from time import sleep
from tqdm import tqdm
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "4.2 Pro"
DEFAULT_WORDLIST = "admin_paths.txt"
DEFAULT_PATHS = [
    "admin", "admin.php", "admin/login.php", "administrator", 
    "login", "wp-admin", "dashboard", "controlpanel", 
    "cp", "admin_area", "admin-console", "manager"
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
    """Display colorized tool banner"""
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

def validate_url(url):
    """Validate and normalize URL format"""
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        url = f"http://{url}"
    return f"{url.rstrip('/')}/"

def generate_url_variants(base_url):
    """Generate URL variants for comprehensive scanning"""
    parsed = urllib.parse.urlparse(base_url)
    schemes = ["http", "https"] if parsed.scheme not in ["http", "https"] else [parsed.scheme]
    subdomains = ["", "www."]
    
    variants = []
    for scheme in schemes:
        for sub in subdomains:
            netloc = f"{sub}{parsed.netloc.split(':', 1)[0]}" if sub else parsed.netloc
            variants.append(
                urllib.parse.urlunparse((
                    scheme,
                    netloc,
                    parsed.path,
                    parsed.params,
                    parsed.query,
                    parsed.fragment
                )).rstrip("/") + "/"
            )
    return list(set(variants))

def load_wordlist(wordlist_path):
    """Smart wordlist loading with automatic creation"""
    # Create default if needed
    if not os.path.exists(DEFAULT_WORDLIST):
        create_default_wordlist()
    
    # Use specified or default
    final_path = wordlist_path or DEFAULT_WORDLIST
    if not os.path.exists(final_path):
        print(f"{Colors.ERROR}[!] Wordlist not found: {final_path}")
        return None
    
    with open(final_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scan_worker(url, proxy, delay, paths, results, progress):
    """Multithreaded scanning worker"""
    lock = Lock()
    queue = Queue()
    
    def worker():
        while True:
            path = queue.get()
            if path is None:
                break
            try:
                full_url = f"{url}{path}"
                response = get(
                    full_url,
                    proxies=proxy,
                    timeout=10,
                    allow_redirects=True,
                    verify=False  # SSL verification disabled for speed
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
    
    # Start threads
    threads = [Thread(target=worker, daemon=True) for _ in range(10)]
    for thread in threads:
        thread.start()
    
    # Add paths to queue
    for path in paths:
        queue.put(path)
    
    # Wait for completion
    queue.join()
    
    # Stop workers
    for _ in range(10):
        queue.put(None)
    for thread in threads:
        thread.join()

def run():
    """Main execution function"""
    create_default_wordlist()
    
    while True:
        display_banner()
        print(f"""
{Colors.INFO}[1]{Colors.RESET} Start Admin Scan
{Colors.WARNING}[99]{Colors.RESET} Exit Tool
        """.strip())
        
        choice = input(f"\n{Colors.BOLD}Select option: {Colors.RESET}").strip()
        if choice == '99':
            sys.exit(0)
        if choice != '1':
            continue
        
        # Get inputs
        target = input(f"\n{Colors.INFO}[+] Target URL (e.g., example.com): {Colors.RESET}").strip()
        proxy = input(f"{Colors.INFO}[+] Proxy (http-1.2.3.4:8080): {Colors.RESET}").strip()
        delay = input(f"{Colors.INFO}[+] Request delay (seconds) [0]: {Colors.RESET}").strip() or '0'
        wordlist = input(f"{Colors.INFO}[+] Wordlist path [Press Enter for default]: {Colors.RESET}").strip()
        
        # Validate inputs
        try:
            delay = int(delay)
            if delay < 0:
                raise ValueError
        except ValueError:
            print(f"{Colors.ERROR}[!] Delay must be a positive integer")
            sleep(2)
            continue
        
        # Load wordlist
        paths = load_wordlist(wordlist)
        if not paths:
            continue
        
        # Setup proxy
        proxy_dict = None
        if proxy:
            try:
                proto, addr = proxy.split('-', 1)
                proxy_dict = {proto: addr}
            except ValueError:
                print(f"{Colors.ERROR}[!] Invalid proxy format. Example: http-1.2.3.4:8080")
                sleep(2)
                continue
        
        # Validate URL
        validated_url = validate_url(target)
        if not validated_url:
            print(f"{Colors.ERROR}[!] Invalid target URL")
            sleep(2)
            continue
        
        # Generate URL variants
        url_variants = generate_url_variants(validated_url)
        print(f"\n{Colors.INFO}[i] Scanning {len(url_variants)} URL variants...")
        
        # Start scanning
        results = []
        total_requests = len(url_variants) * len(paths)
        progress = tqdm(
            total=total_requests,
            unit="req",
            desc=f"{Colors.INFO}Progress",
            dynamic_ncols=True,
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Colors.INFO, Colors.RESET)
        )
        
        for url in url_variants:
            scan_worker(url, proxy_dict, delay, paths, results, progress)
        
        progress.close()
        
        # Display results
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
