#!/usr/bin/python3
import os
import sys
from threading import Lock, Thread
from requests import get
from requests.exceptions import ConnectionError as fail
from requests.exceptions import MissingSchema as noschema
from queue import Queue
from time import sleep
import pyfiglet

def display_banner():
    ascii_banner = pyfiglet.figlet_format("Admin Finder")
    print(ascii_banner)
    print("\033[1;31mFuck Isreal By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\n")

def display_menu():
    print("[01] Share Admin Dashboard")
    print("[99] Exit to main.py")

def handle_menu_choice():
    choice = input("Enter your choice: ").strip()
    if choice == '01':
        site = input("Enter website URL (e.g., http://example.com): ").strip()
        if not site:
            print("Website URL is required!")
            handle_menu_choice()
            return
        proxy = input("Enter proxy (protocol-ip:port, e.g., http-1.2.3.4:8080) [Leave blank if none]: ").strip()
        delay = input("Enter delay in seconds (default 0): ").strip() or '0'
        wordlist = input("Enter custom wordlist path [default list.txt]: ").strip() or 'list.txt'

        proxy_enable = False
        proxyprotocol = proxyserver = None
        if proxy:
            try:
                proxyprotocol, proxyserver = proxy.split('-', 1)
                proxy_enable = True
            except ValueError:
                print("Invalid proxy format. Use protocol-ip:port (e.g., http-1.2.3.4:8080)")
                handle_menu_choice()
                return

        try:
            delay = int(delay)
        except ValueError:
            print("Delay must be an integer.")
            handle_menu_choice()
            return

        if not os.path.isfile(wordlist):
            print(f"Wordlist file {wordlist} not found!")
            handle_menu_choice()
            return

        scan_websites([site], proxy_enable, proxyprotocol, proxyserver, delay, wordlist)
    elif choice == '99':
        print("Exiting...")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
        handle_menu_choice()

def scan_websites(websites, proxy_enable, proxyprotocol=None, proxyserver=None, delay=0, wordlist='list.txt'):
    q = Queue()
    print_lock = Lock()

    def thread_func(website):
        worker = q.get()
        try:
            url = f"{website}{worker}"
            proxies = {proxyprotocol: proxyserver} if proxy_enable else None
            r = get(url, proxies=proxies, allow_redirects=True)
            if r.ok:
                with print_lock:
                    print(f"    [Status-code - {r.status_code}] Success: {worker}")
        except fail:
            with print_lock:
                print(f"Connection Error for {worker}")
        except noschema:
            with print_lock:
                print("ERROR: Missing URL scheme. Example: http://example.com")
            sys.exit()
        finally:
            q.task_done()

    for website in websites:
        if not website.endswith('/'):
            website += '/'
        try:
            with open(wordlist, 'r') as f:
                paths = [line.strip() for line in f]
        except FileNotFoundError:
            print(f"Wordlist file {wordlist} not found!")
            continue
        for path in paths:
            q.put(path)
        print(f"Result for {website}:")
        while not q.empty():
            t = Thread(target=thread_func, args=(website,))
            t.daemon = True
            t.start()
            sleep(delay)
        q.join()
        print('\n')

def run():
    """واجهة التشغيل الرئيسية للأداة"""
    display_banner()
    if len(sys.argv) == 1:
        display_menu()
        handle_menu_choice()
    else:
        proxy_enable = False
        proxyprotocol = proxyserver = None
        delay = 0
        wordlist = 'list.txt'
        websites_to_scan = []

        args = sys.argv[1:]
        i = 0
        while i < len(args):
            arg = args[i]
            if arg == '-site':
                i += 1
                while i < len(args) and not args[i].startswith('-'):
                    websites_to_scan.append(args[i])
                    i += 1
                if not websites_to_scan:
                    print("Error: -site requires a website URL")
                    sys.exit(1)
            elif arg == '--proxy':
                i += 1
                if i >= len(args):
                    print("Error: --proxy requires a protocol-proxy (e.g., http-1.2.3.4:8080)")
                    sys.exit(1)
                proxy = args[i]
                proxy_enable = True
                try:
                    proxyprotocol, proxyserver = proxy.split('-', 1)
                except ValueError:
                    print("Invalid proxy format. Use protocol-proxy (e.g., http-1.2.3.4:8080)")
                    sys.exit(1)
                i += 1
            elif arg == '--t':
                i += 1
                if i >= len(args):
                    print("Error: --t requires a delay in seconds")
                    sys.exit(1)
                try:
                    delay = int(args[i])
                except ValueError:
                    print("Delay must be an integer.")
                    sys.exit(1)
                i += 1
            elif arg == '--w':
                i += 1
                if i >= len(args):
                    print("Error: --w requires a wordlist path")
                    sys.exit(1)
                wordlist = args[i]
                i += 1
            else:
                print(f"Unknown argument: {arg}")
                sys.exit(1)

        if not websites_to_scan:
            print("Error: No website provided. Use -site to specify the target.")
            sys.exit(1)

        scan_websites(websites_to_scan, proxy_enable, proxyprotocol, proxyserver, delay, wordlist)

if __name__ == "__main__":
    run()
