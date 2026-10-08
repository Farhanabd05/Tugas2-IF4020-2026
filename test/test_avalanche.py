import random
from statistics import mean

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

MIN_PERCENT = 40
MAX_PERCENT = 60

PLAINTEXTS = [
    b"According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible.",
    b"I, Columbina Hyposelenia, lay aside my body. Let it be cast into the dark night, to illuminate the future. May it be a companion to all who dwell beneath the moon. Until the time comes for me to return home",
    b"Have you removed the dead body from the tree?",
    b"ABCD"*32,
    b"CIPHER"
]
KEY_TEST_PLAINTEXT = PLAINTEXTS[1]

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


def flip_bit(original, bit_position):
    modified = bytearray(original)
    modified[bit_position // 8] ^= 1 << (bit_position % 8)

    return bytes(modified)


def changed_bits(difference):
    return sum(byte.bit_count() for byte in difference)


def measure_difference(original, modified, mode, bit_position=None):
    if len(original) != len(modified):
        raise ValueError("Cannot compare outputs of different lengths")

    difference = bytes(a ^ b for a, b in zip(original, modified))
    region = difference
    propagation_matches = True

    if bit_position is not None:
        byte_position = bit_position // 8
        block_start = byte_position // BLOCK_SIZE_BYTES * BLOCK_SIZE_BYTES
        block_end = block_start + BLOCK_SIZE_BYTES

        expected = bytearray(len(difference))
        expected[byte_position] = 1 << (bit_position % 8)

        if mode in ("ofb", "ctr"):
            region = b""
            propagation_matches = difference == expected

        elif mode == "cfb":
            region = difference[block_end:]
            propagation_matches = difference[:block_end] == expected[:block_end]

        elif mode == "ecb":
            region = difference[block_start:block_end]
            propagation_matches = not any(difference[:block_start]) and not any(difference[block_end:])

        elif mode == "cbc":
            region = difference[block_start:]
            propagation_matches = not any(difference[:block_start])

    return {
        "output": difference,
        "diffusion": region,
        "propagation_matches": propagation_matches,
    }


def summarize_measurements(measurements):
    output_changes = sum(changed_bits(r["output"]) for r in measurements)
    output_bits = sum(len(r["output"]) * 8 for r in measurements)
    diffusion_changes = sum(changed_bits(r["diffusion"]) for r in measurements)
    diffusion_bits = sum(len(r["diffusion"]) * 8 for r in measurements)

    return {
        "output_percent": 100 * output_changes / output_bits,
        "diffusion_percent": 100 * diffusion_changes / diffusion_bits if diffusion_bits else None,
        "propagation_matches": all(r["propagation_matches"] for r in measurements),
    }


def plaintext_avalance_effect(plaintext, key, mode):
    original_ciphertext = encrypt(plaintext, key, mode)
    measurements = []

    for bit_position in range(len(plaintext) * 8):
        modified_plaintext = flip_bit(plaintext, bit_position)
        modified_ciphertext = encrypt(modified_plaintext, key, mode)

        measurements.append(measure_difference(original_ciphertext, modified_ciphertext, mode, bit_position))

    return summarize_measurements(measurements)


def key_avalanche_effect(plaintext, key, mode):
    original_ciphertext = encrypt(plaintext, key, mode)
    measurements = []

    for bit_position in range(len(key) * 8):
        modified_key = flip_bit(key, bit_position)
        modified_ciphertext = encrypt(plaintext, modified_key, mode)

        measurements.append(measure_difference(original_ciphertext, modified_ciphertext, mode))

    return summarize_measurements(measurements)


def failure_reason(result):
    reasons = []

    if not result["propagation_matches"]:
        reasons.append("unexpected bit propagation")

    percent = result["diffusion_percent"]

    if percent is not None and not MIN_PERCENT <= percent <= MAX_PERCENT:
        reasons.append(f"diffusion {percent:.2f}%")

    return ", ".join(reasons)


def print_header():
    print(f"{'Mode':<4}  {'Whole ciphertext %':>18}  {'Diffusion region %':>18}  {'Result':>6}")
    print("-" * 52)


def print_result(mode, results):
    output_percent = mean(r["output_percent"] for r in results)
    diffusion_percent = results[0]["diffusion_percent"]
    diffusion_display = "N/A"

    if diffusion_percent is not None:
        diffusion_percent = mean(r["diffusion_percent"] for r in results)
        diffusion_display = f"{diffusion_percent:.2f}%"

    failures = []

    for key_number, result in enumerate(results, 1):
        reason = failure_reason(result)

        if reason:
            failures.append(f"key {key_number}: {reason}")

    status = "FAIL" if failures else "PASS"
    details = "  " + "; ".join(failures) if failures else ""

    print(f"{mode.upper():<4}  {output_percent:>17.2f}%  {diffusion_display:>18}  {status:>6}{details}")

    return not failures


if __name__ == "__main__":
    keys = generate_keys()
    plaintext_test_key = keys[0]
    all_passed = True

    print("All bit positions are flipped separately.")
    print(f"Each key's average diffusion must be within {MIN_PERCENT}--{MAX_PERCENT}%.")

    print("\nPlaintext avalanche effect")
    print(f"Fixed random key: {plaintext_test_key.hex()}")

    for plaintext_number, plaintext in enumerate(PLAINTEXTS, 1):
        print(f"\nPlaintext {plaintext_number}: {len(plaintext)} bytes")
        print_header()

        for mode in ENCRYPT_FUNCTIONS:
            results = [plaintext_avalance_effect(plaintext, plaintext_test_key, mode)]

            passed = print_result(mode, results)
            all_passed = all_passed and passed

    print("\nKey avalanche effect")
    print(f"Average across {KEY_NUMBER} seeded random keys")
    print(f"Fixed plaintext: sample 2 ({len(KEY_TEST_PLAINTEXT)} bytes)")
    print_header()

    for mode in ENCRYPT_FUNCTIONS:
        results = [key_avalanche_effect(KEY_TEST_PLAINTEXT, key, mode) for key in keys]

        passed = print_result(mode, results)
        all_passed = all_passed and passed

    overall_status = "PASS" if all_passed else "FAIL"
    print(f"\nOverall: {overall_status}")
