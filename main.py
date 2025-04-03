#!/usr/bin/env python3
import os
import sys
from tools import open_files, admin_finder
from colorama import Fore, init
import pyfiglet

init(autoreset=True)
WIDTH = 80

def display_banner():
    os.system('clear')
    banner = pyfiglet.figlet_format("Fuck Isreal By Anonymous Jordan", font="slant")
    print(Fore.RED + banner)
    print(Fore.YELLOW + "="*WIDTH)
    print(Fore.RED + "Fuck Israel By: Anonymous Jordan Team".center(WIDTH))
    print(Fore.GREEN + "https://t.me/AnonymousJordan".center(WIDTH))
    print(Fore.YELLOW + "="*WIDTH + "\n")

def main():
    display_banner()
    
    tools = [
        ("01", "File Operations", "Manage files", open_files.py),
        ("02", "Admin Finder", "Find admin panels", admin_finder.py),
        ("99", "Exit", "Exit program", sys.exit)
    ]

    print(Fore.CYAN + "╒" + "═"*(WIDTH-2) + "╕")
    print(Fore.CYAN + "│" + 
          f"{'Tool ID'.center(10)}" + 
          f"{'Tool Name'.center(25)}" + 
          f"{'Description'.center(30)}" + 
          f"{'Status'.center(10)}" + 
          Fore.CYAN + "│")
    print(Fore.CYAN + "├" + "─"*10 + "┼" + "─"*25 + "┼" + "─"*30 + "┼" + "─"*10 + "┤")
    
    for tool in tools:
        status = Fore.GREEN + "Active" if tool[3] else Fore.RED + "Inactive"
        print(Fore.CYAN + "│" + 
              f"{Fore.YELLOW}{tool[0].center(8)} " + 
              f"{Fore.WHITE}{tool[1].ljust(23)} " + 
              f"{Fore.CYAN}{tool[2].ljust(28)} " + 
              f"{status.ljust(10)}" + 
              Fore.CYAN + "│")
    print(Fore.CYAN + "╘" + "═"*(WIDTH-2) + "╛")
    
    choice = input(f"\n{Fore.YELLOW}[{Fore.RED}#{Fore.YELLOW}] Select Option: ")
    
    for tool in tools:
        if choice == tool[0]:
            print(f"\n{Fore.GREEN}{'='*30}")
            print(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Launching {tool[1]}...")
            print(f"{Fore.GREEN}{'='*30}\n")
            tool[3]()
            return

if __name__ == "__main__":
    while True:
        main()
