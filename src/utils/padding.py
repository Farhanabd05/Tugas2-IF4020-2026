def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    padding_length = block_size - (len(data) % block_size)

    padding = bytes([padding_length]) * padding_length

    return data + padding

def pkcs7_unpad(data: bytes, block_size: int) -> bytes:
    if not data:
        raise ValueError("Cannot unpad empty data")

    padding_length = data[-1]

    if padding_length < 1 or padding_length > block_size:
        raise ValueError("Invalid padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid padding")

    return data[:-padding_length]