import pytest
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from activity4_digital_signature.signature import (
    generate_key_pair,
    export_public_key_pem,
    get_public_key_fingerprint,
    sign_message,
    verify_signature,
)


def test_generate_key_pair_defaults():
    private_key, public_key = generate_key_pair()
    assert isinstance(private_key, RSAPrivateKey)
    assert isinstance(public_key, RSAPublicKey)
    assert private_key.key_size == 2048
    assert public_key.key_size == 2048
    assert public_key.public_numbers().e == 65537


def test_generate_key_pair_custom_size():
    # Fast test with 1024 bits for speed
    private_key, public_key = generate_key_pair(1024)
    assert private_key.key_size == 1024
    assert public_key.key_size == 1024


def test_generate_key_pair_invalid_size():
    with pytest.raises(ValueError):
        generate_key_pair(512)  # too small, insecure
    with pytest.raises(TypeError):
        generate_key_pair("2048")
    with pytest.raises(TypeError):
        generate_key_pair(None)


def test_export_public_key_pem():
    _, public_key = generate_key_pair(1024)
    pem = export_public_key_pem(public_key)
    assert isinstance(pem, str)
    assert pem.startswith("-----BEGIN PUBLIC KEY-----")
    assert pem.strip().endswith("-----END PUBLIC KEY-----")


def test_get_public_key_fingerprint():
    _, public_key = generate_key_pair(1024)
    fingerprint = get_public_key_fingerprint(public_key)
    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64  # SHA-256 hex digest length
    assert all(c in "0123456789abcdefABCDEF" for c in fingerprint)


def test_sign_and_verify_normal_message():
    private_key, public_key = generate_key_pair(1024)
    message = "Cryptography and Network Security 2026 - Digital Signature Test"
    
    signature = sign_message(message, private_key)
    assert isinstance(signature, bytes)
    assert len(signature) == 128  # 1024 / 8 bytes
    
    is_valid = verify_signature(message, signature, public_key)
    assert is_valid is True


def test_sign_accepts_raw_bytes():
    private_key, public_key = generate_key_pair(1024)
    raw_message = b"\x01\x02\x03\x04\xff\xfe"
    
    signature = sign_message(raw_message, private_key)
    assert verify_signature(raw_message, signature, public_key) is True


def test_sign_invalid_types():
    private_key, public_key = generate_key_pair(1024)
    with pytest.raises(TypeError):
        sign_message(12345, private_key)
    with pytest.raises(TypeError):
        sign_message("msg", public_key)  # public key cannot sign


def test_verification_failure_on_message_tampering():
    private_key, public_key = generate_key_pair(1024)
    original_message = "Transfer $1,000 to Bob"
    tampered_message = "Transfer $9,000 to Bob"
    
    signature = sign_message(original_message, private_key)
    
    # Original verifies
    assert verify_signature(original_message, signature, public_key) is True
    # Tampered message must fail verification
    assert verify_signature(tampered_message, signature, public_key) is False


def test_verification_failure_on_signature_tampering():
    private_key, public_key = generate_key_pair(1024)
    message = "Integrity critical command"
    
    signature = bytearray(sign_message(message, private_key))
    # Flip the first byte
    signature[0] ^= 0xFF
    
    assert verify_signature(message, bytes(signature), public_key) is False


def test_verification_failure_on_wrong_public_key():
    alice_priv, alice_pub = generate_key_pair(1024)
    _, bob_pub = generate_key_pair(1024)
    
    message = "Authentic dispatch from Alice"
    alice_sig = sign_message(message, alice_priv)
    
    # Alice's public key verifies Alice's signature
    assert verify_signature(message, alice_sig, alice_pub) is True
    # Bob's public key must reject Alice's signature
    assert verify_signature(message, alice_sig, bob_pub) is False


def test_verification_failure_on_malformed_signature():
    _, public_key = generate_key_pair(1024)
    message = "Valid message"
    
    # Too short / truncated signature
    assert verify_signature(message, b"short", public_key) is False
    # Non-bytes signature
    assert verify_signature(message, "invalid_string_sig", public_key) is False
    # Non-string non-bytes message
    assert verify_signature(12345, b"\x00" * 128, public_key) is False


def test_probabilistic_signature_pss_property():
    # In RSA-PSS, random salt ensures two signatures of the same message are distinct
    private_key, public_key = generate_key_pair(1024)
    message = "Deterministic message for probabilistic signature testing"
    
    sig1 = sign_message(message, private_key)
    sig2 = sign_message(message, private_key)
    
    # Bytes must not be identical due to randomized PSS salt
    assert sig1 != sig2
    # Both signatures must verify successfully
    assert verify_signature(message, sig1, public_key) is True
    assert verify_signature(message, sig2, public_key) is True


def test_empty_message_signing_and_verification():
    private_key, public_key = generate_key_pair(1024)
    empty_msg = ""
    
    sig = sign_message(empty_msg, private_key)
    assert verify_signature(empty_msg, sig, public_key) is True
    assert verify_signature("not empty", sig, public_key) is False


def test_multibyte_unicode_characters():
    private_key, public_key = generate_key_pair(1024)
    unicode_msg = "CNS Signature ✍️: Zürich & Tokyo 東京 2026!"
    
    sig = sign_message(unicode_msg, private_key)
    assert verify_signature(unicode_msg, sig, public_key) is True


def test_verify_signature_invalid_public_key():
    private_key, _ = generate_key_pair(1024)
    sig = sign_message("test", private_key)
    with pytest.raises(TypeError):
        verify_signature("test", sig, "not_a_public_key")
    with pytest.raises(TypeError):
        verify_signature("test", sig, private_key)  # private key cannot be used as public key


def test_cli_run_demo():
    from activity4_digital_signature.cli import run_demo, format_explanation

    result = run_demo("Academic CNS Signature 2026")
    assert result["message"] == "Academic CNS Signature 2026"
    assert result["is_valid"] is True
    assert result["key_size"] == 2048
    assert result["signature_bytes_len"] == 256
    assert len(result["fingerprint"]) == 64

    explanation = format_explanation()
    assert "SHA-256" in explanation
    assert "RSA-PSS" in explanation
    assert "Authenticity" in explanation
    assert "Integrity" in explanation
    assert "Non-Repudiation" in explanation


def test_cli_demo_tamper():
    from activity4_digital_signature.cli import demo_tamper
    
    # Ensures demo_tamper executes cleanly without exceptions
    demo_tamper()




