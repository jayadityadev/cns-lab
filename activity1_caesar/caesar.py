"""Caesar Cipher implementation."""


def normalize_key(key: int) -> int:
    """Normalize an integer key into the range [0, 25] via modulo 26.
    
    Raises:
        TypeError: If key is not an integer or is a boolean.
    """
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError(f"Key must be an integer, got {type(key).__name__}")
    return key % 26


def encrypt(plaintext: str, key: int) -> str:
    """Encrypt a plaintext string using the Caesar cipher with the given shift key.
    
    Preserves character case and non-alphabetic characters.
    
    Raises:
        TypeError: If plaintext is not a string or key is not an integer.
    """
    if not isinstance(plaintext, str):
        raise TypeError(f"Plaintext must be a string, got {type(plaintext).__name__}")
    
    shift = normalize_key(key)
    result = []
    for char in plaintext:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(char)
    return "".join(result)


def decrypt(ciphertext: str, key: int) -> str:
    """Decrypt a ciphertext string using the Caesar cipher with the given shift key.
    
    Inverse of encrypt: defined as encrypt(ciphertext, -key).
    
    Raises:
        TypeError: If ciphertext is not a string or key is not an integer.
    """
    if not isinstance(ciphertext, str):
        raise TypeError(f"Ciphertext must be a string, got {type(ciphertext).__name__}")
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError(f"Key must be an integer, got {type(key).__name__}")
    return encrypt(ciphertext, -key)


