#!/usr/bin/env python3
import os
import sys
from colorama import Fore, Style, init
import pyfiglet
from tools import open_files, admin_finder,

# ───═ Initialization ═──
init(autoreset=True)
WIDTH = 80

# ───═ Banner Design ═──
def display_banner():
    os.system('clear')
    banner_text = pyfiglet.figlet_format("Fuck Isreal", font="slant")
    gradient_banner = []
    for line in banner_text.split('\n'):
        gradient_line = ""
        for i, char in enumerate(line):
            r = 255
            g = min(50 + i*2, 255)
            b = 0
            gradient_line += f"\033[38;2;{r};{g};{b}m{char}"
        gradient_banner.append(gradient_line)
    print('\n'.join(gradient_banner))
    print(Fore.RED + "="*WIDTH)
    print(Fore.YELLOW + "Fuck Israel By: Anonymous Jordan Team".center(WIDTH))
    print(Fore.CYAN + "https://t.me/AnonymousJordan".center(WIDTH))
    print(Fore.RED + "="*WIDTH + "\n")

# ───═ Main Menu ═──
def main():
    display_banner()
    
    tools = [
        ("01", "File Operations", "Manage files", open_files.run),
        ("02", "Admin Finder", "Discover admin panels", admin_finder.run),
        ("99", "Exit", "Terminate the program", sys.exit)
    ]

    # ───═ Menu Box ═──
    print(Fore.MAGENTA + "╒" + "═"*(WIDTH-2) + "╕")
    print(Fore.MAGENTA + "│" + 
          f"{'ID'.center(8)}" + 
          f"{'Tool Name'.center(25)}" + 
          f"{'Description'.center(35)}" + 
          f"{'Status'.center(10)}" + 
          Fore.MAGENTA + "│")
    print(Fore.MAGENTA + "├" + "─"*8 + "┼" + "─"*25 + "┼" + "─"*35 + "┼" + "─"*10 + "┤")
    
    for tool in tools:
        status = f"{Fore.GREEN}Active" if tool[3] else f"{Fore.RED}Inactive"
        print(Fore.MAGENTA + "│" + 
              f"{Fore.YELLOW}{tool[0].center(6)} " + 
              f"{Fore.CYAN}{tool[1].ljust(23)} " + 
              f"{Fore.WHITE}{tool[2].ljust(33)} " + 
              f"{status.ljust(8)} " + 
              Fore.MAGENTA + "│")
    print(Fore.MAGENTA + "╘" + "═"*(WIDTH-2) + "╛")
    
    try:
        choice = input(f"\n{Fore.YELLOW}[{Fore.RED}#{Fore.YELLOW}] Select Option ({Fore.CYAN}01-03{Fore.YELLOW}/{Fore.RED}99{Fore.YELLOW}): ").strip()
        
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
