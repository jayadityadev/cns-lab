"""One-Time Pad (OTP) Encryption Module."""
from .otp import generate_key, xor_bytes, encrypt, decrypt

__all__ = ["generate_key", "xor_bytes", "encrypt", "decrypt"]
