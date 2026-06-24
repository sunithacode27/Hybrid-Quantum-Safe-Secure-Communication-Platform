from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

# AES-256 key (32 bytes)
from hybrid.hybrid_key import generate_hybrid_key
key=generate_hybrid_key()

# Save key for decryption
with open("secret.key", "wb") as f:
    f.write(key)

filename = input("Enter file name to encrypt: ")

with open(filename, "rb") as f:
    data = f.read()

cipher = AES.new(key, AES.MODE_CBC)
ciphertext = cipher.encrypt(pad(data, AES.block_size))

with open(filename + ".enc", "wb") as f:
    f.write(cipher.iv)
    f.write(ciphertext)

print("File encrypted successfully!")
print("Encrypted file:", filename + ".enc")
print("Key saved in secret.key")