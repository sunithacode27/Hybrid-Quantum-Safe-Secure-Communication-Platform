from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# 🔐 ENCRYPT FUNCTION
def encrypt_message(message):
    key = os.urandom(32)  # AES-256 key
    iv = os.urandom(16)   # IV

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    return key, iv, ciphertext


# 🔓 DECRYPT FUNCTION
def decrypt_message(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()


# ▶️ MAIN TEST
if __name__ == "__main__":
    msg = input("Enter message: ")

    key, iv, ct = encrypt_message(msg)

    print("\nEncrypted:", ct)

    decrypted = decrypt_message(key, iv, ct)

    print("Decrypted:", decrypted)