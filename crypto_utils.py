from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
import os

def encrypt_message(message, key):
    iv = os.urandom(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv + ciphertext)
    tag = h.digest()

    return iv, ciphertext, tag


def decrypt_message(key, iv, ciphertext, tag):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv + ciphertext)
    h.verify(tag)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()