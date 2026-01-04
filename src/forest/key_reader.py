from cryptography.hazmat.primitives import serialization

def read_key(key_path: str):

    with open(key_path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)
