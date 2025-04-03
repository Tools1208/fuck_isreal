#!/usr/bin/env python3
import tkinter as tk
import requests
import threading
from tkinter import ttk, messagebox
import sys
import os
import re
import tempfile
import webbrowser
import time
import pyfiglet

# ───═ ʙᴀɴɴᴇʀ ═──
def print_banner():
    os.system('clear')
    print("\033[1;31mFuck Israel By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\033[1;35m" + pyfiglet.figlet_format("Admin Finder").center(60) + "\033[0m")

print_banner()

# ───═ ᴄʟᴀss ᴅᴇғɪɴɪᴛɪᴏɴ ═──
class AdminHunterX:
    def __init__(self, master):
        self.master = master
        self.master.title("WebAdmin Auditor Pro v9.11")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.exit_app)  # Handle window close button
        
        self.common_paths = [
            "/admin", "/wp-admin", "/administrator", "/login",
            "/controlpanel", "/dashboard", "/adm", "/manager"
        ]
        
        self.scan_active = False
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        main_frame = ttk.Frame(self.master)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Input Section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Target URL:").pack(side=tk.LEFT, padx=5)
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.url_entry.insert(0, "http://")
        
        self.scan_btn = ttk.Button(input_frame, text="L33T SCAN", command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Change MAIN MENU button to exit the application
        self.exit_btn = ttk.Button(input_frame, text="EXIT", command=self.exit_app)
        self.exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Results Section
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_tree = ttk.Treeview(results_frame, columns=("Status", "Type"))
        self.result_tree.heading("#0", text="URL")
        self.result_tree.heading("Status", text="Status")
        self.result_tree.heading("Type", text="Type")
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.result_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.configure(yscrollcommand=vsb.set)
        
        # Status Bar
        self.status_bar = ttk.Label(self.master, text="[+] Ready to pwn", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def start_scan(self):
        if not self.validate_url():
            return
            
        if self.scan_active:
            messagebox.showwarning("Scan Active", "A scan is already in progress!")
            return
            
        self.scan_active = True
        self.scan_btn.config(state=tk.DISABLED)
        self.status_bar.config(text="[+] Enumerating attack surface...")
        
        threading.Thread(target=self.admin_hunt, daemon=True).start()

    def admin_hunt(self):
        target = self.url_entry.get().strip()
        found = []
        
        for path in self.common_paths:
            try:
                url = target.rstrip('/') + path
                response = requests.get(url, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    if self.is_admin_page(response.text):
                        self.add_result(url, response.status_code, "High Confidence")
                elif 300 <= response.status_code < 400:
                    self.add_result(url, "Redirect", response.headers['Location'])
                else:
                    self.add_result(url, response.status_code, "Not Found")
            except Exception as e:
                self.add_result(url, "Error", str(e))
        
        self.scan_active = False
        self.scan_btn.config(state=tk.NORMAL)
        self.status_bar.config(text=f"[+] Scan completed - {len(found)} potential admin pages found")

    def add_result(self, url, status, type_):
        self.master.after(0, self.result_tree.insert, "", "end", 
                        {"text": url, "values": (status, type_)})

    def is_admin_page(self, content):
        keywords = ['login', 'admin', 'dashboard', 'control panel']
        return any(keyword in content.lower() for keyword in keywords)

    def validate_url(self):
        url = self.url_entry.get().strip()
        regex = re.compile(
            r'^(http|https)://'
            r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            r'(:\d+)?'
            r'(/.*)?$'
        )
        if not regex.match(url):
            messagebox.showerror("Invalid URL", "Please enter a valid URL (e.g., http://example.com)")
            return False
        return True

    def exit_app(self):
        """Gracefully exit the application"""
        self.master.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AdminHunterX(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application crashed: {str(e)}")
        sys.exit(1)
