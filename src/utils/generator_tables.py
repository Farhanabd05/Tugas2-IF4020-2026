import hashlib
import random


def make_seed(seed_string):
    digest = hashlib.sha256(
        seed_string.encode("utf-8")
    ).digest()

    return int.from_bytes(
        digest,
        byteorder="big"
    )


def fisher_yates(values, seed_string):
    result = list(values)

    seed = make_seed(seed_string)
    rng = random.Random(seed)

    for i in range(len(result) - 1, 0, -1):
        j = rng.randint(0, i)

        result[i], result[j] = (
            result[j],
            result[i]
        )

    return result


SBOX = fisher_yates(
    range(256),
    "IF4020-Feistel-FisherYates-2026-v1:sbox"
)

PBOX = fisher_yates(
    range(64),
    "IF4020-Feistel-FisherYates-2026-v1:pbox"
)


print("SBOX = (")
for i in range(0, 256, 16):
    print("    " + ", ".join(
        str(x) for x in SBOX[i:i+16]
    ) + ",")
print(")")


print("\nPBOX = (")
for i in range(0, 64, 16):
    print("    " + ", ".join(
        str(x) for x in PBOX[i:i+16]
    ) + ",")
print(")")