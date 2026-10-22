"""One-Time Pad (OTP) Implementation.

Batch No: 2026_CNS_A_01
Activity 3: One-Time Pad (OTP)
"""

import secrets


def generate_key(length: int) -> bytes:
    """Generate cryptographically secure uniformly random bytes using secrets CSPRNG.
    
    Args:
        length: Non-negative integer number of bytes to generate.
        
    Returns:
        bytes of length `length`.
        
    Raises:
        TypeError: If length is not an integer or is a boolean.
        ValueError: If length is negative.
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError(f"Length must be an integer, got {type(length).__name__}")
    if length < 0:
        raise ValueError("Key length cannot be negative.")
    return secrets.token_bytes(length)


def xor_bytes(data: bytes | bytearray, key: bytes | bytearray) -> bytes:
    """Perform bytewise XOR between data and key of identical length.
    
    Args:
        data: Plaintext or ciphertext bytes.
        key: Cryptographically secure key bytes of identical length.
        
    Returns:
        Resulting bytes after XOR transformation.
        
    Raises:
        TypeError: If data or key is not bytes or bytearray.
        ValueError: If len(data) != len(key).
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"Data must be bytes, got {type(data).__name__}")
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError(f"Key must be bytes, got {type(key).__name__}")
    if len(data) != len(key):
        raise ValueError(
            f"Key length ({len(key)} bytes) must exactly match data length ({len(data)} bytes)."
        )
    return bytes(a ^ b for a, b in zip(data, key))


def encrypt(plaintext: str | bytes | bytearray, key: bytes | bytearray) -> bytes:
    """Encrypt a plaintext string or raw bytes using the One-Time Pad key.
    
    If plaintext is a string, it is encoded to UTF-8 bytes before XORing.
    
    Args:
        plaintext: The message as a UTF-8 string or raw bytes.
        key: Uniformly random key bytes of identical byte length.
        
    Returns:
        Ciphertext bytes.
        
    Raises:
        TypeError: If plaintext is not str/bytes/bytearray or key is not bytes/bytearray.
        ValueError: If len(data_bytes) != len(key).
    """
    if isinstance(plaintext, str):
        data_bytes = plaintext.encode("utf-8")
    elif isinstance(plaintext, (bytes, bytearray)):
        data_bytes = bytes(plaintext)
    else:
        raise TypeError(f"Plaintext must be str or bytes, got {type(plaintext).__name__}")
        
    return xor_bytes(data_bytes, key)


def decrypt(ciphertext: bytes | bytearray, key: bytes | bytearray) -> tuple[str | None, bytes]:
    """Decrypt ciphertext bytes using the One-Time Pad key.
    
    Attempts UTF-8 decoding on the recovered bytes. If decoding succeeds,
    returns (decoded_string, raw_bytes). If decoding fails (e.g. incorrect key),
    returns (None, raw_bytes).
    
    Args:
        ciphertext: The enciphered bytes.
        key: The key bytes of identical length.
        
    Returns:
        Tuple of (decoded_text_or_None, raw_decrypted_bytes).
        
    Raises:
        TypeError: If ciphertext or key is not bytes/bytearray.
        ValueError: If len(ciphertext) != len(key).
    """
    raw_decrypted = xor_bytes(ciphertext, key)
    try:
        decoded_text = raw_decrypted.decode("utf-8")
    except UnicodeDecodeError:
        decoded_text = None
    return decoded_text, raw_decrypted


