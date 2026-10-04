from ..cipher.cipher import BLOCK_SIZE, encrypt_block, decrypt_block
from ..utils.padding import pkcs7_pad, pkcs7_unpad

def encrypt_ecb(plaintext: bytes, key: bytes) -> bytes:
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE) 
    ciphertext = [] 
    
    for i in range(0, len(plaintext), BLOCK_SIZE): 
        block = plaintext[i:i + BLOCK_SIZE] 
        ciphertext.append(encrypt_block(block, key)) 
    
    return b"".join(ciphertext)

def decrypt_ecb(ciphertext: bytes, key: bytes) -> bytes:
    if len(ciphertext) == 0 or len(ciphertext) % BLOCK_SIZE != 0: 
        raise ValueError( f"Ciphertext length must be a non-zero multiple of {BLOCK_SIZE}" ) 
    
    plaintext = [] 
    
    for i in range(0, len(ciphertext), BLOCK_SIZE): 
        block = ciphertext[i:i + BLOCK_SIZE] 
        plaintext.append(decrypt_block(block, key)) 
    
    return pkcs7_unpad(b"".join(plaintext), BLOCK_SIZE)

if __name__ == "__main__":
    # NOTE:(to self). From root, do python -m src.modes.ecb

    key = b"KeyYoisakiKanade"

    plaintext = b"It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."

    print(f"Plaintext : {plaintext}")
    print(f"Key       : {key}")
    print()

    ciphertext = encrypt_ecb(plaintext, key)

    print(f"Ciphertext: {ciphertext}")

    decrypted = decrypt_ecb(ciphertext, key)

    print(f"Decrypted : {decrypted}")
    
    print()
    if decrypted == plaintext:
        print("Alhamdulillah")
    else:
        print("Waduh")