import random
import math
from statistics import mean, pstdev

from src.modes.cbc import encrypt_cbc
from src.modes.cfb import encrypt_cfb
from src.modes.ctr import encrypt_ctr
from src.modes.ecb import encrypt_ecb
from src.modes.ofb import encrypt_ofb

KEY_NUMBER = 5
RANDOM_SEED = 24601
KEY_SIZE_BYTES = 16
BLOCK_SIZE_BYTES = 16
IV = b"FEDCBA9876543210"

PLAINTEXTS = []
with open("test/plaintexts.txt", "r", encoding="utf-8") as f:
    PLAINTEXTS = [line.rstrip("\r\n").encode("utf-8") for line in f]
PLAINTEXTS.append(b"ABCD"*1024)

ENCRYPT_FUNCTIONS = {
    "ecb": encrypt_ecb,
    "cbc": encrypt_cbc,
    "cfb": encrypt_cfb,
    "ofb": encrypt_ofb,
    "ctr": encrypt_ctr,
}

def generate_keys(n=KEY_NUMBER, seed=RANDOM_SEED):
    rng = random.Random(seed)
    return [rng.randbytes(KEY_SIZE_BYTES) for _ in range(n)]

def encrypt(plaintext, key, mode):
    encrypt_function = ENCRYPT_FUNCTIONS[mode]

    if mode == "ecb":
        return encrypt_function(plaintext, key)
    return encrypt_function(plaintext, key, IV)

def entropy(text: bytes) -> float:
    if not text: return 0.0

    frequency = {}
    for byte in text:
        frequency[byte] = frequency.get(byte, 0) + 1

    res = 0.0
    for count in frequency.values():
        probability = count / len(text)
        res -= probability * math.log2(probability)
    return res

if __name__ == "__main__":
    keys = generate_keys(n = len(PLAINTEXTS))

    entropies = {
        "ecb": [],
        "cbc": [],
        "cfb": [],
        "ofb": [],
        "ctr": [],
    }

    # Fix column length for each mode
    for i, plaintext in enumerate(PLAINTEXTS):
        key = keys[i]
        for mode in entropies.keys():
            ciphertext = encrypt(plaintext, key, mode)
            entropies[mode].append(entropy(ciphertext))

    print("=== Entropies ===")
    print(f"{'Plaintext':<30} | {'Key':<32} | {'Length (bytes)':<14} | {'ECB':<8} | {'CBC':<8} | {'CFB':<8} | {'OFB':<8} | {'CTR':<8} |")
    for i, plaintext in enumerate(PLAINTEXTS):
        key = keys[i]
        print(f"{str(plaintext)[:30]:<30} | {key.hex():<32} | {len(plaintext):<14} | {entropies['ecb'][i]:<8.4f} | {entropies['cbc'][i]:<8.4f} | {entropies['cfb'][i]:<8.4f} | {entropies['ofb'][i]:<8.4f} | {entropies['ctr'][i]:<8.4f} |")

    print()
    print(f"{'Statistic':<14} | {'ECB':<8} | {'CBC':<8} | {'CFB':<8} | {'OFB':<8} | {'CTR':<8} |")

    for label, statistic in [("Min", min), ("Max", max), ("Average", mean), ("Stddev", pstdev)]:
        values = " | ".join(f"{statistic(entropies[mode]):<8.4f}" for mode in entropies)
        print(f"{label:<14} | {values} |")
