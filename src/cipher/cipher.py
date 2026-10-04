BLOCK_SIZE = 16  # 128 bit TODO: ini dummy. tolong sesuaikan
KEY_SIZE = 16    # 128 bit TODO: ini dummy. tolong sesuaikan

#TODO: ini dummy
def encrypt_block(block: bytes, key: bytes) -> bytes:
    if len(block) != BLOCK_SIZE:
        raise ValueError(f"Block must be exactly {BLOCK_SIZE} bytes")

    if len(key) != KEY_SIZE:
        raise ValueError(f"Key must be exactly {BLOCK_SIZE} bytes")
    
    result = bytes(block[i] ^ key[i] for i in range(BLOCK_SIZE))

    return result

#TODO: ini dummy
def decrypt_block(block: bytes, key: bytes) -> bytes:
    if len(block) != BLOCK_SIZE:
        raise ValueError(f"Block must be exactly {BLOCK_SIZE} bytes")

    if len(key) != KEY_SIZE:
        raise ValueError(f"Key must be exactly {BLOCK_SIZE} bytes")
    
    result =  bytes(block[i] ^ key[i] for i in range(BLOCK_SIZE))

    return result


# TODO: untuk primitif operasi bisa di-add di file berbeda di folder ini. Atur atur :D