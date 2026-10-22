"""Command Line Interface and Demonstration for Digital Signatures.

Batch No: 2026_CNS_A_01
Activity 4: Digital Signature Implementation (RSA-PSS with SHA-256)
"""

import argparse
import base64
import sys
from pathlib import Path

# Ensure repository root is in sys.path when invoked directly as a script
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Ensure stdout handles UTF-8 properly across diverse console environments
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from activity4_digital_signature.signature import (
    generate_key_pair,
    sign_message,
    verify_signature,
    get_public_key_fingerprint,
    export_public_key_pem,
)


def format_explanation() -> str:
    """Return academic summary of digital signatures, hashing, authenticity, and PKI."""
    return """
================================================================================
                    ALGORITHM PRINCIPLE & SECURITY ANALYSIS
================================================================================
1. Working Principle & The Three Cryptographic Roles:
   - Hashing (SHA-256):
       Arbitrary-length message M is compressed into a 256-bit fixed-size digest h.
       Hashing ensures efficiency (signing a 32-byte digest rather than megabytes
       of text) and cryptographic collision resistance.
   - Private-Key Signing:
       The signer uses their private key (d, n) with RSA-PSS padding to compute:
       S = (PSS(h))^d mod n
       Because d is strictly secret, only the legitimate owner can produce S.
   - Public-Key Verification:
       Any recipient or third party verifies S using the public key (e, n):
       Recovers PSS(h) from S^e mod n and checks that it matches SHA-256(M).
       Verification requires NO access to the secret private key.

2. Security Properties Provided:
   - Authenticity:
       Assures the receiver that the message was signed by the entity possessing
       the private key corresponding to the advertised public key.
   - Integrity:
       Guarantees that the message has not been altered, inserted, or corrupted
       in transit. Modifying even a single bit of M alters SHA-256(M) and fails verification.
   - Non-Repudiation:
       The signer cannot credibly deny creating the signature, provided the
       private key remained strictly confidential and uncompromised.

3. CRITICAL DISTINCTIONS:
   a. Digital Signatures vs. Encryption:
      * Encryption provides CONFIDENTIALITY (conceals message content).
      * Digital Signatures provide AUTHENTICITY and INTEGRITY (message is plaintext).
      * Signing a message DOES NOT encrypt or hide its contents!
   b. Key Possession vs. Real-World Identity:
      * A valid mathematical signature proves possession of the PRIVATE KEY.
      * It does NOT automatically prove a physical human or corporate identity.
      * Binding public keys to verified real-world identities requires Public Key
        Infrastructure (PKI), Digital Certificates (X.509), and Certificate Authorities (CAs).

4. Advantages of RSA-PSS over Legacy PKCS#1 v1.5:
   - Provably secure: RSA-PSS is proven secure in the Random Oracle Model.
   - Probabilistic: Employs randomized salt during padding, defeating chosen-message
     attacks and ensuring every signature is distinct even for identical messages.
================================================================================
"""


def run_demo(message: str) -> dict:
    """Execute digital signature generation and verification demonstration."""
    private_key, public_key = generate_key_pair(2048)
    fingerprint = get_public_key_fingerprint(public_key)
    signature = sign_message(message, private_key)
    is_valid = verify_signature(message, signature, public_key)

    sig_b64 = base64.b64encode(signature).decode("ascii")
    sig_hex = signature.hex().upper()

    print("\n" + "=" * 80)
    print("      CNS ACTIVITY 4: RSA-PSS DIGITAL SIGNATURE DEMONSTRATION")
    print("=" * 80)
    print(f"Message                : {message}")
    print(f"Hash Algorithm         : SHA-256")
    print(f"Signature Scheme       : RSA-PSS (MGF1 with SHA-256, salt=MAX_LENGTH)")
    print(f"Public Key Modulus     : 2048 bits (e = 65537)")
    print(f"Public Key Fingerprint : {fingerprint}")
    print(f"Signature (Base64)     : {sig_b64[:60]}... ({len(signature)} bytes)")
    print(f"Signature (Hex Sample) : {sig_hex[:64]}...")
    print("-" * 80)
    print(f"Verification Result    : {'VALID (Authenticity & Integrity Confirmed)' if is_valid else 'INVALID'}")
    print(format_explanation())

    return {
        "message": message,
        "key_size": 2048,
        "fingerprint": fingerprint,
        "signature_bytes_len": len(signature),
        "signature_b64": sig_b64,
        "is_valid": is_valid,
    }


def demo_tamper():
    """Demonstrate verification failures on message tampering, signature corruption, and wrong key."""
    private_key, public_key = generate_key_pair(2048)
    _, attacker_pub = generate_key_pair(2048)
    
    orig_msg = "Authorise payment of 5000 INR to Student Club."
    tampered_msg = "Authorise payment of 50000 INR to Student Club."
    
    signature = sign_message(orig_msg, private_key)
    corrupted_sig = bytearray(signature)
    corrupted_sig[10] ^= 0xAA  # flip bits in signature
    
    print("\n" + "=" * 80)
    print("      DEMONSTRATION: DIGITAL SIGNATURE INTEGRITY & TAMPER DETECTION")
    print("=" * 80)
    print(f"Original Message       : {orig_msg}")
    print(f"Tampered Message       : {tampered_msg}")
    print("-" * 80)
    
    # 1. Authentic Verification
    v1 = verify_signature(orig_msg, signature, public_key)
    print(f"1. Authentic Message + Original Signature : {'VALID [Passed]' if v1 else 'INVALID [Failed]'}")
    
    # 2. Tampered Message Verification
    v2 = verify_signature(tampered_msg, signature, public_key)
    print(f"2. Tampered Message + Original Signature  : {'VALID [Failed]' if v2 else 'INVALID [Tampering Detected!]'}")
    
    # 3. Corrupted Signature Verification
    v3 = verify_signature(orig_msg, bytes(corrupted_sig), public_key)
    print(f"3. Original Message + Corrupted Signature : {'VALID [Failed]' if v3 else 'INVALID [Corruption Detected!]'}")
    
    # 4. Wrong Public Key Verification
    v4 = verify_signature(orig_msg, signature, attacker_pub)
    print(f"4. Original Message + Unrelated Public Key: {'VALID [Failed]' if v4 else 'INVALID [Key Mismatch Detected!]'}")
    
    print("-" * 80)
    print("Conclusion: Any modification of the message, signature corruption, or key mismatch")
    print("immediately invalidates the digital signature, providing strict integrity assurance.")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="CNS Activity 4: Digital Signature Demonstration (Batch 2026_CNS_A_01)"
    )
    parser.add_argument(
        "-m", "--message", type=str, help="Message text to sign and verify"
    )
    parser.add_argument(
        "--demo-tamper", action="store_true", help="Demonstrate tamper detection and wrong-key rejection"
    )
    parser.add_argument(
        "--explanation-only", action="store_true", help="Display only academic explanation"
    )

    args = parser.parse_args()

    if args.explanation_only:
        print(format_explanation())
        return

    if args.demo_tamper:
        demo_tamper()
        return

    message = args.message
    if message is None:
        try:
            message = input("Enter message to digitally sign: ")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

    run_demo(message)


if __name__ == "__main__":
    main()
