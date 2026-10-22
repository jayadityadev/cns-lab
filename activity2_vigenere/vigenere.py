"""Vigenère Cipher implementation.

Batch No: 2026_CNS_A_01
Activity 2: Polyalphabetic Substitution Cipher (Vigenère Cipher)
"""


def normalize_key(key: str) -> str:
    """Validate and normalize a Vigenère cipher key to uppercase [A-Z].
    
    Args:
        key: A string of alphabetic characters.
        
    Returns:
        Uppercase string containing only ASCII alphabetic characters.
        
    Raises:
        TypeError: If key is not a string.
        ValueError: If key is empty or contains non-alphabetic characters.
    """
    if not isinstance(key, str):
        raise TypeError(f"Key must be a string, got {type(key).__name__}")
    if not key:
        raise ValueError("Key must be a non-empty string.")
    if not key.isalpha() or not key.isascii():
        raise ValueError("Key must contain only ASCII alphabetic characters (A-Z, a-z).")
    return key.upper()


def encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext using the polyalphabetic Vigenère cipher.
    
    The key advances only when an alphabetic character is enciphered.
    Preserves character case and non-alphabetic characters.
    
    Args:
        plaintext: The message string to encrypt.
        key: The non-empty alphabetic key string.
        
    Returns:
        The encrypted ciphertext string.
        
    Raises:
        TypeError: If plaintext is not a string or key is not a string.
        ValueError: If key is invalid.
    """
    if not isinstance(plaintext, str):
        raise TypeError(f"Plaintext must be a string, got {type(plaintext).__name__}")
    
    clean_key = normalize_key(key)
    key_len = len(clean_key)
    key_idx = 0
    ciphertext = []
    
    for ch in plaintext:
        if 'a' <= ch <= 'z':
            shift = ord(clean_key[key_idx % key_len]) - ord('A')
            ciphertext.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            key_idx += 1
        elif 'A' <= ch <= 'Z':
            shift = ord(clean_key[key_idx % key_len]) - ord('A')
            ciphertext.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            key_idx += 1
        else:
            ciphertext.append(ch)
            
    return "".join(ciphertext)


def decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using the polyalphabetic Vigenère cipher.
    
    The key advances only when an alphabetic character is deciphered.
    Preserves character case and non-alphabetic characters.
    
    Args:
        ciphertext: The enciphered message string to decrypt.
        key: The non-empty alphabetic key string.
        
    Returns:
        The decrypted plaintext string.
        
    Raises:
        TypeError: If ciphertext is not a string or key is not a string.
        ValueError: If key is invalid.
    """
    if not isinstance(ciphertext, str):
        raise TypeError(f"Ciphertext must be a string, got {type(ciphertext).__name__}")
    
    clean_key = normalize_key(key)
    key_len = len(clean_key)
    key_idx = 0
    plaintext = []
    
    for ch in ciphertext:
        if 'a' <= ch <= 'z':
            shift = ord(clean_key[key_idx % key_len]) - ord('A')
            plaintext.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
            key_idx += 1
        elif 'A' <= ch <= 'Z':
            shift = ord(clean_key[key_idx % key_len]) - ord('A')
            plaintext.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
            key_idx += 1
        else:
            plaintext.append(ch)
            
    return "".join(plaintext)


