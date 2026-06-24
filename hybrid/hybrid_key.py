import hashlib
import sys   
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classical_crypto.ecdh_keygen import generate_ecdh_keys
from pqc.kyber import generate_kyber_keys, kyber_shared_key


def generate_hybrid_key():
    key_A, key_B = generate_ecdh_keys()
    
    pub, priv = generate_kyber_keys()
    pqc_key = kyber_shared_key(pub, priv)

    final_key = hashlib.sha256(key_A + pqc_key).digest()

    return final_key


if __name__ == "__main__":
    hybrid_key = generate_hybrid_key()

    print("🚀 Hybrid Quantum-Safe Key Generated")
    print("🔐 Final Key:", hybrid_key.hex())