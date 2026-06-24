import socket
import threading

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 5000))
server.listen(2)

print("Server started... Waiting for 2 clients")

client1, addr1 = server.accept()
print("Client 1 connected:", addr1)

client2, addr2 = server.accept()
print("Client 2 connected:", addr2)

print("Chat started!\n")


def forward(sender, receiver):
    while True:
        try:
            data = sender.recv(4096)
            if not data:
                break

            print("⚠️ Intercepted (encrypted):", data)
            receiver.send(data)

        except:
            break


threading.Thread(target=forward, args=(client1, client2), daemon=True).start()
threading.Thread(target=forward, args=(client2, client1), daemon=True).start()

while True:
    pass