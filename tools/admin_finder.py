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

# ثوابت الألوان
COLORS = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'END': '\033[0m'
}

# الثوابت العامة
BANNER = r"""
 ______   __  __     ______     __    __     ______     ______  
/\  == \ /\ \_\ \   /\  ___\   /\ "-./  \   /\  __ \   /\__  _\ 
\ \  _-/ \ \  __ \  \ \  __\   \ \ \-./\ \  \ \ \/\ \  \/_/\ \/ 
 \ \_\    \ \_\ \_\  \ \_____\  \ \_\ \ \_\  \ \_____\    \ \_\ 
  \/_/     \/_/\/_/   \/_____/   \/_/  \/_/   \/_____/     \/_/ 
"""
VERSION = "3.0 Pro"
DEFAULT_WORDLIST = os.path.join(os.path.dirname(__file__), 'list.txt')

def display_banner():
    """عرض الواجهة الرئيسية مع الألوان"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(COLORS['CYAN'], end='')
    print(pyfiglet.figlet_format("AdminFinder", font="slant", justify="center"))
    print(COLORS['YELLOW'] + BANNER + COLORS['END'])
    print(f"{COLORS['RED']}{'='*60}{COLORS['END']}")
    print(f"{COLORS['GREEN']}{'Telegram: https://t.me/AnonymousJordan'.center(60)}{COLORS['END']}")
    print(f"{COLORS['CYAN']}Version: {VERSION}{COLORS['END']}".center(60))
    print(f"{COLORS['RED']}{'='*60}{COLORS['END']}\n")

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
    variants = []
    schemes = ["http", "https"] if parsed.scheme not in ["http", "https"] else [parsed.scheme]
    subdomains = ["", "www."]
    
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
    """تحميل قائمة المسارات من الملف"""
    if not wordlist_path:
        return []
        
    if not os.path.isfile(wordlist_path):
        print(f"{COLORS['RED']}[!] خطأ: ملف القائمة غير موجود '{wordlist_path}'{COLORS['END']}")
        return None
    with open(wordlist_path, 'r') as f:
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
                        print(f"\r{COLORS['GREEN']}[+] تم العثور: {full_url} (حالة: {response.status_code}){COLORS['END']}")
                progress.update(1)
                sleep(delay)
            except (ConnectionError, InvalidSchema, MissingSchema):
                progress.update(1)
                continue
            finally:
                queue.task_done()
    
    # بدء خيوط العمل
    threads = []
    for _ in range(10):
        thread = Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # إضافة المسارات إلى قائمة الانتظار
    for path in paths:
        queue.put(path)
    
    # انتظار اكتمال جميع المهام
    queue.join()
    
    # إيقاف الخيوط
    for _ in range(10):
        queue.put(None)
    for thread in threads:
        thread.join()

def main():
    try:
        while True:
            display_banner()
            print(f"{COLORS['YELLOW']}أدخل '99' في أي وقت للعودة للقائمة الرئيسية{COLORS['END']}\n")
            
            # الحصول على مدخلات المستخدم مع إمكانية العودة
            target = input(f"{COLORS['CYAN']}[+] أدخل الهدف (مثال: example.com): {COLORS['END']}").strip()
            if target == '99':
                continue
                
            proxy_input = input(f"{COLORS['CYAN']}[+] أدخل البروكسي (http-1.2.3.4:8080): {COLORS['END']}").strip()
            if proxy_input == '99':
                continue
                
            delay = input(f"{COLORS['CYAN']}[+] أدخل التأخير بين الطلبات (ثانية) [0]: {COLORS['END']}").strip()
            if delay == '99':
                continue
            try:
                delay = int(delay) if delay else 0
                if delay < 0:
                    raise ValueError
            except ValueError:
                print(f"{COLORS['RED']}[!] خطأ: التأخير يجب أن يكون عددًا صحيحًا موجبًا{COLORS['END']}")
                sleep(2)
                continue
                
            wordlist = input(f"{COLORS['CYAN']}[+] أدخل مسار القائمة (اضغط Enter للتخطي): {COLORS['END']}").strip()
            if wordlist == '99':
                continue
            wordlist = wordlist or DEFAULT_WORDLIST
                
            # التحقق من الرابط المستهدف
            validated_url = validate_url(target)
            if not validated_url:
                print(f"{COLORS['RED']}[!] خطأ: رابط الهدف غير صالح{COLORS['END']}")
                sleep(2)
                continue
                
            # تحميل القائمة
            paths = load_wordlist(wordlist)
            if not paths:
                print(f"{COLORS['YELLOW']}[!] تستخدم القائمة الافتراضية: {DEFAULT_WORDLIST}{COLORS['END']}")
                sleep(2)
                paths = load_wordlist(DEFAULT_WORDLIST)
                
            # إعداد البروكسي
            proxy = None
            if proxy_input:
                try:
                    proto, addr = proxy_input.split('-', 1)
                    proxy = {proto: addr}
                except ValueError:
                    print(f"{COLORS['RED']}[!] خطأ في تنسيق البروكسي. المثال: http-1.2.3.4:8080{COLORS['END']}")
                    sleep(2)
                    continue
            
            # إنشاء متغيرات الرابط
            url_variants = generate_url_variants(validated_url)
            print(f"\n{COLORS['YELLOW']}[i] جاري مسح {len(url_variants)} متغير رابط...{COLORS['END']}")
            
            # بدء المسح
            results = []
            total_requests = len(url_variants) * len(paths)
            progress = tqdm(total=total_requests, unit="req", desc="التقدم", dynamic_ncols=True, 
                           bar_format="{l_bar}%s{bar}%s{r_bar}" % (COLORS['CYAN'], COLORS['END']))
            
            for url in url_variants:
                scan_worker(url, proxy, delay, paths, results, progress)
            
            progress.close()
            
            # عرض النتائج
            if results:
                print(f"\n{COLORS['GREEN']}[+] تم العثور على لوحات تحكم:{COLORS['END']}")
                for url, status in results:
                    print(f"  {COLORS['YELLOW']}-{COLORS['END']} {url} (حالة: {status})")
            else:
                print(f"\n{COLORS['RED']}[!] لم يتم العثور على لوحات تحكم{COLORS['END']}")
            
            input(f"\n{COLORS['CYAN']}اضغط Enter للعودة للقائمة الرئيسية...{COLORS['END']}")
                
    except KeyboardInterrupt:
        print(f"\n{COLORS['RED']}[!] تم إيقاف الأداة بواسطة المستخدم{COLORS['END']}")
        sys.exit(0)

if __name__ == "__main__":
    main()
