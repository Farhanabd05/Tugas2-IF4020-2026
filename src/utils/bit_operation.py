def xor_blocks(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def add_bytes(a: bytes, b: bytes) -> bytes:
    return bytes((x + y) % 256 for x, y in zip(a, b))