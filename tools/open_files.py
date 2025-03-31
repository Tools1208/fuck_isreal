# tools/open_files.py
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

def run():
    """Main interface for the password cracking tool"""
    print("\033[1;36m=== Advanced Password Cracker v2.1 ===\033[0m")
    file_path = input("Enter encrypted file path: ").strip()
    
    if not os.path.exists(file_path):
        print("\033[1;31m[!] File not found\033[0m")
        return

    wordlist = input("Wordlist path (press enter to skip): ").strip()
    hash_algo = input("Hash algorithm [SHA256/SHA512] (default: SHA256): ").upper() or 'SHA256'
    iterations = int(input("PBKDF2 iterations (default: 500000): ") or 500000)
    threads = int(input(f"Threads (default: {os.cpu_count()}): ") or os.cpu_count())

    try:
        result = crack_file(
            file_path=file_path,
            wordlist=wordlist,
            hash_algo=hash_algo,
            iterations=iterations,
            threads=threads
        )
        
        if result:
            print(f"\n\033[1;32m[+] Password found: {result[0]}\033[0m")
            with open("decrypted_data.bin", "wb") as f:
                f.write(result[1])
            print(f"[+] Decrypted data saved to {os.path.abspath('decrypted_data.bin')}")
        else:
            print("\n\033[1;31m[-] Password not found\033[0m")
            
    except KeyboardInterrupt:
        print("\n\033[1;31m[-] Attack aborted by user\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")

def crack_file(file_path, wordlist=None, hash_algo='SHA256', 
               iterations=500000, threads=os.cpu_count()):
    """Core cracking function with multiprocessing"""
    with open(file_path, 'rb') as f:
        data = f.read()
    salt = data[:16]
    encrypted_data = data[16:]

    # Set up multiprocessing
    manager = multiprocessing.Manager()
    candidate_queue = manager.Queue(maxsize=threads*2)
    result_queue = manager.Queue()

    # Create process pool
    pool = multiprocessing.Pool(
        processes=threads,
        initializer=worker,
        initargs=(salt, encrypted_data, hash_algo, iterations, candidate_queue, result_queue)
    )

    # Start candidate feeder
    feeder = multiprocessing.Process(
        target=feed_candidates,
        args=(candidate_queue, wordlist)
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
    """Multiprocessing worker for decryption attempts"""
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

def feed_candidates(queue, wordlist=None):
    """Generate and feed password candidates"""
    # Phase 1: Wordlist attack
    if wordlist and os.path.exists(wordlist):
        with open(wordlist, 'r', encoding='latin-1') as f:
            for line in f:
                queue.put(line.strip())
    
    # Phase 2: Hybrid attack
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    current_year = time.localtime().tm_year
    for year in range(current_year-3, current_year+1):
        queue.put(f"Admin{year}!")
        queue.put(f"Pass{year}@")
        queue.put(f"{seasons[(year//3)%4]}{year}")

    # Phase 3: Brute-force attack
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    for length in range(1, 7):  # Up to 6 characters
        for chars in itertools.product(charset, repeat=length):
            queue.put(''.join(chars))
    
    # Send poison pills
    for _ in range(multiprocessing.cpu_count()):
        queue.put(None)
