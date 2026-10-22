"""Command Line Interface and Demonstration for One-Time Pad (OTP).

Batch No: 2026_CNS_A_01
Activity 3: One-Time Pad (OTP)
"""

import argparse
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

from activity3_one_time_pad.otp import generate_key, encrypt, decrypt, xor_bytes



def format_explanation() -> str:
    """Return academic summary of the One-Time Pad, Shannon's theorem, and key management."""
    return """
================================================================================
                    ALGORITHM PRINCIPLE & SECURITY ANALYSIS
================================================================================
1. Working Principle & Mathematical Operation:
   - The One-Time Pad (OTP) represents the theoretical pinnacle of symmetric encryption.
   - Plaintext message M is represented as a sequence of bytes (e.g. UTF-8).
   - An equally-sized key K of uniformly random bytes is generated using a
     Cryptographically Secure Pseudo-Random Number Generator (CSPRNG).
   - Encryption & Decryption use bitwise / bytewise Exclusive-OR (XOR, denoted ^):
       * Encryption: C_i = M_i ^ K_i
       * Decryption: M'_i = C_i ^ K_i = (M_i ^ K_i) ^ K_i = M_i
   - XOR is its own mathematical inverse; no separate decryption inverse algorithm is required.

2. Shannon's Theorem & Perfect Secrecy:
   - In 1949, Claude Shannon proved that OTP provides INFORMATION-THEORETIC
     PERFECT SECRECY (unconditional secrecy):
       P(M = m | C = c) = P(M = m)
   - Observing the ciphertext provides ZERO statistical information to an adversary
     about the underlying message, regardless of infinite computing power or time.
   - Every possible plaintext of length L is equally likely to be the decryption
     under some valid key pad K in the keyspace.

3. Mandatory Conditions for Perfect Secrecy:
   To achieve perfect secrecy, ALL FIVE conditions must be strictly satisfied:
     1. The key must be genuinely, uniformly random (P(K=k) = 1 / 256^L).
     2. The key must be at least as long as the message being encrypted.
     3. The key must remain completely secret from all third parties.
     4. The key must be used STRICTLY ONCE (never reused or recycled).
     5. The communicating parties must securely exchange and protect the key pad.

4. Catastrophic Failure of Key Reuse (Two-Time Pad Attack):
   - If the same key K is used to encrypt two different messages M1 and M2:
       C1 = M1 ^ K
       C2 = M2 ^ K
   - An eavesdropper simply XORs the two ciphertexts together:
       C1 ^ C2 = (M1 ^ K) ^ (M2 ^ K) = M1 ^ M2
   - The key cancels out completely!
   - The XOR sum of two natural language texts can be readily decrypted using
     statistical letter frequencies and 'crib dragging' (testing common words).

5. Real-World Key-Management Limitations:
   - Key Distribution Bottleneck:
       Distributing a truly random key pad as large as the data securely requires
       an already secure channel (a physical courier or quantum key distribution).
   - Storage & Entropy Exhaustion:
       Encrypting 1 Terabyte of data requires 1 Terabyte of truly random key bytes.
   - Synchronization & Destruction:
       Both sender and receiver must track pad offsets; consumed pages must be
       physically destroyed to prevent retrospective compromise.

6. Historical Application:
   - The Washington-Moscow "Red Telephone" hotline teletype link (established 1963)
     used one-time tape pads delivered securely via diplomatic couriers.
================================================================================
"""


def run_demo(plaintext: str, key_bytes: bytes | None = None) -> dict:
    """Execute encryption and decryption demonstration and display results."""
    msg_bytes = plaintext.encode("utf-8")
    
    if key_bytes is None:
        key_bytes = generate_key(len(msg_bytes))
    elif len(key_bytes) != len(msg_bytes):
        raise ValueError(
            f"Key length ({len(key_bytes)} bytes) does not match message length ({len(msg_bytes)} bytes)."
        )

    ciphertext = encrypt(msg_bytes, key_bytes)
    decoded_text, recovered_bytes = decrypt(ciphertext, key_bytes)

    print("\n" + "=" * 80)
    print("           CNS ACTIVITY 3: ONE-TIME PAD (OTP) DEMONSTRATION")
    print("=" * 80)
    print(f"Original Plaintext     : {plaintext}")
    print(f"Plaintext UTF-8 Bytes  : {len(msg_bytes)} bytes")
    print(f"Generated Random Key   : {key_bytes.hex().upper()} (Length: {len(key_bytes)} bytes)")
    print(f"Encrypted Ciphertext   : {ciphertext.hex().upper()} (Length: {len(ciphertext)} bytes)")
    print(f"Recovered Plaintext    : {decoded_text if decoded_text is not None else recovered_bytes.hex()}")
    print("-" * 80)
    print(f"Round-Trip Verified    : {'SUCCESS (Original == Recovered)' if decoded_text == plaintext else 'FAILED'}")
    print("\n[!] EDUCATIONAL NOTICE:")
    print("    Printing the secret key above is strictly for academic demonstration.")
    print("    In production cryptography, exposing the key on terminal output completely")
    print("    destroys confidentiality and violates the secrecy requirement.")
    print(format_explanation())

    return {
        "plaintext": plaintext,
        "msg_bytes_len": len(msg_bytes),
        "key_hex": key_bytes.hex(),
        "ciphertext_hex": ciphertext.hex(),
        "recovered_text": decoded_text,
        "round_trip_success": (decoded_text == plaintext),
    }


def demo_key_reuse():
    """Demonstrate the catastrophic Two-Time Pad key reuse vulnerability."""
    m1 = "ATTACK AT DAWN!"
    m2 = "DEFEND THE WALL"
    b1 = m1.encode("utf-8")
    b2 = m2.encode("utf-8")
    
    shared_key = generate_key(len(b1))
    c1 = encrypt(b1, shared_key)
    c2 = encrypt(b2, shared_key)
    
    xor_ciphertexts = xor_bytes(c1, c2)
    xor_plaintexts = xor_bytes(b1, b2)
    
    print("\n" + "=" * 80)
    print("           DEMONSTRATION: CATASTROPHIC TWO-TIME PAD ATTACK")
    print("=" * 80)
    print(f"Plaintext 1 (M1)       : {m1}")
    print(f"Plaintext 2 (M2)       : {m2}")
    print(f"Shared Reused Key (Hex): {shared_key.hex().upper()}")
    print(f"Ciphertext 1 (C1 Hex)  : {c1.hex().upper()}")
    print(f"Ciphertext 2 (C2 Hex)  : {c2.hex().upper()}")
    print("-" * 80)
    print("Adversary computes C1 ^ C2:")
    print(f"C1 ^ C2 (Hex)          : {xor_ciphertexts.hex().upper()}")
    print(f"M1 ^ M2 (Hex)          : {xor_plaintexts.hex().upper()}")
    print(f"Key Canceled Out?      : {'YES (C1 ^ C2 == M1 ^ M2)' if xor_ciphertexts == xor_plaintexts else 'NO'}")
    print("\nConclusion: Reusing a One-Time Pad key destroys perfect secrecy entirely,")
    print("allowing an eavesdropper to recover the plaintext difference without knowing the key!")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="CNS Activity 3: One-Time Pad Demonstration (Batch 2026_CNS_A_01)"
    )
    parser.add_argument(
        "-p", "--plaintext", type=str, help="Plaintext message to encipher"
    )
    parser.add_argument(
        "-k", "--key-hex", type=str, help="Hexadecimal key bytes (optional; generated automatically if omitted)"
    )
    parser.add_argument(
        "--demo-key-reuse", action="store_true", help="Demonstrate the two-time pad key reuse attack"
    )
    parser.add_argument(
        "--explanation-only", action="store_true", help="Display only academic explanation"
    )

    args = parser.parse_args()

    if args.explanation_only:
        print(format_explanation())
        return

    if args.demo_key_reuse:
        demo_key_reuse()
        return

    plaintext = args.plaintext
    key_bytes = None

    if args.key_hex:
        try:
            key_bytes = bytes.fromhex(args.key_hex)
        except ValueError:
            print("Error: Invalid hexadecimal string supplied for --key-hex.")
            sys.exit(1)

    # Interactive prompt if arguments are omitted
    if plaintext is None:
        try:
            plaintext = input("Enter plaintext message: ")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

    try:
        run_demo(plaintext, key_bytes)
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
