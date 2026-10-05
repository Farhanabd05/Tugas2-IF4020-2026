from ..modes.ctr import encrypt_ctr
from ..modes.cfb import encrypt_cfb
from ..modes.ofb import encrypt_ofb

def avalanche_effect(plaintext: bytes, key: bytes, iv: bytes, mode: str) -> None:
    if mode == "ctr":
        encrypt_func = encrypt_ctr
    elif mode == "cfb":
        encrypt_func = encrypt_cfb
    elif mode == "ofb":
        encrypt_func = encrypt_ofb
    else:
        raise ValueError("Mode tidak valid. Pilih 'ctr', 'cfb', atau 'ofb'.")
    ciphertext_original = encrypt_func(plaintext, key, iv)
    modified_plaintext = bytearray(plaintext) # ubah 1 bit awal dari plaintext
    modified_plaintext[0] ^= 0x01 
    ciphertext_modified = encrypt_func(bytes(modified_plaintext), key, iv)
    differing_bits = sum(bin(a ^ b).count("1") for a, b in zip(ciphertext_original, ciphertext_modified))

    print(f"Mode: {mode.upper()}")
    print(f"Jumlah bit yang berbeda antara ciphertext asli dan modifikasi: {differing_bits}")

if __name__ == "__main__":
    key = b"KeyYoisakiKanade"
    iv = b"FEDCBA9876543210"

    # test avalance effect for each mode
    plaintext = b"It's a beautiful day outside. Birds are singing, flowers are blooming... on days like these, kids like you... should be mengerjakan TA."
    for mode in ["ctr", "cfb", "ofb"]:
        avalanche_effect(plaintext, key, iv, mode)