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

def run():
    print("\033[1;31mFuck Israel By  : Anonymous Jordan Team\033[0m")
    print("\033[1;31m Link  : https://t.me/AnonymousJordan\033[0m")
    
    print("""
\033[1;33mTool Features:\033[0m
\033[1;32m[1]\033[0m PBKDF2-HMAC with SHA256/SHA512
\033[1;32m[2]\033[0m Fernet symmetric decryption
\033[1;32m[3]\033[0m Multi-stage attacks: Wordlist + Mask + Hybrid + Brute-force
\033[1;32m[4]\033[0m Multiprocessing acceleration
\033[1;32m[5]\033[0m Customizable parameters (iterations, threads, charset)
\033[1;32m[6]\033[0m Mask attack support (?l, ?u, ?d, ?s)
\033[1;32m[7]\033[0m Configurable brute-force length (up to 8 chars)
""")
    
    print(pyfiglet.figlet_format("open_files.py", font="slant"))
    
    file_path = input("Encrypted file path: ").strip()
    if not os.path.exists(file_path):
        print("\033[1;31m[!] File not found\033[0m")
        return

    wordlist = input("Wordlist path (enter to skip): ").strip()
    mask_pattern = input("Mask pattern (e.g., Admin?d?d): ").strip()
    hash_algo = input("Hash [SHA256/SHA512] (default: SHA256): ").upper() or 'SHA256'
    iterations = int(input("PBKDF2 iterations (default: 500000): ") or 500000)
    threads = int(input(f"Threads (default: {os.cpu_count()}): ") or os.cpu_count())
    brute_length = int(input("Brute-force max length (default: 6): ") or 6)
    custom_charset = input("Custom charset (default: a-zA-Z0-9!@#$%^&*()): ").strip() or "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

    try:
        result = crack_file(
            file_path=file_path,
            wordlist=wordlist,
            mask_pattern=mask_pattern,
            hash_algo=hash_algo,
            iterations=iterations,
            threads=threads,
            brute_length=brute_length,
            custom_charset=custom_charset
        )
        
        if result:
            print(f"\n\033[1;32m[+] Password found: {result[0]}\033[0m")
            with open("decrypted_data.bin", "wb") as f:
                f.write(result[1])
            print(f"[+] Decrypted data saved to {os.path.abspath('decrypted_data.bin')}")
        else:
            print("\n\033[1;31m[-] Password not found\033[0m")
            
    except KeyboardInterrupt:
        print("\n\033[1;31m[-] Attack aborted\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")

def crack_file(file_path, wordlist=None, mask_pattern=None, hash_algo='SHA256', 
               iterations=500000, threads=os.cpu_count(),
               brute_length=6, custom_charset=None):
    
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
        args=(candidate_queue, wordlist, mask_pattern, brute_length, custom_charset)
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

def feed_candidates(queue, wordlist=None, mask_pattern=None, 
                   brute_length=6, custom_charset=None):
    # Wordlist phase
    if wordlist and os.path.exists(wordlist):
        with open(wordlist, 'r', encoding='latin-1') as f:
            for line in f:
                queue.put(line.strip())
    
    # Mask attack phase
    if mask_pattern:
        for candidate in generate_mask_candidates(mask_pattern):
            queue.put(candidate)
    
    # Hybrid attack phase
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    current_year = time.localtime().tm_year
    for year in range(current_year-3, current_year+1):
        queue.put(f"Admin{year}!")
        queue.put(f"Pass{year}@")
        queue.put(f"{seasons[(year//3)%4]}{year}")

    # Brute-force phase
    charset = custom_charset or "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    max_length = min(brute_length, 8)  # Limit to 8 characters max for practicality
    for length in range(1, max_length + 1):
        for chars in itertools.product(charset, repeat=length):
            queue.put(''.join(chars))
    
    # Terminate workers
    for _ in range(multiprocessing.cpu_count()):
        queue.put(None)
