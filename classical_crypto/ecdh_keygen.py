from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

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
        info=b'handshake data'
    ).derive(shared_A)

    key_B = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_B)

    return key_A, key_B


if __name__ == "__main__":
    key_A, key_B = generate_ecdh_keys()
    print("ECDH Key A:", key_A.hex())
    print("ECDH Key B:", key_B.hex())