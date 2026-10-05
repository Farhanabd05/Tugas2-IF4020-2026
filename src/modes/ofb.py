from ..cipher.cipher import BLOCK_SIZE, encrypt_block, decrypt_block
from ..utils.padding import pkcs7_pad, pkcs7_unpad
from ..utils.bit_operation import xor_blocks

def encrypt_ofb(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"iv must be exactly {BLOCK_SIZE} bytes")

    padded_text = pkcs7_pad(plaintext, BLOCK_SIZE)
    ciphertext = []
    current_feedback = iv
    for i in range(0, len(padded_text), BLOCK_SIZE):
        block = padded_text[i:i+BLOCK_SIZE]
        keystream_block = encrypt_block(current_feedback, key)
        cipher_block = xor_blocks(block, keystream_block)
        ciphertext.append(cipher_block)
        current_feedback = keystream_block
    return b"".join(ciphertext)

def decrypt_ofb(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"iv must be exactly {BLOCK_SIZE} bytes")
    padded_plaintext = []
    current_feedback = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        keystream_block = encrypt_block(current_feedback, key)
        plain_block = xor_blocks(block, keystream_block)
        padded_plaintext.append(plain_block)
        current_feedback = keystream_block
    return pkcs7_unpad(b"".join(padded_plaintext), BLOCK_SIZE)

if __name__ == "__main__":
    key = b"KeyYoisakiKanade"
    iv = b"FEDCBA9876543210"

    plaintext = b"It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."

    print(f"Plaintext : {plaintext}")
    print(f"Key       : {key}")
    print(f"IV        : {iv}")
    print()

    ciphertext = encrypt_ofb(plaintext, key, iv)

    print(f"Ciphertext: {ciphertext}")

    decrypted = decrypt_ofb(ciphertext, key, iv)

    print(f"Decrypted : {decrypted}")

    print()
    if decrypted == plaintext:
        print("Alhamdulillah")
    else:
        print("Waduh")
