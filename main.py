#!/usr/bin/env python3
import os
import sys
from time import sleep

def check_system_dependencies():
    # Check figlet installation
    if os.system("which figlet > /dev/null") != 0:
        print("\033[1;31mError: figlet is not installed!\033[0m")
        print("Install using: sudo apt install figlet")
        sys.exit(1)
    
    # Check lolcat installation
    if os.system("which lolcat > /dev/null") != 0:
        print("\033[1;31mError: lolcat is not installed!\033[0m")
        print("Install using: sudo apt install lolcat")
        sys.exit(1)

def check_python_dependencies():
    required = ['requests', 'cryptography', 'tqdm', 'pyfiglet', 'colorama']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\033[1;33m[!] Installing missing Python dependencies...\033[0m")
        os.system(f"pip3 install {' '.join(missing)} --break-system-packages")
        print("\033[1;32m[+] Dependencies installed successfully!\033[0m")
        sleep(2)
        os.execv(sys.executable, ['python3'] + sys.argv)

# Run system checks first
check_system_dependencies()
check_python_dependencies()

# Import tools after dependency checks
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
    
    # Print available tools
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
