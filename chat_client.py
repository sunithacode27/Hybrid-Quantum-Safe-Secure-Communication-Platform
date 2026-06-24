from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
import os
import socket
import threading
import pickle

client = socket.socket()

print("Trying to connect...")
try:
    client.connect(('127.0.0.1', 5000))
    print("Connected! Start chatting...\n")
except Exception as e:
    print("Connection failed:", e)
    exit()


# 🔐 ENCRYPT
def encrypt_message(message, key):
    iv = os.urandom(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv + ciphertext)
    tag = h.digest()

    return iv, ciphertext, tag


# 🔓 DECRYPT
def decrypt_message(key, iv, ciphertext, tag):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(iv + ciphertext)

    h.verify(tag)  # raises error if tampered

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()


# 📥 RECEIVE THREAD
def receive():
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break

            packet = pickle.loads(data)

            key = packet["kyber_key"]
            iv = packet["iv"]
            ciphertext = packet["ciphertext"]
            tag = packet["tag"]

            msg = decrypt_message(key, iv, ciphertext, tag)

            print("\nFriend:", msg)
            print("You: ", end="", flush=True)

        except Exception as e:
            print("\n[Receive Error]", e)
            break


# 📤 SEND LOOP
def send():
    while True:
        try:
            msg = input("You: ")

            aes_key = os.urandom(32)

            iv, ciphertext, tag = encrypt_message(msg, aes_key)

            packet = {
                "kyber_key": aes_key,
                "iv": iv,
                "ciphertext": ciphertext,
                "tag": tag
            }

            client.send(pickle.dumps(packet))

        except Exception as e:
            print("\n[Send Error]", e)
            break


# 🚀 START CHAT
threading.Thread(target=receive, daemon=True).start()
send()