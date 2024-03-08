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
  cipher = Cipher(algorithms.AES(key),
                  modes.CTR(iv),
                  backend=default_backend())
  encryptor = cipher.encryptor()
  with open(file_path, 'rb') as f:
    plaintext = f.read()
  padder = padding.PKCS7(128).padder()
  padded_data = padder.update(plaintext) + padder.finalize()
  ciphertext = encryptor.update(padded_data) + encryptor.finalize()
  with open(file_path, 'wb') as f:
    f.write(ciphertext)


def encrypt_folder(folder_path, key, iv):
  start_time = time.time()
  for root, dirs, files in os.walk(folder_path):
    for file in files:
      file_path = os.path.join(root, file)
      encrypt_file(file_path, key, iv)
  end_time = time.time()
  print(f"Encryption took {end_time - start_time} seconds")


encrypt_folder(folder_path, key, iv)
