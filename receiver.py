import socket, pickle
from crypto_utils import decrypt_message

client = socket.socket()
client.connect(('localhost', 5000))

print("Connected. Waiting...")

while True:
    data = client.recv(4096)
    if not data:
        break

    packet = pickle.loads(data)

    msg = decrypt_message(packet["key"], packet["iv"], packet["ciphertext"])
    print("Friend:", msg)

client.close()import socket
import threading

server = socket.socket()
server.bind(('localhost', 5000))
server.listen(2)

print("Server started...")

client1, addr1 = server.accept()
print("Client1 connected:", addr1)

client2, addr2 = server.accept()
print("Client2 connected:", addr2)


def forward(source, target):
    while True:
        data = source.recv(4096)
        if not data:
            break
        print("⚠️ Attacker intercepted:", data)
        target.send(data)


# Run both directions
threading.Thread(target=forward, args=(client1, client2)).start()
threading.Thread(target=forward, args=(client2, client1)).start()