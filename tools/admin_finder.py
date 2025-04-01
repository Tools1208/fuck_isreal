#!/usr/bin/env python3
import os
import sys
import urllib.parse
from threading import Lock, Thread
from requests import get
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema
from queue import Queue
from time import sleep
from tqdm import tqdm
import pyfiglet
from colorama import Fore, Style, init

# تهيئة الألوان
init(autoreset=True)

# الثوابت
VERSION = "4.0 Pro"
DEFAULT_WORDLIST = "list.txt"
DEFAULT_PATHS = [
    "admin", "admin.php", "admin.html", "admin/login.php",
    "administrator", "login", "wp-admin", "admin/dashboard",
    "dashboard", "admin_area", "controlpanel", "cp"
]

# ألوان خاصة
class Colors:
    HEADER = Fore.MAGENTA
    INFO = Fore.CYAN
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

def create_default_wordlist():
    """إنشاء قائمة مسارات افتراضية إذا لم تكن موجودة"""
    if not os.path.exists(DEFAULT_WORDLIST):
        with open(DEFAULT_WORDLIST, 'w') as f:
            for path in DEFAULT_PATHS:
                f.write(f"{path}\n")
        print(f"{Colors.SUCCESS}[+] تم إنشاء قائمة مسارات افتراضية: {DEFAULT_WORDLIST}")

def display_banner():
    """عرض الواجهة الرئيسية الملونة"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.HEADER + pyfiglet.figlet_format("AdminFinder", font="slant"))
    print(Colors.INFO + """
    ______   __  __     ______     __    __     ______     ______  
   /\  == \ /\ \_\ \   /\  ___\   /\ "-./  \   /\  __ \   /\__  _\ 
   \ \  _-/ \ \  __ \  \ \  __\   \ \ \-./\ \  \ \ \/\ \  \/_/\ \/ 
    \ \_\    \ \_\ \_\  \ \_____\  \ \_\ \ \_\  \ \_____\    \ \_\ 
     \/_/     \/_/\/_/   \/_____/   \/_/  \/_/   \/_____/     \/_/ 
    """.strip())
    print(f"{Colors.WARNING}{'='*60}")
    print(f"{Colors.INFO}{'Telegram: https://t.me/AnonymousJordan'.center(60)}")
    print(f"{Colors.HEADER}Version: {VERSION}".center(60))
    print(f"{Colors.WARNING}{'='*60}")

def validate_url(url):
    """التحقق من صحة الرابط وتنسيقه"""
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
    return url.rstrip("/") + "/"

def generate_url_variants(base_url):
    """إنشاء متغيرات مختلفة من الرابط للمسح الشامل"""
    parsed = urllib.parse.urlparse(base_url)
    schemes = ["http", "https"] if parsed.scheme not in ["http", "https"] else [parsed.scheme]
    subdomains = ["", "www."]
    
    variants = []
    for scheme in schemes:
        for sub in subdomains:
            netloc = sub + parsed.netloc.split(':', 1)[0]
            variants.append(urllib.parse.urlunparse((
                scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            )).rstrip("/") + "/")
    return list(set(variants))

def load_wordlist(wordlist_path):
    """تحميل قائمة المسارات مع إنشاء افتراضي إذا لزم الأمر"""
    # إنشاء القائمة الافتراضية إذا لم تكن موجودة
    if not os.path.exists(DEFAULT_WORDLIST):
        create_default_wordlist()
    
    # استخدام القائمة المحددة أو الافتراضية
    final_path = wordlist_path or DEFAULT_WORDLIST
    if not os.path.exists(final_path):
        print(f"{Colors.ERROR}[!] خطأ: لا يمكن العثور على الملف: {final_path}")
        return None
    
    with open(final_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scan_worker(url, proxy, delay, paths, results, progress):
    """وظيفة المسح المتعددة الخيوط"""
    lock = Lock()
    queue = Queue()
    
    def worker():
        while True:
            path = queue.get()
            if path is None:
                break
            try:
                full_url = url + path
                response = get(full_url, proxies=proxy, timeout=10, allow_redirects=True)
                if 200 <= response.status_code < 300:
                    with lock:
                        results.append((full_url, response.status_code))
                        print(f"\r{Colors.SUCCESS}[+] تم العثور: {full_url} (حالة: {response.status_code})")
                progress.update(1)
                sleep(delay)
            except Exception:
                progress.update(1)
                continue
            finally:
                queue.task_done()
    
    # بدء الخيوط
    threads = []
    for _ in range(10):
        thread = Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # إضافة المسارات للتنفيذ
    for path in paths:
        queue.put(path)
    
    # انتظار انتهاء المهام
    queue.join()
    
    # إيقاف الخيوط
    for _ in range(10):
        queue.put(None)
    for thread in threads:
        thread.join()

def main():
    create_default_wordlist()
    
    while True:
        display_banner()
        print(f"""
{Colors.INFO}[01]{Colors.RESET} بدء مسح لوحة التحكم
{Colors.WARNING}[99]{Colors.RESET} الخروج من الأداة
        """.strip())
        
        choice = input(f"\n{Colors.BOLD}اختر رقما: {Colors.RESET}").strip()
        if choice == '99':
            sys.exit(0)
        elif choice != '01':
            continue
        
        # الحصول على المدخلات
        target = input(f"\n{Colors.INFO}[+] أدخل الهدف (مثال: example.com): {Colors.RESET}").strip()
        proxy = input(f"{Colors.INFO}[+] أدخل البروكسي (http-1.2.3.4:8080): {Colors.RESET}").strip()
        delay = input(f"{Colors.INFO}[+] التأخير بين الطلبات (ثانية) [0]: {Colors.RESET}").strip() or '0'
        wordlist = input(f"{Colors.INFO}[+] مسار القائمة [اضغط Enter للتخطي]: {Colors.RESET}").strip()
        
        # معالجة المدخلات
        try:
            delay = int(delay)
            if delay < 0:
                raise ValueError
        except ValueError:
            print(f"{Colors.ERROR}[!] خطأ: التأخير يجب أن يكون عددًا صحيحًا موجبًا")
            sleep(2)
            continue
        
        # تحميل القائمة
        paths = load_wordlist(wordlist)
        if not paths:
            continue
        
        # إعداد البروكسي
        proxy_dict = None
        if proxy:
            try:
                proto, addr = proxy.split('-', 1)
                proxy_dict = {proto: addr}
            except ValueError:
                print(f"{Colors.ERROR}[!] خطأ في تنسيق البروكسي. المثال: http-1.2.3.4:8080")
                sleep(2)
                continue
        
        # التحقق من الرابط
        validated_url = validate_url(target)
        if not validated_url:
            print(f"{Colors.ERROR}[!] خطأ: رابط الهدف غير صالح")
            sleep(2)
            continue
        
        # إنشاء متغيرات الرابط
        url_variants = generate_url_variants(validated_url)
        print(f"\n{Colors.INFO}[i] جاري مسح {len(url_variants)} متغير رابط...")
        
        # بدء المسح
        results = []
        total_requests = len(url_variants) * len(paths)
        progress = tqdm(
            total=total_requests,
            unit="req",
            desc=f"{Colors.INFO}التقدم",
            dynamic_ncols=True,
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Colors.INFO, Colors.RESET)
        )
        
        for url in url_variants:
            scan_worker(url, proxy_dict, delay, paths, results, progress)
        
        progress.close()
        
        # عرض النتائج
        print(f"\n{Colors.BOLD}{'='*60}")
        if results:
            print(f"{Colors.SUCCESS}[+] تم العثور على {len(results)} لوحة تحكم:")
            for url, status in results:
                print(f"  {Colors.WARNING}-{Colors.RESET} {url} (حالة: {status})")
        else:
            print(f"{Colors.ERROR}[!] لم يتم العثور على أي لوحات تحكم")
        
        input(f"\n{Colors.INFO}اضغط Enter للعودة للقائمة الرئيسية...")

if __name__ == "__main__":
    main()
