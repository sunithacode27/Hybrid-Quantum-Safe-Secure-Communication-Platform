from pqcrypto.kem.ml_kem_768 import generate_keypair
from pqcrypto.kem.ml_kem_768 import encrypt
from pqcrypto.kem.ml_kem_768 import decrypt


# Receiver generates keys
public_key, private_key = generate_keypair()

print("Public Key Length:", len(public_key))
print("Private Key Length:", len(private_key))

# Sender generates shared secret
ciphertext, sender_secret = encrypt(public_key)

# Receiver recovers same secret
receiver_secret = decrypt(private_key, ciphertext)

print("\nSender Secret:")
print(sender_secret.hex())

print("\nReceiver Secret:")
print(receiver_secret.hex())

print("\nMatch ?")
print(sender_secret == receiver_secret)