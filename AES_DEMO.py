from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 32-byte key for AES-256
key = get_random_bytes(32)

# Create cipher object
cipher = AES.new(key, AES.MODE_CBC)

# Message
message = b"Hello Mam, Hybrid Secure Message!"

# Encrypt
ciphertext = cipher.encrypt(pad(message, AES.block_size))

print("Encrypted Data:", ciphertext.hex())

# Decrypt
decipher = AES.new(key, AES.MODE_CBC, cipher.iv)
plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)

print("Decrypted Message:", plaintext.decode())