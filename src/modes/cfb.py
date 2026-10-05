from ..cipher.cipher import BLOCK_SIZE, encrypt_block, decrypt_block
from ..utils.xor import xor_blocks

def encrypt_cfb(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != BLOCK_SIZE: 
        raise ValueError(f"IV must be exactly {BLOCK_SIZE} bytes")

    ciphertext = [] 
    previous = iv

    for i in range(0, len(plaintext), BLOCK_SIZE): 
        block = plaintext[i:i + BLOCK_SIZE]
        keystream = encrypt_block(previous, key) 
        
        encrypted_block = xor_blocks(block, keystream[:len(block)]) 
        ciphertext.append(encrypted_block)  
        previous = encrypted_block 
    
    return b"".join(ciphertext)

def decrypt_cfb(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != BLOCK_SIZE: 
        raise ValueError(f"IV must be exactly {BLOCK_SIZE} bytes")

    plaintext = [] 
    previous = iv

    for i in range(0, len(ciphertext), BLOCK_SIZE): 
        block = ciphertext[i:i + BLOCK_SIZE] 
        keystream = encrypt_block(previous, key)
        
        decrypted_block = xor_blocks(block, keystream[:len(block)]) 
        plaintext.append(decrypted_block) 
        previous = block 
    
    return b"".join(plaintext)

if __name__ == "__main__":
    # NOTE:(to self). From root, do python -m src.modes.cfb

    key = b"KeyYoisakiKanade"
    iv  = b"FEDCBA9876543210"

    plaintext = b"It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."

    print(f"Plaintext : {plaintext}")
    print(f"Key       : {key}")
    print(f"IV        : {iv}")
    print()

    ciphertext = encrypt_cfb(plaintext, key, iv)

    print(f"Ciphertext: {ciphertext}")

    decrypted = decrypt_cfb(ciphertext, key, iv)

    print(f"Decrypted : {decrypted}")
    
    print()
    if decrypted == plaintext:
        print("Alhamdulillah")
    else:
        print("Waduh")