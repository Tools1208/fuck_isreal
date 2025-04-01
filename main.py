#!/usr/bin/env python3
import os
import sys
import subprocess
from time import sleep

def check_system_dependencies():
    packages = []
    if subprocess.run(['which', 'figlet'], stdout=subprocess.PIPE).returncode != 0:
        packages.append("figlet")
    if subprocess.run(['which', 'lolcat'], stdout=subprocess.PIPE).returncode != 0:
        packages.append("lolcat")
    
    if packages:
        print(f"\033[1;33m[!] Installing system dependencies: {' '.join(packages)}\033[0m")
        subprocess.run(['sudo', 'apt', 'update'], stdout=subprocess.PIPE)
        subprocess.run(['sudo', 'apt', 'install', '-y'] + packages, stdout=subprocess.PIPE)
        print("\033[1;32m[+] System dependencies installed successfully!\033[0m")
        sleep(2)

def check_python_dependencies():
    required = ['requests', 'cryptography', 'tqdm', 'pyfiglet', 'colorama', 'beautifulsoup4']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\033[1;33m[!] Installing Python dependencies: {', '.join(missing)}\033[0m")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages'] + missing)
        print("\033[1;32m[+] Python dependencies installed successfully!\033[0m")
        sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)

def run_checks():
    check_system_dependencies()
    check_python_dependencies()

if __name__ == "__main__":
    run_checks()

import os
import sys
from time import sleep
from tools.open_files import run as open_files
from tools.admin_finder import run as admin_finder

def display_header():
    os.system('clear && figlet Fuck_Isreal | lolcat 2>/dev/null || figlet Fuck_Isreal')
    print("\033[1;31mFuck Isreal By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\n")

def main_menu():
    display_header()
    tools = {
        '01': ("Open Files", open_files),
        '02': ("Admin Finder", admin_finder),
    }
    
    print(f"\033[1;33m[01]\033[0m Open Files\t\t\033[1;33m[02]\033[0m Admin Finder")
    print(f"\033[1;31m[99]\033[0m Exit\n")
    return tools

def main():
    while True:
        tools = main_menu()
        choice = input("\033[1;35mChoose an option: \033[0m").strip()
        
        if choice == '99':
            print("\033[1;31mExiting...\033[0m")
            sleep(1)
            sys.exit()
            
        elif choice in tools:
            os.system('clear')
            try:
                tools[choice][1]()
            except Exception as e:
                print(f"\033[1;31mError: {str(e)}\033[0m")
                sleep(3)
            finally:
                os.system('clear')
        else:
            print("\033[1;31mInvalid choice! Please try again.\033[0m")
            sleep(1)
            os.system('clear')

if __name__ == "__main__":
    main()
