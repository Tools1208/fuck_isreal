#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from time import sleep

# ───═ تكوين البيئة ═──
ROOT_DIR = Path(__file__).parent.absolute()
VENV_DIR = ROOT_DIR / "venv"
PYTHON = VENV_DIR / "bin" / "python"
PIP = VENV_DIR / "bin" / "pip"

def install_system_deps():
    # تثبيت اعتماديات النظام
    deps = ["figlet", "lolcat", "python3-venv"]
    missing = []
    
    for dep in deps:
        if subprocess.run(["dpkg", "-s", dep], stdout=subprocess.PIPE).returncode != 0:
            missing.append(dep)
    
    if missing:
        print(f"\033[1;33m[!] Installing system packages: {', '.join(missing)}\033[0m")
        subprocess.run(["sudo", "apt", "update"], stdout=subprocess.PIPE)
        subprocess.run(["sudo", "apt", "install", "-y"] + missing, stdout=subprocess.PIPE)

def create_virtualenv():
    # إنشاء بيئة افتراضية
    if not VENV_DIR.exists():
        print("\033[1;33m[!] Creating virtual environment...\033[0m")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR])
        sleep(2)

def install_python_deps():
    # تثبيت الاعتمادات داخل البيئة الافتراضية
    required = ["requests", "beautifulsoup4", "pyfiglet", "tqdm", "colorama"]
    subprocess.run([PIP, "install", "--no-warn-script-location"] + required)

def check_environment():
    # التحقق من الإعدادات
    if not PYTHON.exists() or not PIP.exists():
        create_virtualenv()
        install_python_deps()

def run_in_venv():
    # تشغيل البرنامج داخل البيئة الافتراضية
    os.execv(PYTHON, [PYTHON] + sys.argv)

if __name__ == "__main__":
    # إعداد البيئة عند التشغيل الأول
    install_system_deps()
    check_environment()
    
    # التأكد من أننا نعمل داخل البيئة الافتراضية
    if "VIRTUAL_ENV" not in os.environ:
        run_in_venv()

# ───═ الكود الرئيسي ═──
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
    print(subprocess.getoutput(f'{VENV_DIR}/bin/figlet Fuck_Isreal | lolcat 2>/dev/null || {VENV_DIR}/bin/figlet Fuck_Isreal'))
    print("\033[1;31mFuck Isreal By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\n")

class AdminFinder:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Finder v3.0")
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
    elif choice == "99":
        print("\033[1;31mExiting...\033[0m")
        sys.exit()
    else:
        print("\033[1;31mInvalid choice!\033[0m")
        sleep(1)
        main_menu()

if __name__ == "__main__":
    main_menu()
