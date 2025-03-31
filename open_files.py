# tools/password_cracker.py
import os
import time
import itertools
import multiprocessing
import logging
from tqdm import tqdm
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken

class PasswordCracker:
    def __init__(self, file_path, wordlist=None, hash_algo='SHA256',
                 iterations=500000, threads=os.cpu_count()):
        self.file_path = file_path
        self.wordlist = wordlist
        self.hash_algo = getattr(hashes, hash_algo.upper(), hashes.SHA256)()
        self.iterations = iterations
        self.threads = threads
        self.load_encrypted_data()

    def load_encrypted_data(self):
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
            self.salt = data[:16]
            self.encrypted_data = data[16:]
        except Exception as e:
            raise ValueError(f"File error: {str(e)}")

    def generate_candidates(self):
        # Wordlist attack
        if self.wordlist and os.path.exists(self.wordlist):
            with open(self.wordlist, 'r', encoding='latin-1') as f:
                yield from (line.strip() for line in f)

        # Hybrid attack patterns
        seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        current_year = time.localtime().tm_year
        for year in range(current_year-3, current_year+1):
            yield from (f"{season}{year}" for season in seasons)
            yield from (f"Admin{year}!", f"Pass{year}@", f"Password{year}#")

        # Brute-force attack
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        for length in range(1, 8):
            yield from (''.join(chars) for chars in itertools.product(charset, repeat=length))

    def worker(self, candidate_queue, result_queue):
        backend = default_backend()
        while True:
            pwd = candidate_queue.get()
            if pwd is None:
                break

            try:
                kdf = PBKDF2HMAC(
                    algorithm=self.hash_algo,
                    length=32,
                    salt=self.salt,
                    iterations=self.iterations,
                    backend=backend
                )
                key = kdf.derive(pwd.encode())
                cipher = Fernet(key)
                decrypted = cipher.decrypt(self.encrypted_data)
                result_queue.put(('success', pwd, decrypted))
                return
            except InvalidToken:
                continue
            except Exception as e:
                result_queue.put(('error', str(e)))

    def start(self):
        start_time = time.time()
        manager = multiprocessing.Manager()
        candidate_queue = manager.Queue(maxsize=self.threads*2)
        result_queue = manager.Queue()

        pool = multiprocessing.Pool(
            processes=self.threads,
            initializer=self.worker,
            initargs=(candidate_queue, result_queue)
        )

        feeder = multiprocessing.Process(
            target=self._feed_candidates,
            args=(candidate_queue,)
        )
        feeder.start()

        try:
            with tqdm(desc="Progress", unit=" attempts") as pbar:
                while True:
                    result = result_queue.get()

                    if result[0] == 'success':
                        pool.terminate()
                        elapsed = time.time() - start_time
                        return f"Password found: {result[1]} in {elapsed:.2f}s"
                    elif result[0] == 'error':
                        logging.error(result[1])

                    pbar.update()

        except KeyboardInterrupt:
            pool.terminate()
            return "Attack aborted"
        finally:
            pool.close()
            pool.join()
            feeder.join()

    def _feed_candidates(self, queue):
        for candidate in self.generate_candidates():
            queue.put(candidate)
        for _ in range(self.threads):
            queue.put(None)
