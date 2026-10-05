from ..utils.bit_operation import xor_blocks, add_bytes
from ..cipher.cipher import BLOCK_SIZE, encrypt_block, decrypt_block
from ..utils.padding import pkcs7_pad, pkcs7_unpad


def encrypt_ctr(plaintext: bytes, key: bytes, counter: bytes) -> bytes:
    if len(counter) != BLOCK_SIZE:
        raise ValueError(f"Counter must be exactly {BLOCK_SIZE} bytes")
    ciphertext = []
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)

    for i in range(0, len(plaintext), BLOCK_SIZE):
        encrypted_counter = encrypt_block(counter, key)
        block = plaintext[i : i + BLOCK_SIZE]
        ciphertext.append(xor_blocks(block, encrypted_counter))
        counter = add_bytes(counter, bytes([1] * BLOCK_SIZE))

    return b"".join(ciphertext)


def decrypt_ctr(ciphertext: bytes, key: bytes, counter: bytes) -> bytes:
    if len(counter) != BLOCK_SIZE:
        raise ValueError(f"Counter must be exactly {BLOCK_SIZE} bytes")
    plaintext = []

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        encrypted_counter = encrypt_block(counter, key)
        block = ciphertext[i : i + BLOCK_SIZE]
        plaintext.append(xor_blocks(block, encrypted_counter))
        counter = add_bytes(counter, bytes([1] * BLOCK_SIZE))

    return pkcs7_unpad(b"".join(plaintext), BLOCK_SIZE)


if __name__ == "__main__":
    key = b"KeyYoisakiKanade"
    counter = b"FEDCBA9876543210"

    plaintext = b"It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."

    print(f"Plaintext : {plaintext}")
    print(f"Key       : {key}")
    print(f"counter        : {counter}")
    print()

    ciphertext = encrypt_ctr(plaintext, key, counter)

    print(f"Ciphertext: {ciphertext}")

    decrypted = decrypt_ctr(ciphertext, key, counter)

    print(f"Decrypted : {decrypted}")

    print()
    if decrypted == plaintext:
        print("Alhamdulillah")
    else:
        print("Waduh")
