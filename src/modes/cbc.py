from ..cipher.cipher import BLOCK_SIZE, encrypt_block, decrypt_block
from ..utils.padding import pkcs7_pad, pkcs7_unpad
from ..utils.xor import xor_blocks

def encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"IV must be exactly {BLOCK_SIZE} bytes")

    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)

    ciphertext = []
    previous = iv

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        xored_block = xor_blocks(block, previous)
        encrypted_block = encrypt_block(xored_block, key)
        ciphertext.append(encrypted_block)
        previous = encrypted_block

    return b"".join(ciphertext)

def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"IV must be exactly {BLOCK_SIZE} bytes")

    if len(ciphertext) == 0 or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError(f"Ciphertext length must be a multiple of {BLOCK_SIZE}")
    
    plaintext = []
    previous = iv

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        decrypted_block = decrypt_block(block, key)
        original_block = xor_blocks(decrypted_block, previous)
        plaintext.append(original_block)
        previous = block

    return pkcs7_unpad(b"".join(plaintext), BLOCK_SIZE)

if __name__ == "__main__":
    # NOTE:(to self). From root, do python -m src.modes.cbc

    key = b"KeyYoisakiKanade"
    iv  = b"FEDCBA9876543210"

    plaintext = b"It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."

    print(f"Plaintext : {plaintext}")
    print(f"Key       : {key}")
    print(f"IV        : {iv}")
    print()

    ciphertext = encrypt_cbc(plaintext, key, iv)

    print(f"Ciphertext: {ciphertext}")

    decrypted = decrypt_cbc(ciphertext, key, iv)

    print(f"Decrypted : {decrypted}")
    
    print()
    if decrypted == plaintext:
        print("Alhamdulillah")
    else:
        print("Waduh")