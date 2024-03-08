import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Replace with key and IV
key = os.urandom(32)  # AES256 key
iv = os.urandom(16)  # CTR mode IV
folder_path = "test"

def encrypt_file(file_path, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    with open(file_path, 'rb') as in_file, open(file_path + '.enc', 'wb') as out_file:
        while True:
            chunk = in_file.read(64 * 1024)  # Read 64KB at a time
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)  
            out_file.write(encryptor.update(padder.update(chunk)))
        out_file.write(encryptor.update(padder.finalize()) + encryptor.finalize())

    os.remove(file_path)  
    os.rename(file_path + '.enc', file_path)  

def encrypt_folder(folder_path, key, iv):
    start_time = time.time()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key, iv)
    end_time = time.time()
    print(f"Encryption took {end_time - start_time} seconds")

encrypt_folder(folder_path, key, iv)
