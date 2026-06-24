import socket
import threading
import pickle
import os
import sqlite3
import datetime
import struct
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from PIL import Image, ImageTk

from crypto_utils import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket()

# ---------- USERNAME ----------
username = input("Enter your name: ")

# ---------- UI ----------
root = Tk()
root.title(f"🔐 Secure Chat - {username}")
root.geometry("500x550")
root.configure(bg="#1e1e2f")

chat_box = ScrolledText(root, wrap=WORD,
                        bg="#2c2c3c", fg="white",
                        font=("Arial", 11),
                        padx=10, pady=10)
chat_box.pack(padx=10, pady=10, fill=BOTH, expand=True)
chat_box.config(state=DISABLED)

# ---------- TAG STYLES ----------
chat_box.tag_config("you", foreground="white",
                    background="#00a884",
                    justify="right",
                    lmargin1=100, lmargin2=100,
                    rmargin=10)

chat_box.tag_config("friend", foreground="black",
                    background="#f0f0f0",
                    justify="left",
                    lmargin1=10, lmargin2=10,
                    rmargin=100)

chat_box.tag_config("system", foreground="gray", justify="center")
chat_box.tag_config("space", spacing1=10)

# ---------- INPUT ----------
frame = Frame(root, bg="#1e1e2f")
frame.pack(fill=X, padx=10, pady=10)

entry = Entry(frame, bg="#3c3c4f", fg="white",
              insertbackground="white", font=("Arial", 12))
entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

send_btn = Button(frame, text="Send",
                  bg="#00ffcc", fg="black",
                  font=("Arial", 10, "bold"))
send_btn.pack(side=RIGHT)

# ---------- LOG ----------
def log(message, sender="system", sender_name=""):
    chat_box.config(state=NORMAL)
    time = datetime.datetime.now().strftime("%H:%M")

    if sender == "you":
        chat_box.insert(END, "\n", "space")
        chat_box.insert(END, f"{username} [{time}]\n{message}\n", "you")
        chat_box.insert(END, "\n", "space")

    elif sender == "friend":
        chat_box.insert(END, "\n", "space")
        chat_box.insert(END, f"{sender_name} [{time}]\n{message}\n", "friend")
        chat_box.insert(END, "\n", "space")

    else:
        chat_box.insert(END, message + "\n\n", "system")

    chat_box.see(END)
    chat_box.config(state=DISABLED)




def show_image(image_path, sender="friend"):

    chat_box.config(state=NORMAL)

    img = Image.open(image_path)

    img.thumbnail((200, 200))

    photo = ImageTk.PhotoImage(img)

    chat_box.image_create(END, image=photo)

    if not hasattr(chat_box, "images"):
        chat_box.images = []

    chat_box.images.append(photo)

    chat_box.insert(END, "\n\n")

    chat_box.see(END)

    chat_box.config(state=DISABLED)

# ---------- SAFE SEND ----------
def send_full(data):
    data = pickle.dumps(data)
    length = struct.pack('!I', len(data))
    client.sendall(length + data)

# ---------- SAFE RECEIVE ----------
def recv_full():
    raw_len = client.recv(4)
    if not raw_len:
        return None

    length = struct.unpack('!I', raw_len)[0]

    data = b''
    while len(data) < length:
        packet = client.recv(4096)
        if not packet:
            return None
        data += packet

    return pickle.loads(data)





def save_message(sender, message, timestamp):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages(sender,message,timestamp) VALUES(?,?,?)",(sender, message, timestamp))

    conn.commit()
    conn.close()


def load_messages():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT sender, message, timestamp FROM messages"
    )

    rows = cursor.fetchall()
   
    print("Loaded rows:", rows)

    conn.close()

    for sender, message, timestamp in rows:

        if sender == username:
            log(message, "you")
        else:
            log(message, "friend", sender)
# ---------- CONNECT ----------
def connect():
      try:
        client.connect((HOST, PORT))
        log("Connected to server", "system")
        return True
      except Exception as e:
        log(f"[Connection Error] {e}", "system")
        return False

# ---------- RECEIVE ----------
def receive():
       while True:
        try:
            packet = recv_full()
            if not packet:
                break

            key = packet["kyber_key"]
            nonce = packet["nonce"]
            ct = packet["ciphertext"]
            tag = packet["tag"]
            sender_name = packet.get("name", "Friend")

            if packet.get("type") == "file":
                filename = packet["filename"]

                msg = decrypt_message(key, nonce, ct, tag)

                with open("received_" + filename, "wb") as f:
                    f.write(msg.encode('latin1'))
                    filepath = "received_" + filename

                if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                          show_image(filepath, "friend")
                else:
                 log(f"📁 Received file: {filename}", "friend", sender_name)

            else:
              msg = decrypt_message(key, nonce, ct, tag)

              log(msg, "friend", sender_name)

                 
        except Exception as e:
            log(f"[Receive Error] {e}", "system")
            break

# ---------- SEND MESSAGE ----------
def send_msg(event=None):
    msg = entry.get().strip()
    if not msg:
        return

    entry.delete(0, END)

    try:
        aes_key = os.urandom(32)
        nonce, ct, tag = encrypt_message(msg, aes_key)

        packet = {
            "kyber_key": aes_key,
            "nonce": nonce,
            "ciphertext": ct,
            "tag": tag,
            "name": username
        }

        send_full(packet)
        log(msg, "you")
        time = datetime.datetime.now().strftime("%H:%M")
        save_message(username, msg, time)
 
    except Exception as e:
        log(f"[Send Error] {e}", "system")

# ---------- SEND FILE ----------
def send_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        aes_key = os.urandom(32)
        nonce, ct, tag = encrypt_message(data.decode('latin1'), aes_key)

        packet = {
            "type": "file",
            "filename": os.path.basename(file_path),
            "kyber_key": aes_key,
            "nonce": nonce,
            "ciphertext": ct,
            "tag": tag,
            "name": username
        }

        send_full(packet)
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
           show_image(file_path, "you")
        else:
          log(f"📁 Sent file: {os.path.basename(file_path)}","you")
    except Exception as e:
        log(f"[File Send Error] {e}", "system")




# ---------- BUTTONS ----------
send_btn.config(command=send_msg)
entry.bind("<Return>", send_msg)

file_btn = Button(frame, text="📁",
                  bg="#ffaa00", fg="black",
                  font=("Arial", 10, "bold"),
                  command=send_file)
file_btn.pack(side=RIGHT, padx=5)

# ---------- START ----------
load_messages()

if connect():
    threading.Thread(target=receive, daemon=True).start()

root.mainloop()