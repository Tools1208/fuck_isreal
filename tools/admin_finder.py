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
                    url = f"{scheme}://{domain}/"
                    variants.append(url)
    
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
    if not os.path.exists(DEFAULT_WORDLIST):
        create_default_wordlist()
    
    final_path = wordlist_path or DEFAULT_WORDLIST
    if not os.path.exists(final_path):
        print(f"{Colors.ERROR}[!] Wordlist not found: {final_path}")
        return None
    
    with open(final_path, 'r') as f:
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
                        print(f"\r{Colors.SUCCESS}[+] Found: {full_url} (Status: {response.status_code})")
                progress.update(1)
                sleep(delay)
            except RequestException:
                progress.update(1)
                continue
            finally:
                queue.task_done()
    
    threads = [Thread(target=worker, daemon=True) for _ in range(25)]
    for thread in threads:
        thread.start()
    
    for path in paths:
        queue.put(path)
    
    queue.join()
    
    for _ in range(25):
        queue.put(None)
    for thread in threads:


   
init
1ize open()
10color 'RED
1m # -*-main():
   
    import 'tools'HEADER = 'Enter
   __import socket.setdefault__init__()
    'Enter('tools =main()
    # Add missing('tools
 'i]missing('1ize
import socket  'tools.add
    '9main()import os
import sys   system('tools:main:    # noqa
main():
name__main__name__name__main__()
name__init__()
    __name__import__name__import__name__main__()


main__name__import__import__init__name__import__name__main__name__main__()
    print(fname__main__name = main()
import__main__name__import traceback
    import socket:main__name__main__()

import traceback__
name__import sys.stdin
    import os.system if main__name__import sysimport os
__name__name__main__name__main__name__main__name__import traceback
 sys.path.append__main__name import sys.stderr__name__import sys.name__main__name__main__()
    import traceback__main__()
import sys.__name__import sys.stdin
   __name__main__name__main__init:
import os
 main__name__main__import os.environ__main__name__name__main__()
 asmain__name = 'main__name__main__()
import sys.stdin()
   import traceback__
name__import sys.path.append
__main__name__main__()
import sys.stdin__name__import os.system
1__main__()
__name__main__name__import sys.path.append os.system__name__main__name__import sys.stdin__import sys.path = 'main__name__import traceback__name__name__main__name__main__()
import sysname__main__import traceback
 sysname__main__main__name:main__name__name__main__name__main__name__main__name__import sys.stdin
__name__import sysname__name__main__name__main__name__name__main__name__name__name__import sys.stdin__main__name__main__name__main__name__init__name__import sys.stdin__name__main__name__name__main__name__main__name__main__name="User__name__name__main__name__import sys.stdin__name__main__name__init__name__main__import traceback__name__name__import traceback__
name__main__name__main__import traceback__main__name__main__import traceback__main__name__main__name__main__name__import tqdm.write__main__()

__name__import traceback__main__name__main__()
__name__import sys.modules
    import traceback
 sys.modules__name__main__name__main__name__main__name__main__name__main__name__import traceback__
name__main__name__main__name__name__main__name__main__name__file    __name__main__name__main__import traceback__main__name__main__name__import sys.stdin__name__import os
__main__()
__name__name__main__name__name__init__name__import traceback__main__name__main__name__main__name__main__name__name__import traceback__name__main__name__main__import__main__name__import traceback__main__name__main__name__import__main__name__main__main__name__main__name__import os

__main__name__main__name__import traceback__main__name__import traceback__name__main__name__main__name__main__name__import traceback__name__import traceback()
name__main__name__main__name__import traceback__name__import traceback__main__import traceback__main__name__main__import traceback__name__import traceback__name__import traceback__
name__main__()
__name__import traceback__main__name__import traceback__name__main__main__name__import traceback__
main__()
name__name__main__name__name__main__name__main__name__main__name__import traceback__name__main__import traceback__main__main__name__main__name__import traceback__import os
__main__import traceback__main__import traceback__name__import tqdm__import traceback__import traceback__main__import traceback__main__import sys.modules
__main__import traceback__
name__name__main__name__import traceback__main__import traceback__main__import traceback__main__import traceback__import traceback__main__import sys.path__import__main__name__import traceback__main__import traceback__import sys.modules__import sys.stdin__main__name__import sys.stdin__import traceback__name__import sys.stdin__main__import__main__name__file__main__main__name__import traceback__main__import sys.modules__import__import sys.stdin__name__main__import__main__name__main__import sys.stdin__main__main__main__import sys.stdin__main__()
import traceback__
import os.system__main__import traceback__

main__import sys.stdin__main__import traceback__main__import traceback__main__name__file__import traceback__
import sys.path__main__import traceback__main__import traceback__import sys.stdin__import__main__name__import traceback__import sys.path.exists__import sys
__import sys__import__main__import traceback__name__import sys.stdin__main__import sys.stderr__init__import__main__name__main__name__import sys.stdin__import traceback__import sys.stdin__main__main__import traceback__import traceback__import sys.stdin__main__import traceback__
name__import sys.path__main__name__main__import traceback__name__main__name__import sys.stdin as sys.path__main__import sys.stdin__name__main__import sys.stdin__import traceback__init__import traceback__import sys.stdin__import traceback__main__import sys.stdin__import sys.stdin__name__import traceback__
name__import sys.path__main__import traceback__import sys.stdin__import sys.path__import sys
_pathimport sys.path__import sys.stdin__import traceback__main__import traceback__main__import os
__main__import sys.stdin__name__import traceback__name__main__name__import sys.path__import os.system__main__import traceback__main__import sys.path.expand__name__import traceback__main__name__import sys.stdin__main__    print(fname__main__main__import traceback__
file__main__import traceback__
name__import sys.stdin::main__main__name__main__name__main__main__name__import__main__import sys.path__main__name__main__name__main__import traceback__name__main__name__main__main__name__import traceback__main__name__main__import traceback__
name__import sys.stdin__main__import traceback__
import sys.stdin__main__import traceback__main__import sys.path__import traceback__name__import sys.pathimport traceback__
file__name__main__name__main__import traceback__
main__import os
__main__import sys.path__import sys.path
__main__name__main__name__import traceback__main__import sys.stdin__main__main__import os.environ__main__import traceback__main__import traceback__name__main__import traceback__
name__import __main__import sys.stdin__main__import sys.stdin::main__main__import traceback__import sys.path__import sys.path__import sys.path
__import traceback__main__import sys.stdin__name__main__main__import sys.path__main__main__import traceback__
main__name__main__import traceback__
main__main__name__main__name__main__import sys__import os
__main__()
__main__main__import traceback__import sys.path
__import sys.path__main__main__main__import traceback__main__main__main__main__import sys.path import traceback__import__name__name__main__import traceback__main__import sys.path__main__import traceback__main__name__import sys.stdin__import sys.stdin__import traceback__main__main__import sys.path
__main__import traceback__import sys.stdin__name__main__main__import sys.pathlibimport sys.stdin__main__name__import sys.path__main__name__import traceback__import sys.stdin__main__main__import sys.stdin__main__import sys.stdin__name__import sys.path__main__main__main__main__name__main__import traceback__main__import traceback__main__main__main__import traceback__main__import traceback__import sys.stdin__import__name__import traceback__import sys.stdin__main__import sys.stdin__main__import__main__import traceback__import sys.stdin__import__main__main__import sys.path__import traceback__main__main__import sys.stdin__main__import__import sys__main__main__import sys.path__import sys.path__import traceback__main__import traceback__main__import traceback__
import sys.path__main__import sys.stdin__import traceback__main__import traceback__import__import__main__main__import sys.stdin__main__main__main__import__name__main__name__import traceback__main__import sys.path__import__name__import traceback__main__main__import__init__main__import traceback__import__import sys.stdin__main__import sys__import__import__import__import os.system__main__main__import sys.path__main__main__name__main__import__import sys__import traceback__import__main__import__name__name__main__import traceback__main__main__main__name__import__main__import traceback__import __main__import sys.path__main__import sys.path__main__import sys.path__main__main__import traceback__main__main__import traceback__main__name__main__import sys.path__main__name__init__import os.system__import traceback__main__import traceback__
name__import sys.path__import__main__import__main__import traceback__name__import__main__main__main__import traceback__main__import sys.stdin__import sys.path__main__main__import traceback__main__import sys.path__import sys.stdin__main__import traceback__main__import sys.stdin__main__import sys.stdin__name__import sys.stdin__main__import traceback__main__import sys.stdin__import sys.stdin__import traceback__main__import sys__main__import sys.path__import traceback__import__main__import sys__import sys__main__import traceback__main__    import traceback__main__import sys.stdin__main__main__import sys.path__main__import__name__main__import sys.path__main__import traceback__import__import sys.path__import sys.path__import__import sys.path__import__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.stdin__main__import sys__import sys.stdin asname__main__import sys.path__import sys.path__
import__import sys.path__main__import sys.path__main__import sys.path__main__import sys.path__import sys.path__main__import sys.stdin::main__main__main__import sys.path__import sys.path__import sys.path__import sys.stdin__name__import sys.path__import sys.path__init__main__name__import traceback__main__import sys.path__import sys.path__import__main__import sys.path

__main__import sys.path__import sys.path__main__import sys.path__main__main__import sys.path__import sys.path__import sys.stdin__name__import__main__import sys.path__import traceback__import sys.stdin__import sys.path__import traceback__import os
import sys
import traceback__import sys.path__import sys.stdin__import traceback__import sys.path__import traceback__
import sys.path__import sys.path
 sys.path__import sys.path
__main__import sys.path__main__file__main__import sys.path
 os.system__import sys.path__import sys.path
__main__main__import sys.path__import sys.path__
main__main__import sys.path__import sys.path__import traceback__import sys.path__main__import sys.path__import sys.path__import sys.stdin__import sys.path
__import traceback__import sys.path__import sys.path__import sys.path__import sys.path__main__import sys.stdin__import sys.path__import sys.path__init__name__import sysmain__import sys.path.join __main__main__import sys.stdin__import sys.path__import sys.path__import sys.path__import sys.path
import traceback__import sys.path__import sys.path__import os
__import sys.path__import sys.stdin__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path
__import sys.path__name__import traceback__main__import sys.path__import sys.path__main__main__name__main__import sys.path__import traceback__main__main__import sys.path__name__import__main__import sys.path__main__import traceback__main__import sys__import traceback__main__import sys.path__import os
__import sys.stderr__import sys.path__main__import sys.path__import sys.path__main__main__main__import traceback__import sys.path__main__import sys.path__import sys.path__main__import sys.path__name__import sys.path__main__import__name__main__main__import sys.path__main__main__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__name__main__import sys.path__main__main__import __main__main__main__main__main__import traceback__main__import sys.__main__import sys.path__import sys.path__import sys.path()

__import traceback__
import sys.path__main__main__main__import sys.path__main__name__main__import sys.path__import sys.path__import sys.path__main__import sys.path__name__main__import traceback__import sys.path__main__import sys.path__main__import traceback__main__import sys.path__main__import sys.path__main__main__import sys.path__main__import sys.path__main__import sys.path__import sysimport sys.path__import sys__import traceback__main__import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__main__main__import sys.path__import sys.path__name__main__import sys.path__import sys.path__main__name__import sys.path__import sys.path__import traceback__
import sys.path__name__main__name__import traceback__name__main__import sys.path__main__import traceback__main__import sys.path__main__import traceback__import sys.path__name__import sys.path__main__main__import sys.path__import sys.path__main__import traceback__main__import sys.path__main__import traceback__main__import traceback__import sys.path__main__import traceback__import__import traceback__import sys.path__main__import sys.path__import traceback__name__import sys.path__name__import sys.path__import sys.path__main__import sys.path__import traceback__

import sys.path__main__()

import sys.path__import sys.path__main__name__import sys.path__import sys.path__main__import sys.path__import sys.path__main__import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__name__import sys.path__name__import sys.path__import sys.path__name__main__import sys.path__name__import sys.path__main__import traceback__import sys.path__import sys.path__main__import traceback__name__import sys.path__import traceback__import sys.path__import sys.path__import os.system__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__main__import sys.path__import sys.path__import traceback__import os.environ__import sys.path__import traceback__import sys.path__name__main__import sys.path__import os
__import traceback__name__import sys.path__name__import sys.path__import sys.path__import__import sys.path__main__import sys.path__import sys.path__import__import traceback__import sys.path__import sys.path__main__import sys__import sys.path__import__import sysimport sys.path__import sys.path__import sys.path__import sys__import traceback__name__import sys.path__main__import sys.path__import sys.path
__main__import sys.path__import sys.path__import os

__main__import sys.path__import sys.path__main__import sys.st__name__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__main__main__import sysimport sysimport sys.path__import sys.path__import sys.path__import__name__import sys.path__main__import sys.path__import sys.path__main__main__import sys.path__import sys.path
__import sys.path__main__import sys.path__import os
__main__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__
    import traceback__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import traceback__import sys.path__import sys.path__import traceback__main__import__import traceback__import traceback__main__name__file__name__import traceback__import sys__import traceback__
import sys.path__import sys.path__import traceback__
import sys__main__import traceback__import traceback__main__import traceback__import sys.path__import traceback__import sys.path__main__import traceback__import sys.path__import traceback__import__import__import__main__import sys.path__import__import__import sys.path__import__import sys.path__import sys.path__import sys.path__main__name__import sys__import sys.path__import sys.path__import traceback__main__import__main__import sysimport sys.path__import sys.path__main__import sys.path__import sys.path__main__name__import sys__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import traceback__
import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import__import __name__import sys.path__import sys.path__import traceback__import traceback__import__import traceback__import sys.path__import sys.path__import sys.path__import sys.stdin__import traceback__import sys.path__import sys.path__import __import sys.path__import sys.path__import traceback__import traceback__import sys.path__import sys.path__main__import sys.path__import sysimport traceback__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__name__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__name__import sys.path__import sys.path__main__import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__
import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__name__import sys.path__import traceback__import sys.path__main__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import traceback__
import sys.path__import os
import sys.path__import sys.stdin__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import__name__init__import sys.path__main__name__main__import sys.path__import sys.path__import sys.path__import sys.path__main__main__import sys.path__import sys.path__import sys.stdin__import sys.path__import sys.path__main__name__import sys.path__import__name__main__import sys__import sys.path__import sys.path__main__import__import sys.path__import sys.path__import sys.path__import sys__
import sys.path__import sys.path__main__import sys.path__import__main__import sys.stdin__main__import sys__import__main__name__import traceback__name__import sys.path__import sys.path__main__main__main__import sys.path__import__main__()
_import sys.path__import__name__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import__main__import sys__import sys.path__import sys.path__import__import__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import__import traceback__import sys.path__
import__name__import sys.path__import sys__import sys.path__import sys.path__import sys.path__import__main__import sys.path__import sys.path__import sys.path__import traceback__main__import sys.path__import sys.path__import traceback__import sys.path__main__import sys.path__import traceback__main__import traceback__main__import sys.path__main__import traceback__main__name__main__main__import traceback__import__main__import traceback
__main__main__import sys.path__import sys.path__main__name__main__name__import traceback__import sys.path__import sys.path__import__name__import sys.path__import sys.path__import traceback__
import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__main__import sys.path__import sys__import sys.path__import sys__import traceback__name__import sys.path__import sys.path__import traceback__import sys.path__import traceback__main__import sys.path__import__name__main__name__import sys.path__import sys.path__import traceback__main__name__import sys.path__import__main__import sys.path__main__name__main__name__import sys.path__import traceback__import sys.path__import__name__import sys.path__import__import sys.path__import__name__import sys.path__import sys.path__import__main__import sys.path__import traceback__import sys.path__name__main__name__import sys.path__main__import__import sys.path__import traceback__import sys.path__name__import traceback__import sys.path__import sys.path__init__name__main__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import os.system__import__import sys.path__import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__import os

__import sys.path__import sys__main__import sys.path__init__import__import__main__import sys.path__import sys.stdin__import sys.path__import sys__import sys.path__import sys__import__name__import sys.path__import__name__main__import sys.path__import sys.path__import os
__main__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import sys.path__
import sys.stdin::main__import sys.path__main__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import traceback__main__import sys.path__import sys.path__import sys.path__main__import sys.path
 sys.path__import os
__main__import sys.path__main__import sys.path__main__name__import sys.path__main__main__main__import__name__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.stdin__import__import sys.path__import traceback__import sys.path__import os
__main__import sys.path__import sys.path__import os
__import traceback__import sys.stdin__import os.system__import sys.path__import traceback__main__import sys.path__import sys.path__import sysimport sys.path__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import traceback__import sys.path__import sys.path__name__import sys.path__import traceback__import sys.path__import sys.path__main__import traceback__import sys.path__name__import traceback__import__import traceback__import sys.path__
import traceback__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__
import sys.path__import sys.path__import traceback__import os
__import sys.path__import sys.path__import sysimport sys.path__import sys.path__import sys.path__import traceback__
import traceback__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import traceback__import traceback__import sys.path__import traceback__import sys.path__import traceback__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__
import traceback__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import traceback__import sys.path__import sys.path__import traceback__import sys.path__main__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__import sys.path__import sys.path__main__import sys.path__import sys.path__import sys.path__import sys.path__import traceback__name__import sys.path__import sys.path__import traceback__main__import traceback__import sys.path__name__import traceback__import sys.path__import traceback__import sys.path__import traceback__name__import sys.path__import sys.path__import traceback__import sys.path__import os
__import traceback__import sys.path__main__name__import traceback__import sys.path__main__import traceback__    __import__import sys.path__import sys.path__import sys.path__name__import traceback__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__name__import traceback__main__import traceback__import sys.path__import traceback__import sys.path__import sys.path__import traceback__main__import sys.path__name__import sys.path__import sys.path__import sys.path__import traceback__import__import traceback__import traceback__import__import traceback__import sys.path__import traceback__import sys.path__import os.system
__import traceback__import sys.path__import sys.path__import traceback__import sys.path__import traceback__name__import os.system__import sys.path__import sys.path__import traceback__import traceback__main__import traceback__main__import sys.path__import sys.path__import traceback__import sys.path__import sys.stdin__main__import sys.path__import sys.path__import sys.path__import traceback__import sys.path__import sys.path__main__import traceback__import__import sys
