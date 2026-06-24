from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hybrid.hybrid_key import generate_hybrid_key
key = generate_hybrid_key()

# Load key
with open("secret.key", "rb") as f:
    key = f.read()

filename = input("Enter encrypted file name: ")

with open(filename, "rb") as f:
    iv = f.read(16)
    ciphertext = f.read()

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

output_file = filename.replace(".pdf.enc", "_decrypted.pdf")

with open(output_file, "wb") as f:
    f.write(plaintext)

print("File decrypted successfully!")
print("Decrypted file:", output_file)