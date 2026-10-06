from .tables import SBOX, PBOX

BLOCK_SIZE = 16
KEY_SIZE = 16
ROUNDS = 16
MASK64 = (1 << 64) - 1


def _rotl8(x: int, n: int) -> int:
    n &= 7
    return ((x << n) | (x >> (8 - n))) & 255 if n else x


def _rotl64(x: int, n: int) -> int:
    n &= 63
    return ((x << n) | (x >> (64 - n))) & MASK64 if n else x


def _permute64(value: int) -> int:
    result = 0
    for position, source in enumerate(PBOX):
        result |= ((value >> source) & 1) << position
    return result


def _round_keys(master_key: bytes) -> tuple[bytes, ...]:
    state = list(master_key)
    keys = []
    for r in range(ROUNDS):
        mixed = [
            SBOX[(state[i] + state[(i + 5) % 16] + r + i) & 255]
            for i in range(16)
        ]
        shifted = [_rotl8(mixed[(i + r + 1) % 16], (i + r) % 7 + 1)
                   for i in range(16)]
        keys.append(bytes((shifted[i] + shifted[i + 8]) & 255 for i in range(8)))
        state = [(shifted[i] + mixed[(i + 11) % 16] + 17 * r + i) & 255
                 for i in range(16)]
    return tuple(keys)


def _f(right: int, round_key: bytes, round_index: int) -> int:
    source = right.to_bytes(8, 'big')
    x = [SBOX[_rotl8((source[i] + round_key[i]) & 255, (i + round_index) % 7 + 1)]
         for i in range(8)]
    y = [x[i] ^ _rotl8(x[(i + 1) % 8], 1) ^ _rotl8(x[(i + 3) % 8], 3)
         for i in range(8)]
    value = _permute64(int.from_bytes(bytes(y), 'big'))
    return _rotl64(value, (round_index * 7 + 1) % 64)


def _validate(block: bytes, key: bytes) -> None:
    if not isinstance(block, bytes) or len(block) != BLOCK_SIZE:
        raise ValueError(f'Block must be exactly {BLOCK_SIZE} bytes')
    if not isinstance(key, bytes) or len(key) != KEY_SIZE:
        raise ValueError(f'Key must be exactly {KEY_SIZE} bytes')


def encrypt_block(block: bytes, key: bytes) -> bytes:
    _validate(block, key)
    left = int.from_bytes(block[:8], 'big')
    right = int.from_bytes(block[8:], 'big')
    for index, rk in enumerate(_round_keys(key)):
        left, right = right, left ^ _f(right, rk, index)
    return left.to_bytes(8, 'big') + right.to_bytes(8, 'big')


def decrypt_block(block: bytes, key: bytes) -> bytes:
    _validate(block, key)
    left = int.from_bytes(block[:8], 'big')
    right = int.from_bytes(block[8:], 'big')
    keys = _round_keys(key)
    for index in range(ROUNDS - 1, -1, -1):
        left, right = right ^ _f(left, keys[index], index), left
    return left.to_bytes(8, 'big') + right.to_bytes(8, 'big')
