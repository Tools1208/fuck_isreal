#!/usr/bin/env python3
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

# ───═ ʙᴀɴɴᴇʀ ═──
def display_banner():
    os.system('clear')
    print(pyfiglet.figlet_format("Decrypter v2.3", font="slant"))
    print("\033[1;31mFuck Israel By  : Anonymous Jordan Team\033[0m".center(60))
    print("\033[1;32mLink  : https://t.me/AnonymousJordan\033[0m".center(60))
    print("\033[1;34m" + "="*60 + "\033[0m")

def exit_gracefully(signum, frame):
    """Handle exit signals"""
    print("\n\033[1;31m[!] Exiting...\033[0m")
    sys.exit(0)

def parse_arguments():
    """Handle command-line arguments"""
    import argparse
    parser = argparse.ArgumentParser(description="Advanced Decryption Tool")
    parser.add_argument('-m', '--mode', required=True, choices=['easy', 'medium', 'hard'],
                        help="Attack mode (easy|medium|hard)")
    parser.add_argument('-f', '--file', required=True, help="Encrypted file path")
    parser.add_argument('-w', '--wordlist', help="Wordlist path (required for easy mode)")
    parser.add_argument('--mask', help="Mask pattern (required for medium mode)")
    parser.add_argument('--hash', choices=['SHA256', 'SHA512'], default='SHA256',
                        help="Hash algorithm for hard mode")
    parser.add_argument('--iterations', type=int, default=500000,
                        help="PBKDF2 iterations for hard mode")
    parser.add_argument('--length', type=int, default=6,
                        help="Max brute-force length (1-8) for hard mode")
    return parser.parse_args()

def main():
    display_banner()
    args = parse_arguments()
    
    # Validate required parameters
    if args.mode == 'easy' and not args.wordlist:
        print("\033[1;31m[!] Wordlist is required for easy mode\033[0m")
        sys.exit(1)
    if args.mode == 'medium' and not args.mask:
        print("\033[1;31m[!] Mask is required for medium mode\033[0m")
        sys.exit(1)
    
    try:
        if args.mode == 'easy':
            result = easy_mode(args.file, args.wordlist)
        elif args.mode == 'medium':
            result = medium_mode(args.file, args.mask)
        elif args.mode == 'hard':
            result = hard_mode(args.file, args.hash, args.iterations, args.length)
        
        if result:
            print(f"\033[1;32m[+] Password found: {result[0]}\033[0m")
            with open("decrypted_data.bin", "wb") as f:
                f.write(result[1])
            print(f"[+] Data saved to {os.path.abspath('decrypted_data.bin')}")
        else:
            print("\033[1;31m[-] Password not found\033[0m")
    
    except KeyboardInterrupt:
        exit_gracefully(None, None)
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
        sys.exit(1)

def easy_mode(file_path, wordlist):
    display_banner()
    print("\033[1;32m=== Easy Mode: Fernet Wordlist Attack ===\033[0m")
    if not os.path.exists(file_path) or not os.path.exists(wordlist):
        print("\033[1;31m[!] File(s) not found!\033[0m")
        return
    
    return crack_file(
        file_path=file_path,
        mode='wordlist',
        wordlist=wordlist
    )

def medium_mode(file_path, mask):
    display_banner()
    print("\033[1;33m=== Medium Mode: Hybrid + Mask Attack ===\033[0m")
    if not os.path.exists(file_path):
        print("\033[1;31m[!] File not found!\033[0m")
        return
    
    return crack_file(
        file_path=file_path,
        mode='hybrid',
        mask=mask
    )

def hard_mode(file_path, hash_algo, iterations, brute_length):
    display_banner()
    print("\033[1;31m=== Hard Mode: Brute-force PBKDF2 ===\033[0m")
    if not os.path.exists(file_path):
        print("\033[1;31m[!] File not found!\033[0m")
        return
    
    return crack_file(
        file_path=file_path,
        mode='brute',
        hash_algo=hash_algo,
        iterations=iterations,
        brute_length=brute_length
    )

# ... [keep the existing crack_file, worker, and generate_mask_candidates functions] ...

if __name__ == "__main__":
    # Handle exit signals
    import signal
    signal.signal(signal.SIGINT, exit_gracefully)
    
    try:
        main()
    except Exception as e:
        print(f"\033[1;31m[!] Fatal Error: {str(e)}\033[0m")
        sys.exit(1)
