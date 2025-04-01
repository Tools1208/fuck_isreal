import os
import sys
import subprocess
from time import sleep
from tkinter import *
from tkinter import ttk, messagebox
import requests
import threading
from bs4 import BeautifulSoup
import pyfiglet

def display_banner():
    os.system('clear')
    # استخدام figlet من داخل البيئة الافتراضية
    print(subprocess.getoutput(f'{sys.exec_prefix}/bin/figlet Fuck_Isreal | lolcat 2>/dev/null || {sys.exec_prefix}/bin/figlet Fuck_Isreal'))
    print("\033[1;31mFuck Isreal By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\n")

class AdminFinder:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Finder v4.0")
        self.master.geometry("800x600")
        
        self.paths = ["/admin", "/login", "/wp-admin", "/dashboard", "/controlpanel"]
        self.create_widgets()
    
    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        self.frame = ttk.Frame(self.master)
        self.frame.pack(pady=20)
        
        ttk.Label(self.frame, text="Target URL:").grid(row=0, column=0)
        self.url = ttk.Entry(self.frame, width=50)
        self.url.grid(row=0, column=1)
        self.url.insert(0, "http://")
        
        self.scan_btn = ttk.Button(self.frame, text="Start Scan", command=self.start_scan)
        self.scan_btn.grid(row=0, column=2, padx=5)
        
        self.result = ttk.Treeview(self.master, columns=("Status", "Type"))
        self.result.heading("#0", text="URL")
        self.result.heading("Status", text="Status")
        self.result.heading("Type", text="Type")
        self.result.pack(fill=BOTH, expand=True)
    
    def start_scan(self):
        target = self.url.get().strip()
        if not target.startswith(("http://", "https://")):
            messagebox.showerror("Error", "Invalid URL format")
            return
        
        threading.Thread(target=self.scan, args=(target,)).start()
    
    def scan(self, target):
        for path in self.paths:
            url = target.rstrip("/") + path
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    self.result.insert("", "end", text=url, values=(res.status_code, "Potential Admin"))
                else:
                    self.result.insert("", "end", text=url, values=(res.status_code, "Not Found"))
            except Exception as e:
                self.result.insert("", "end", text=url, values=("Error", str(e)))

def main_menu():
    display_banner()
    print("\033[1;33m[01]\033[0m Admin Finder")
    print("\033[1;31m[99]\033[0m Exit\n")
    
    choice = input("\033[1;35mChoose an option: \033[0m")
    
    if choice == "01":
        os.system('clear')
        root = Tk()
        app = AdminFinder(root)
        root.mainloop()
        main_menu()  # العودة للقائمة بعد الإغلاق
    elif choice == "99":
        print("\033[1;31mExiting...\033[0m")
        sys.exit()
    else:
        print("\033[1;31mInvalid choice!\033[0m")
        sleep(1)
        main_menu()

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Program interrupted by user\033[0m")
        sys.exit()
