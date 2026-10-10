from .modes.cbc import encrypt_cbc, decrypt_cbc 
from .modes.cfb import encrypt_cfb, decrypt_cfb
from .modes.ctr import encrypt_ctr, decrypt_ctr
from .modes.ecb import encrypt_ecb, decrypt_ecb 
from .modes.ofb import encrypt_ofb, decrypt_ofb

def encrypt(plaintext: str, key: str, mode: str, iv: bytes = None, counter: bytes = None) -> bytes:
    plaintext = plaintext.encode("utf-8") 
    key = key.encode("utf-8") 
    mode = mode.lower()

    if mode == "cbc": 
        if iv is None: 
            raise ValueError("CBC mode requires an IV") 
        ciphertext = encrypt_cbc(plaintext, key, iv)
    
    elif mode == "cfb": 
        if iv is None: 
            raise ValueError("CFB mode requires an IV") 
        
        ciphertext = encrypt_cfb(plaintext, key, iv)

    elif mode == "ctr": 
        if counter is None: 
            raise ValueError("CTR mode requires a counter") 
        
        ciphertext = encrypt_cfb(plaintext, key, counter)

    elif mode == "ecb": 
        ciphertext = encrypt_ecb(plaintext, key)

    elif mode == "ofb": 
        if iv is None: 
            raise ValueError("OFB mode requires an IV") 
        
        ciphertext = encrypt_ofb(plaintext, key, iv)

    else: 
        raise ValueError(f"Unsupported mode: {mode}")

    return ciphertext

def decrypt(ciphertext: bytes, key: str, mode: str, iv: bytes = None, counter: bytes = None) -> str:
    key = key.encode("utf-8") 
    mode = mode.lower()

    if mode == "cbc": 
        if iv is None: 
            raise ValueError("CBC mode requires an IV") 
        plaintext = decrypt_cbc(ciphertext, key, iv)
    
    elif mode == "cfb": 
        if iv is None: 
            raise ValueError("CFB mode requires an IV") 
        
        plaintext = decrypt_cfb(ciphertext, key, iv)

    elif mode == "ctr": 
        if counter is None: 
            raise ValueError("CTR mode requires a counter") 
        
        plaintext = decrypt_cfb(ciphertext, key, counter)

    elif mode == "ecb": 
        plaintext = decrypt_ecb(ciphertext, key)

    elif mode == "ofb": 
        if iv is None: 
            raise ValueError("OFB mode requires an IV") 
        
        plaintext = decrypt_ofb(ciphertext, key, iv)

    else: 
        raise ValueError(f"Unsupported mode: {mode}")

    return plaintext.decode("utf-8")