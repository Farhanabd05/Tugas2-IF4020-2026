from collections import Counter
from pathlib import Path
import random
import matplotlib.pyplot as plt

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

OUTPUT_DIR = Path("test/histograms")
BYTE_VALUES = range(256)
UNIFORM_FREQUENCY = 100 / 256

PLAINTEXTS = []
with open("test/plaintexts.txt", "r", encoding="utf-8") as f:
    PLAINTEXTS = [line.rstrip("\r\n").encode("utf-8") for line in f]
PLAINTEXTS.extend([
    b"I, Columbina Hyposelenia, lay aside my body. Let it be cast into the dark night, to illuminate the future. May it be a companion to all who dwell beneath the moon. Until the time comes for me to return home",
    b"Have you removed the dead body from the tree?",
    b"ABCD" * 32,
    b"ABCD"*1024,
    b"CIPHER",
])

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


def byte_frequencies(data):
    counts = Counter(data)
    return [100 * counts[value] / len(data) if data else 0 for value in BYTE_VALUES]


def plot_histogram(axis, data, title, color):
    axis.bar(BYTE_VALUES, byte_frequencies(data), width=1, color=color)
    axis.axhline(UNIFORM_FREQUENCY, color="#d97706", linestyle="--", label="Uniform (0.3906%)")
    axis.set_title(f"{title} ({len(data)} bytes)")
    axis.set_xlabel("Byte value")
    axis.set_ylabel("Relative frequency (%)")
    axis.set_xlim(-0.5, 255.5)
    axis.set_xticks([0, 64, 128, 192, 255])
    axis.set_ylim(bottom=0)
    axis.legend(fontsize=8)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    keys = generate_keys(n=len(PLAINTEXTS))

    for number, (plaintext, key) in enumerate(zip(PLAINTEXTS, keys), 1):
        figure, axes = plt.subplots(3, 2, figsize=(13, 10), constrained_layout=True)
        axes = axes.flatten()
        figure.suptitle(f"Byte distributions - plaintext {number}\nKey: {key.hex()}")

        plot_histogram(axes[0], plaintext, "Plaintext", "#64748b")

        for axis, mode in zip(axes[1:], ENCRYPT_FUNCTIONS):
            ciphertext = encrypt(plaintext, key, mode)
            plot_histogram(axis, ciphertext, f"{mode.upper()} ciphertext", "#2563eb")

        ciphertext_limit = max(axis.get_ylim()[1] for axis in axes[1:])
        for axis in axes[1:]:
            axis.set_ylim(0, ciphertext_limit)

        output_file = OUTPUT_DIR / f"plaintext_{number:02d}.png"
        figure.savefig(output_file, dpi=150)

        plt.close(figure)
        print(f"Saved {output_file}")
