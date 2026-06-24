# main.py
# HYBRID QUANTUM-SAFE COMMUNICATION SYSTEM
# Classical: ECDH
# PQC: Kyber (Simulated Demo)
# Encryption: AES-GCM

import os
import time
import csv
import hashlib

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ==========================================
# 1. ECDH KEY GENERATION
# ==========================================
def generate_ecdh_keys():
    private_key_A = ec.generate_private_key(ec.SECP256R1())
    private_key_B = ec.generate_private_key(ec.SECP256R1())

    public_key_A = private_key_A.public_key()
    public_key_B = private_key_B.public_key()

    shared_A = private_key_A.exchange(ec.ECDH(), public_key_B)
    shared_B = private_key_B.exchange(ec.ECDH(), public_key_A)

    key_A = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake'
    ).derive(shared_A)

    key_B = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake'
    ).derive(shared_B)

    return key_A, key_B


# ==========================================
# 2. KYBER (SIMULATED DEMO)
# ==========================================
def generate_kyber_keys():
    private_key = os.urandom(32)
    public_key = hashlib.sha256(private_key).digest()
    return public_key, private_key


def kyber_shared_key(public_key, private_key):
    return hashlib.sha256(public_key + private_key).digest()


# ==========================================
# 3. HYBRID KEY
# ==========================================
def generate_hybrid_key():
    ecdh_A, ecdh_B = generate_ecdh_keys()

    pub, priv = generate_kyber_keys()
    pqc_key = kyber_shared_key(pub, priv)

    final_key = hashlib.sha256(ecdh_A + pqc_key).digest()

    return ecdh_A, pqc_key, final_key


# ==========================================
# 4. AES ENCRYPTION
# ==========================================
def encrypt_message(key, message):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    cipher = aes.encrypt(nonce, message.encode(), None)
    return nonce, cipher


def decrypt_message(key, nonce, cipher):
    aes = AESGCM(key)
    plain = aes.decrypt(nonce, cipher, None)
    return plain.decode()


# ==========================================
# 5. SAVE RESULTS
# ==========================================
def save_results(ecdh_time, pqc_time, hybrid_time):
    os.makedirs("results", exist_ok=True)

    with open("results/performance_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Execution Time (seconds)"])
        writer.writerow(["ECDH", ecdh_time])
        writer.writerow(["Kyber", pqc_time])
        writer.writerow(["Hybrid", hybrid_time])


# ==========================================
# 6. MAIN PROGRAM
# ==========================================
def main():
    print("=" * 60)
    print("🚀 HYBRID QUANTUM-SAFE COMMUNICATION SYSTEM")
    print("=" * 60)

    # ECDH Timing
    start = time.perf_counter()
    ecdh_key_A, ecdh_key_B = generate_ecdh_keys()
    ecdh_time = time.perf_counter() - start

    # Kyber Timing
    start = time.perf_counter()
    pub, priv = generate_kyber_keys()
    pqc_key = kyber_shared_key(pub, priv)
    pqc_time = time.perf_counter() - start

    # Hybrid Timing
    start = time.perf_counter()
    _, _, hybrid_key = generate_hybrid_key()
    hybrid_time = time.perf_counter() - start

    # Encryption Demo
    message = "Hello Mam, Hybrid Secure Message!"
    nonce, cipher = encrypt_message(hybrid_key, message)
    decrypted = decrypt_message(hybrid_key, nonce, cipher)

    # Output
    print("\n🔐 Classical ECDH Key :")
    print(ecdh_key_A.hex())

    print("\n🛡️ PQC Kyber Key :")
    print(pqc_key.hex())

    print("\n🚀 Final Hybrid Key :")
    print(hybrid_key.hex())

    print("\n📩 Original Message :", message)
    print("📬 Decrypted Message:", decrypted)

    print("\n📊 PERFORMANCE RESULTS")
    print("-" * 40)
    print("ECDH   :", round(ecdh_time, 6), "seconds")
    print("Kyber  :", round(pqc_time, 6), "seconds")
    print("Hybrid :", round(hybrid_time, 6), "seconds")

    save_results(ecdh_time, pqc_time, hybrid_time)

    print("\n✅ Results saved in results/performance_results.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()