"""Command Line Interface and Demonstration for Caesar Cipher.

Batch No: 2026_CNS_A_01
Activity 1: Classical Substitution Cipher (Caesar Cipher)
"""

import argparse
import sys
from pathlib import Path

# Ensure repository root is in sys.path when invoked directly as a script
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from activity1_caesar.caesar import encrypt, decrypt, normalize_key



def format_explanation() -> str:
    """Return academic summary of the Caesar cipher's principle and security."""
    return """
================================================================================
                    ALGORITHM PRINCIPLE & SECURITY ANALYSIS
================================================================================
1. Working Principle:
   - The Caesar Cipher is a classical monoalphabetic substitution cipher.
   - Each plaintext letter is shifted down the alphabet by a fixed integer key K.
   - Mathematical Transformation:
       * Encryption: C_i = (P_i + K) mod 26
       * Decryption: P_i = (C_i - K) mod 26
   - Case of alphabetic characters is preserved; non-alphabetic characters
     (spaces, digits, punctuation) remain unshifted.

2. Security Aspects & Cryptanalysis:
   - Keyspace Size: |K| = 26 (only 25 non-trivial keys).
   - Vulnerability to Exhaustive Key Search (Brute Force):
       An attacker can test all 25 possible shifts in milliseconds.
   - Vulnerability to Frequency Analysis:
       Letter frequency distribution is preserved exactly, merely rotated.
       In English, 'E' is the most frequent letter (~12.7%), followed by 'T', 'A', 'O'.
       The shift is trivially discovered by aligning the peak frequency.
   - MODERN SECURITY WARNING:
       The Caesar Cipher provides NO computational security and is COMPLETELY INSECURE for modern communications.

3. Advantages:
   - Simple to understand, implement, and compute mentally.
   - Requires minimal computational resources.
   - Serves as an educational baseline for substitution ciphers.

4. Limitations:
   - Extremely small keyspace vulnerable to instant brute-force attack.
   - Preserves underlying language statistics and character patterns.
   - Easily broken with ciphertext-only attacks.

5. Applications:
   - Historical: Used by Julius Caesar (~58 BC) for military correspondence (shift of 3).
   - Modern: ROT13 (shift of 13) for basic spoiler hiding and text obfuscation in online forums.
================================================================================
"""


def run_demo(plaintext: str, key: int) -> dict:
    """Execute encryption and decryption demonstration and display results."""
    norm_key = normalize_key(key)
    ciphertext = encrypt(plaintext, key)
    recovered = decrypt(ciphertext, key)

    print("\n" + "=" * 80)
    print("           CNS ACTIVITY 1: CAESAR CIPHER DEMONSTRATION")
    print("=" * 80)
    print(f"Original Plaintext : {plaintext}")
    print(f"Input Key          : {key} (Normalized shift: {norm_key})")
    print(f"Encrypted Ciphertext: {ciphertext}")
    print(f"Recovered Plaintext : {recovered}")
    print("-" * 80)
    print(f"Round-Trip Verified: {'SUCCESS (Original == Recovered)' if plaintext == recovered else 'FAILED'}")
    print(format_explanation())

    return {
        "plaintext": plaintext,
        "key": key,
        "normalized_key": norm_key,
        "ciphertext": ciphertext,
        "recovered": recovered,
        "round_trip_success": (plaintext == recovered),
    }


def main():
    parser = argparse.ArgumentParser(
        description="CNS Activity 1: Caesar Cipher Demonstration (Batch 2026_CNS_A_01)"
    )
    parser.add_argument(
        "-p", "--plaintext", type=str, help="Plaintext message to encipher"
    )
    parser.add_argument(
        "-k", "--key", type=int, help="Integer shift key (e.g. 3)"
    )
    parser.add_argument(
        "--explanation-only", action="store_true", help="Display only academic explanation"
    )

    args = parser.parse_args()

    if args.explanation_only:
        print(format_explanation())
        return

    plaintext = args.plaintext
    key = args.key

    # Interactive fallback if arguments are omitted
    if plaintext is None:
        try:
            plaintext = input("Enter plaintext message: ")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

    if key is None:
        while True:
            try:
                raw_key = input("Enter integer shift key (e.g. 3): ").strip()
                key = int(raw_key)
                break
            except ValueError:
                print("Error: Key must be a valid integer. Please try again.")
            except (KeyboardInterrupt, EOFError):
                print("\nOperation cancelled.")
                sys.exit(1)

    run_demo(plaintext, key)


if __name__ == "__main__":
    main()
