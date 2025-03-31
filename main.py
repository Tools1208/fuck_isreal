#!/usr/bin/env python3
import os
import sys
from time import sleep

# Custom tool imports
from tools import open_files

# === Setup interface ===
os.system('clear')
os.system('figlet Fuck_Isreal | lolcat')
print("\033[1;31mFuck Isreal By  : Anonymous Jordan Team\033[0m".center(60))
print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
print("\n")

def main_menu():
    """Display main menu with tool integration"""
    # Print options 01-50
    print(f"\033[1;33m[01]\033[0m Open Files Tool", end="\t")
    for i in range(2, 51):
        num = f"{i:02d}"
        print(f"\033[1;33m[{num}]\033[0m Soon", end="\t" if i%5 !=0 else "\n")
    
    print(f"\n\033[1;31m[99]\033[0m Exit\n")

def main():
    while True:
        main_menu()
        choice = input("\033[1;35mChoose an option: \033[0m").strip()
        
        if choice == '99':
            print("\033[1;31mExiting...\033[0m")
            sleep(1)
            sys.exit()
            
        elif choice == '01':
            os.system('clear')
            try:
                open_files.run()  # Run the integrated tool
            except Exception as e:
                print(f"\033[1;31mError: {str(e)}\033[0m")
                sleep(3)
            finally:
                os.system('clear')
        
        elif choice.isdigit() and 2 <= int(choice) <= 50:
            print(f"\033[1;33m\nSelected tool {choice:0>2}\033[0m")
            print("\033[1;34mThis tool will be available soon!\033[0m")
            sleep(2)
            os.system('clear')
            
        else:
            print("\033[1;31mInvalid choice! Please try again.\033[0m")
            sleep(1)
            os.system('clear')

if __name__ == "__main__":
    if not os.path.exists("/usr/bin/figlet"):
        print("\033[1;31mError: figlet is not installed!\033[0m")
        print("Install using: sudo apt install figlet lolcat")
        sys.exit()
    main()
