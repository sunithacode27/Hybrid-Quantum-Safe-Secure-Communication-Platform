from pqcrypto.kem.ml_kem_768 import generate_keypair
from pqcrypto.kem.ml_kem_768 import encrypt
from pqcrypto.kem.ml_kem_768 import decrypt

from crypto_utils import encrypt_message, decrypt_message

# Receiver generates Kyber keys
public_key, private_key = generate_keypair()

# Sender gets shared secret
ciphertext_kyber, sender_secret = encrypt(public_key)

# Receiver gets same secret
receiver_secret = decrypt(private_key, ciphertext_kyber)

print("Same Secret:", sender_secret == receiver_secret)

# AES key from Kyber
aes_key = sender_secret[:32]

message = "Hello Quantum World"

iv, ct, tag = encrypt_message(message, aes_key)

decrypted = decrypt_message(aes_key, iv, ct, tag)

print("Original :", message)
print("Decrypted:", decrypted)