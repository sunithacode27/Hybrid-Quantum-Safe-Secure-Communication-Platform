import time
from pqcrypto.kem.ml_kem_768 import generate_keypair, encrypt, decrypt

start = time.perf_counter()

public_key, private_key = generate_keypair()

keygen_time = time.perf_counter() - start

start = time.perf_counter()

ciphertext, sender_secret = encrypt(public_key)

encrypt_time = time.perf_counter() - start

start = time.perf_counter()

receiver_secret = decrypt(private_key, ciphertext)

decrypt_time = time.perf_counter() - start

print("\n----- RESULTS -----")
print("Key Generation Time :", keygen_time)
print("Encapsulation Time  :", encrypt_time)
print("Decapsulation Time  :", decrypt_time)
print("Secret Match        :", sender_secret == receiver_secret)