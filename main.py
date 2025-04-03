#!/usr/bin/env python3
import os
import sys
from tools import open_files, admin_finder
from colorama import Fore, Back, Style, init
import pyfiglet
from datetime import datetime

# ───═ Initialization ═──
init(autoreset=True)
WIDTH = 80

# ───═ Banner Design ═──
def display_banner():
    os.system('clear')
    banner = pyfiglet.figlet_format("Anonymous Tools", font="slant", justify="center")
    gradient_banner = []
    for line in banner.split('\n'):
        gradient_line = ""
        for i, char in enumerate(line):
            color_code = f"\033[38;2;{255};{0};{0 + i}m"
            gradient_line += f"{color_code}{char}"
        gradient_banner.append(gradient_line)
    print('\n'.join(gradient_banner))
    
    print(f"{Fore.RED}{'='*WIDTH}")
    print(f"{Fore.YELLOW}{'Fuck Israel By: Anonymous Jordan Team'.center(WIDTH)}")
    print(f"{Fore.CYAN}{'https://t.me/AnonymousJordan'.center(WIDTH)}")
    print(f"{Fore.RED}{'='*WIDTH}\n")

# ───═ Main Menu ═──
def main():
    display_banner()
    
    tools = [
        ("01", "File Operations", "Manage files with advanced options", open_files.run),
        ("02", "Admin Finder", "Discover admin panels with smart scanning", admin_finder.run),
        ("99", "Exit", "Terminate the program", sys.exit)
    ]

    # ───═ Menu Box ═──
    print(f"{Fore.MAGENTA}{'╒' + '═'*(WIDTH-2) + '╕'}")
    print(f"{Fore.MAGENTA}│{'Tool ID'.center(8)}│{'Tool Name'.center(25)}│{'Description'.center(35)}│{'Status'.center(10)}│")
    print(f"{Fore.MAGENTA}├" + "─"*8 + "┼" + "─"*25 + "┼" + "─"*35 + "┼" + "─"*10 + "┤")
    
    for tool in tools:
        status = f"{Fore.GREEN}Active" if tool[3] else f"{Fore.RED}Inactive"
        print(f"{Fore.MAGENTA}│{Fore.YELLOW} {tool[0].center(6)} {Fore.MAGENTA}│ {Fore.CYAN}{tool[1].ljust(23)} {Fore.MAGENTA}│ {Fore.WHITE}{tool[2].ljust(33)} {Fore.MAGENTA}│ {status.ljust(8)} {Fore.MAGENTA}│")
    
    print(f"{Fore.MAGENTA}╘" + "═"*(WIDTH-2) + "╛")
    
    try:
        choice = input(f"\n{Fore.YELLOW}[{Fore.RED}#{Fore.YELLOW}] Select Tool ({Fore.CYAN}01-02{Fore.YELLOW}/{Fore.RED}99{Fore.YELLOW}): {Fore.WHITE}")
        
        for tool in tools:
            if choice == tool[0]:
                print(f"\n{Fore.GREEN}{'='*30}")
                print(f"{Fore.YELLOW}[{Fore.GREEN}+{Fore.YELLOW}] Launching {tool[1]}...")
                print(f"{Fore.GREEN}{'='*30}\n")
                time.sleep(1)
                tool[3]()
                return
        
        print(f"\n{Fore.RED}[!] Invalid selection, returning to menu...")
        time.sleep(2)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[{Fore.RED}!{Fore.YELLOW}] Operation cancelled by user")
        time.sleep(1)

if __name__ == "__main__":
    while True:
        main()
