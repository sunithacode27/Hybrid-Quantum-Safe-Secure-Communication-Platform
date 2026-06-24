import os
import hashlib

def generate_kyber_keys():
    private_key = os.urandom(32)
    public_key = hashlib.sha256(private_key).digest()
    return public_key, private_key

def kyber_shared_key(public_key, private_key):
    return hashlib.sha256(public_key + private_key).digest()

if __name__ == "__main__":
    pub, priv = generate_kyber_keys()
    shared = kyber_shared_key(pub, priv)

    print("Kyber Public Key:", pub.hex())
    print("Kyber Shared Key:", shared.hex())