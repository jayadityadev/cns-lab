"""Digital Signature Implementation using RSA-PSS and SHA-256.

Batch No: 2026_CNS_A_01
Activity 4: Digital Signature Implementation
"""

import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


def generate_key_pair(key_size: int = 2048) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA private and public key pair.
    
    Args:
        key_size: RSA modulus size in bits (default: 2048). Must be >= 1024.
        
    Returns:
        tuple of (private_key, public_key).
        
    Raises:
        TypeError: If key_size is not an integer.
        ValueError: If key_size < 1024.
    """
    if not isinstance(key_size, int) or isinstance(key_size, bool):
        raise TypeError(f"key_size must be an integer, got {type(key_size).__name__}")
    if key_size < 1024:
        raise ValueError(f"key_size must be at least 1024 bits for security, got {key_size}")
        
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    return private_key, private_key.public_key()


def export_public_key_pem(public_key: rsa.RSAPublicKey) -> str:
    """Export public key in standard PEM (SubjectPublicKeyInfo) format."""
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError(f"public_key must be RSAPublicKey, got {type(public_key).__name__}")
    pem_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem_bytes.decode("ascii")


def get_public_key_fingerprint(public_key: rsa.RSAPublicKey) -> str:
    """Compute the SHA-256 hex fingerprint of the public key's DER encoding."""
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError(f"public_key must be RSAPublicKey, got {type(public_key).__name__}")
    der_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return hashlib.sha256(der_bytes).hexdigest()


def sign_message(message: str | bytes | bytearray, private_key: rsa.RSAPrivateKey) -> bytes:
    """Sign a message using RSA-PSS with SHA-256 and maximum salt length.
    
    Args:
        message: Plaintext message as string or raw bytes.
        private_key: RSAPrivateKey instance.
        
    Returns:
        Digital signature as bytes.
        
    Raises:
        TypeError: If private_key is not RSAPrivateKey or message is not str/bytes.
    """
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError(f"private_key must be RSAPrivateKey, got {type(private_key).__name__}")
    if isinstance(message, str):
        data = message.encode("utf-8")
    elif isinstance(message, (bytes, bytearray)):
        data = bytes(message)
    else:
        raise TypeError(f"message must be str or bytes, got {type(message).__name__}")

    return private_key.sign(
        data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )


def verify_signature(
    message: str | bytes | bytearray,
    signature: bytes | bytearray,
    public_key: rsa.RSAPublicKey,
) -> bool:
    """Verify an RSA-PSS SHA-256 signature against a message using the public key.
    
    Args:
        message: Plaintext message as string or raw bytes.
        signature: The signature bytes to verify.
        public_key: RSAPublicKey instance.
        
    Returns:
        True if the signature is authentic and valid; False otherwise.
        
    Raises:
        TypeError: If public_key is not RSAPublicKey.
    """
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError(f"public_key must be RSAPublicKey, got {type(public_key).__name__}")
    if not isinstance(signature, (bytes, bytearray)):
        return False
    if isinstance(message, str):
        data = message.encode("utf-8")
    elif isinstance(message, (bytes, bytearray)):
        data = bytes(message)
    else:
        return False

    try:
        public_key.verify(
            bytes(signature),
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError):
        return False

