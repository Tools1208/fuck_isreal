import os
import sys
import time
import itertools
import multiprocessing
from tqdm import tqdm
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
import pyfiglet

def display_banner():
    os.system('clear')
    print(pyfiglet.figlet_format("Decrypter v2.3", font="slant"))
    print("\033[1;31mFuck Israel By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\033[1;34m" + "="*60 + "\033[0m")

def show_menu():
    print("""
\033[1;33m[01]\033[0m Easy Mode   \033[1;32m(Fernet Wordlist Attack)\033[0m
\033[1;33m[02]\033[0m Medium Mode \033[1;32m(Hybrid + Mask Attack)\033[0m
\033[1;33m[03]\033[0m Hard Mode   \033[1;32m(Brute-force PBKDF2)\033[0m
\033[1;31m[99]\033[0m Return to Main Menu

\033[1;34mUsage Tips:\033[0m
- Use 'rockyou.txt' for wordlist attacks
- Mask format: ?l (lower), ?u (upper), ?d (digits), ?s (symbols)
- Brute-force supports up to 8 characters
""")

def run():
    display_banner()
    show_menu()
    
    while True:
        choice = input("\033[1;35mSelect Attack Mode: \033[0m").strip()
        
        if choice == '99':
            print("\033[1;31mReturning to main menu...\033[0m")
            time.sleep(1)
            return
            
        elif choice in ['1', '01']:
            easy_mode()
            
        elif choice in ['2', '02']:
            medium_mode()
            
        elif choice in ['3', '03']:
            hard_mode()
            
        else:
            print("\033[1;31m[!] Invalid choice! Try again\033[0m")
            time.sleep(1)
            display_banner()
            show_menu()

def easy_mode():
    display_banner()
    print("\033[1;32m=== Easy Mode: Fernet Wordlist Attack ===\033[0m")
    
    file_path = input("Encrypted file path: ").strip()
    wordlist = input("Wordlist path: ").strip()
    
    if not (os.path.exists(file_path) and os.path.exists(wordlist)):
        print("\033[1;31m[!] File(s) not found!\033[0m")
        return

    try:
        result = crack_file(
            file_path=file_path,
            mode='wordlist',
            wordlist=wordlist
        )
        
        if result:
            print(f"\n\033[1;32m[+] Password found: {result[0]}\033[0m")
            with open("decrypted_data.bin", "wb") as f:
                f.write(result[1])
            print(f"[+] Data saved to {os.path.abspath('decrypted_data.bin')}")
        else:
            print("\n\033[1;31m[-] Password not found\033[0m")
            
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")

def medium_mode():
    display_banner()
    print("\033[1;33m=== Medium Mode: Hybrid + Mask Attack ===\033[0m")
    
    file_path = input("Encrypted file path: ").strip()
    mask = input("Mask pattern (e.g., Admin?d?d): ").strip()
    
    if not os.path.exists(file_path):
        print("\033[1;31m[!] File not found!\033[0m")
        return

    try:
        result = crack_file(
            file_path=file_path,
            mode='hybrid',
            mask=mask
        )
        
        if result:
            print(f"\n\033[1;32m[+] Password found: {result[0]}\033[0m")
            with open("decrypted_data.bin", "wb") as f:
                f.write(result[1])
            print(f"[+] Data saved to {os.path.abspath('decrypted_data.bin')}")
        else:
            print("\n\033[1;31m[-] Password not found\033[0m")
            
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")

def hard_mode():
    display_banner()
    print("\033[1;31m=== Hard Mode: Brute-force PBKDF2 ===\033[0m")
    
    file_path = input("Encrypted file path: ").strip()
    hash_algo = input("Hash [SHA256/SHA512] (default: SHA256): ").upper() or 'SHA256'
    iterations = int(input("PBKDF2 iterations: ") or 500000)
    brute_length = int(input("Max length (1-8): ") or 6)
    
    if not os.path.exists(file_path):
        print("\033[1;31m[!] File not found!\033[0m")
        return

    try:
        result = crack_file(
            file_path=file_path,
            mode='brute',
            hash_algo=hash_algo,
            iterations=iterations,
            brute_length=brute_length
        )
        
        if result:
            print(f"\n\033[1;32m[+] Password found: {result[0]}\033[0m")
            with open("decrypted_data.bin", "wb") as f:
                f.write(result[1])
            print(f"[+] Data saved to {os.path.abspath('decrypted_data.bin')}")
        else:
            print("\n\033[1;31m[-] Password not found\033[0m")
            
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")

def crack_file(**kwargs):
    mode = kwargs.get('mode')
    file_path = kwargs.get('file_path')
    hash_algo = kwargs.get('hash_algo', 'SHA256')
    iterations = kwargs.get('iterations', 500000)
    threads = kwargs.get('threads', os.cpu_count())
    
    with open(file_path, 'rb') as f:
        data = f.read()
    salt = data[:16]
    encrypted_data = data[16:]

    manager = multiprocessing.Manager()
    candidate_queue = manager.Queue(maxsize=threads*2)
    result_queue = manager.Queue()

    pool = multiprocessing.Pool(
        processes=threads,
        initializer=worker,
        initargs=(salt, encrypted_data, hash_algo, iterations, candidate_queue, result_queue)
    )

    feeder = multiprocessing.Process(
        target=feed_candidates,
        args=(candidate_queue,),
        kwargs={
            'mode': mode,
            'wordlist': kwargs.get('wordlist'),
            'mask': kwargs.get('mask'),
            'brute_length': kwargs.get('brute_length', 6),
            'custom_charset': kwargs.get('custom_charset', None)
        }
    )
    feeder.start()

    try:
        with tqdm(desc="Progress", unit=" attempts") as pbar:
            while True:
                result = result_queue.get()
                
                if result and result[0] == 'success':
                    pool.terminate()
                    return (result[1], result[2])
                    
                pbar.update()
                
    except KeyboardInterrupt:
        pool.terminate()
        raise
    finally:
        pool.close()
        pool.join()
        feeder.join()

def worker(salt, encrypted_data, hash_algo, iterations, candidate_queue, result_queue):
    backend = default_backend()
    hash_class = getattr(hashes, hash_algo.upper(), hashes.SHA256)
    
    kdf = PBKDF2HMAC(
        algorithm=hash_class(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    
    while True:
        pwd = candidate_queue.get()
        if pwd is None:
            break
            
        try:
            key = kdf.derive(pwd.encode())
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_data)
            result_queue.put(('success', pwd, decrypted))
            return
        except InvalidToken:
            continue
        except Exception as e:
            result_queue.put(('error', str(e)))

def feed_candidates(queue, **kwargs):
    mode = kwargs.get('mode')
    wordlist = kwargs.get('wordlist')
    mask = kwargs.get('mask')
    brute_length = kwargs.get('brute_length', 6)
    custom_charset = kwargs.get('custom_charset')

    # Wordlist attack
    if mode == 'wordlist' and wordlist:
        if os.path.exists(wordlist):
            with open(wordlist, 'r', encoding='latin-1') as f:
                for line in f:
                    queue.put(line.strip())

    # Hybrid + Mask attack
    if mode == 'hybrid':
        # Mask attack
        if mask:
            for candidate in generate_mask_candidates(mask):
                queue.put(candidate)
        # Common patterns
        seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        current_year = time.localtime().tm_year
        for year in range(current_year-3, current_year+1):
            queue.put(f"Admin{year}!")
            queue.put(f"Pass{year}@")
            queue.put(f"{seasons[(year//3)%4]}{year}")

    # Brute-force attack
    if mode == 'brute':
        charset = custom_charset or "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        max_length = min(brute_length, 8)
        for length in range(1, max_length + 1):
            for chars in itertools.product(charset, repeat=length):
                queue.put(''.join(chars))
    
    # Terminate workers
    for _ in range(multiprocessing.cpu_count()):
        queue.put(None)

def generate_mask_candidates(mask):
    char_map = {
        '?l': 'abcdefghijklmnopqrstuvwxyz',
        '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '?d': '0123456789',
        '?s': '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
    }
    
    fixed = []
    variables = []
    current_fixed = []
    i = 0
    while i < len(mask):
        if mask[i] == '?' and i + 1 < len(mask):
            key = mask[i:i+2]
            if key in char_map:
                if current_fixed:
                    fixed.append(''.join(current_fixed))
                    current_fixed = []
                variables.append(char_map[key])
                i += 2
            else:
                current_fixed.append(mask[i])
                i += 1
        else:
            current_fixed.append(mask[i])
            i += 1
    if current_fixed:
        fixed.append(''.join(current_fixed))
    
    if not variables:
        return [''.join(fixed)]
    
    variable_chars = [list(var) for var in variables]
    for combo in itertools.product(*variable_chars):
        result = []
        fixed_iter = iter(fixed)
        var_iter = iter(combo)
        done = False
        while not done:
            try:
                result.append(next(fixed_iter))
            except StopIteration:
                pass
            try:
                result.append(next(var_iter))
            except StopIteration:
                done = True
        yield ''.join(result).replace('\n', '')
