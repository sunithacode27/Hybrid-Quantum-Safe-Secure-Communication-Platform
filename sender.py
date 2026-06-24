import socket, pickle
from crypto_utils import encrypt_message

client = socket.socket()
client.connect(('localhost', 5000))

while True:
    msg = input("You: ")
    if msg.lower() == "exit":
        break

    key, iv, ciphertext = encrypt_message(msg)

    packet = {
        "key": key,
        "iv": iv,
        "ciphertext": ciphertext
    }

    client.send(pickle.dumps(packet))

client.close()