"""Command Line Interface and Demonstration for Vigenère Cipher.

Batch No: 2026_CNS_A_01
Activity 2: Polyalphabetic Substitution Cipher (Vigenère Cipher)
"""

import argparse
import sys
from pathlib import Path

# Ensure repository root is in sys.path when invoked directly as a script
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from activity2_vigenere.vigenere import encrypt, decrypt, normalize_key


def format_explanation() -> str:
    """Return academic summary of the Vigenere cipher's principle and security."""
    return """
================================================================================
                    ALGORITHM PRINCIPLE & SECURITY ANALYSIS
================================================================================
1. Working Principle & Tabula Recta:
   - The Vigenere Cipher is a classical polyalphabetic substitution cipher.
   - It employs a sequence of Caesar shifts determined by the letters of a keyword.
   - Conceptually, it uses the "Tabula Recta" (a 26x26 grid where each row is the
     alphabet shifted by one additional position).
   - Mathematical Formulation:
       Let P_i be the i-th plaintext letter and K_j be the j-th key letter:
       * Encryption: C_i = (P_i + K_j) mod 26
       * Decryption: P_i = (C_i - K_j) mod 26
       where A = 0, B = 1, ..., Z = 25.
   - Text Handling Rules:
       * The key stream advances ONLY when an alphabetic character is enciphered.
       * Non-alphabetic characters (spaces, punctuation, digits) remain unshifted.
       * Character casing (uppercase / lowercase) is strictly preserved.

2. Security Aspects & Cryptanalysis:
   - Why it improved on Caesar:
       By cycling through multiple shift keys, a single plaintext letter (e.g. 'E')
       is enciphered into different ciphertext letters depending on its position,
       flattening simple unigram frequency spikes.
   - Why it is Broken (Vulnerabilities):
       a. Kasiski Examination:
          Because the key repeats every L characters, identical plaintext words
          separated by multiples of L yield identical ciphertext sequences. The greatest
          common divisor (GCD) of distances between repeating substrings reveals key length L.
       b. Index of Coincidence (Friedman Test):
          Measures the probability of two randomly selected letters being identical:
          I_c ~ 0.067 for single English text; I_c ~ 0.0385 for uniform random text.
          Allows direct estimation of key length L from ciphertext statistics.
       c. Caesar Decomposition:
          Once L is known, the ciphertext is partitioned into L independent sub-ciphers,
          each of which is a simple monoalphabetic Caesar cipher solvable instantly.
   - MODERN SECURITY WARNING:
       The classical Vigenere cipher provides NO computational security and is
       COMPLETELY INSECURE for modern digital communication.

3. Contrast with One-Time Pad (OTP):
   - A Vigenere cipher repeats a short, human-chosen keyword (periodic key stream).
   - A One-Time Pad uses a key that is truly random, never repeats, and is as long
     as the message itself, offering information-theoretic secrecy.

4. Advantages:
   - Masks simple monoalphabetic letter frequencies.
   - Keyspace grows exponentially with key length (26^L).
   - Historically known as "le chiffre indechiffrable" (the indecipherable cipher).

5. Limitations:
   - Periodic key repetition exposes key length via Kasiski examination.
   - Vulnerable to statistical frequency analysis once period L is determined.
   - Does not provide data integrity or authentication.

6. Historical Application:
   - Used extensively for diplomatic correspondence from the 16th century onward.
   - Employed by the Confederate Army during the American Civil War using brass cipher disks.
================================================================================
"""


def run_demo(plaintext: str, key: str) -> dict:
    """Execute encryption and decryption demonstration and display results."""
    clean_key = normalize_key(key)
    ciphertext = encrypt(plaintext, key)
    recovered = decrypt(ciphertext, key)

    print("\n" + "=" * 80)
    print("           CNS ACTIVITY 2: VIGENERE CIPHER DEMONSTRATION")
    print("=" * 80)
    print(f"Original Plaintext : {plaintext}")
    print(f"Input Key          : {key} (Normalized: {clean_key})")
    print(f"Encrypted Ciphertext: {ciphertext}")
    print(f"Recovered Plaintext : {recovered}")
    print("-" * 80)
    print(f"Round-Trip Verified: {'SUCCESS (Original == Recovered)' if plaintext == recovered else 'FAILED'}")
    print(format_explanation())

    return {
        "plaintext": plaintext,
        "key": key,
        "normalized_key": clean_key,
        "ciphertext": ciphertext,
        "recovered": recovered,
        "round_trip_success": (plaintext == recovered),
    }


def main():
    parser = argparse.ArgumentParser(
        description="CNS Activity 2: Vigenere Cipher Demonstration (Batch 2026_CNS_A_01)"
    )
    parser.add_argument(
        "-p", "--plaintext", type=str, help="Plaintext message to encipher"
    )
    parser.add_argument(
        "-k", "--key", type=str, help="Alphabetic encryption key (e.g. LEMON)"
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
                raw_key = input("Enter alphabetic key (e.g. LEMON): ").strip()
                normalize_key(raw_key)  # validate
                key = raw_key
                break
            except (ValueError, TypeError) as err:
                print(f"Error: {err} Please try again.")
            except (KeyboardInterrupt, EOFError):
                print("\nOperation cancelled.")
                sys.exit(1)

    run_demo(plaintext, key)


if __name__ == "__main__":
    main()
