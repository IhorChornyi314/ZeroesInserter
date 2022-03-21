def read_int(bytes, pos, size):
    return int.from_bytes(bytes[pos: pos + size], 'little')


def read_string(bytes, pos, length=None):
    length = length if length is not None else bytes[pos:].find(b'\0') + 1
    return bytes[pos: pos + length].replace(b'\x00', b'').decode('utf8')
