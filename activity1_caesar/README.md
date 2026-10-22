# CNS Activity 1: Classical Substitution Cipher (Caesar Cipher)

**Course**: Cryptography and Network Security  
**Batch**: 2026_CNS_A_01  
**Course Outcome Mapping**: Activity 1 – CO1  
**Group Members**: Jayaditya Dev, Durgashree M, Aryaman Tiwari, Chirag T  

---

## 1. Introduction and Objective

The objective of this activity is to implement, test, and analyze the **Caesar Cipher**, one of the earliest known classical substitution ciphers. This implementation demonstrates:
- Mathematical encryption and decryption transformations.
- Shift key normalization handling arbitrary integer values (including negative shifts and shifts $\ge 26$).
- Preservation of character casing and non-alphabetic characters (spaces, punctuation, digits).
- Formal round-trip verification: $\mathcal{D}_k(\mathcal{E}_k(P)) = P$.
- Comprehensive cryptanalytic vulnerability assessment (Brute-force / Exhaustive Key Search and Frequency Analysis).

---

## 2. Theoretical Background and Working Principle

The Caesar Cipher is a **monoalphabetic substitution cipher** where each letter in the plaintext is shifted by a fixed integer number of positions $K$ down the Latin alphabet ($A$ through $Z$).

### 2.1 Mathematical Formulation

Let the English alphabet be mapped to integer residues modulo 26:
$$\mathbb{Z}_{26} = \{0, 1, 2, \dots, 25\}$$
where $A \mapsto 0, B \mapsto 1, \dots, Z \mapsto 25$.

#### Encryption
For a plaintext letter $P_i$ and a secret integer key $K$:
$$C_i = \mathcal{E}_K(P_i) = (P_i + K) \pmod{26}$$

#### Decryption
Given ciphertext letter $C_i$ and key $K$:
$$P_i = \mathcal{D}_K(C_i) = (C_i - K) \pmod{26}$$

Equivalently, decryption is encryption with the additive inverse shift:
$$\mathcal{D}_K(C) = \mathcal{E}_{-K \pmod{26}}(C)$$

### 2.2 Text and Key Handling Rules
1. **Case Preservation**: Uppercase letters $[A-Z]$ shift within $[A-Z]$; lowercase letters $[a-z]$ shift within $[a-z]$.
2. **Non-alphabetic Characters**: Punctuation, symbols, digits, and whitespace are preserved verbatim without translation.
3. **Key Normalization**: Any integer key $K \in \mathbb{Z}$ is normalized via:
   $$K_{\text{norm}} = K \pmod{26}$$
   In this implementation, Python's modulo operator natively handles negative shifts (e.g. $-3 \pmod{26} = 23$).

---

## 3. Algorithm and Pseudocode

### 3.1 Encryption Algorithm
```text
Algorithm CaesarEncrypt(plaintext, key):
    shift = key mod 26
    ciphertext = ""
    for each char in plaintext:
        if char is uppercase letter:
            ciphertext += chr((ord(char) - ord('A') + shift) mod 26 + ord('A'))
        else if char is lowercase letter:
            ciphertext += chr((ord(char) - ord('a') + shift) mod 26 + ord('a'))
        else:
            ciphertext += char
    return ciphertext
```

### 3.2 Decryption Algorithm
```text
Algorithm CaesarDecrypt(ciphertext, key):
    return CaesarEncrypt(ciphertext, -key)
```

---

## 4. Security Analysis, Advantages, and Limitations

### 4.1 Cryptanalytic Vulnerabilities

> [!WARNING]
> **Modern Security Warning**: The Caesar cipher is **completely insecure** for modern digital communication and offers zero cryptographic confidentiality.

1. **Exhaustive Key Search (Brute-Force Attack)**:
   - The keyspace size is bounded by the alphabet length: $|\mathcal{K}| = 26$.
   - A key of $0 \pmod{26}$ is the identity transformation (no encryption).
   - Thus, there are only **25 non-trivial keys**.
   - An adversary can compute and display all 25 candidate plaintexts in a few microseconds:
     $$\mathcal{O}(|\mathcal{K}| \cdot N) = 25 \cdot N \text{ operations}$$
     where $N$ is message length.

2. **Frequency Analysis (Statistical Cryptanalysis)**:
   - Monoalphabetic ciphers do not alter the underlying unigram frequency distribution of the natural language.
   - In standard English text, the letter **E** appears with approximately $12.7\%$ frequency, followed by **T** ($9.1\%$), **A** ($8.2\%$), and **O** ($7.5\%$).
   - An attacker counts letter frequencies in the ciphertext and aligns the highest frequency peak with 'E' to instantly determine $K$.

### 4.2 Advantages
- Conceptual simplicity: Easy to learn, demonstrate, and implement mentally.
- Negligible computational overhead: Requires minimal memory and CPU cycles ($\mathcal{O}(N)$ time, $\mathcal{O}(1)$ auxiliary space).
- Historical significance: Foundation for polyalphabetic systems (e.g., Vigenère cipher).

### 4.3 Limitations
- Tiny keyspace ($25$ active keys).
- Preserves letter frequency and punctuation structures.
- Vulnerable to ciphertext-only attack without known plaintext.

### 4.4 Applications
- **Historical**: Used by Julius Caesar circa 58 BC with a shift of $3$ ($D \leftarrow A$) to protect military communications against illiterate or non-Latin-literate adversaries.
- **Modern**: **ROT13** (Caesar shift $K=13$) is used in online discussion forums (Usenet, Reddit) to obscure movie spoilers, puzzle answers, and offensive humor from casual glance.

---

## 5. Execution Instructions

### Prerequisites
- Python 3.11+ installed or managed via `uv`.

### 5.1 Running the Automated Test Suite
From the repository root:
```bash
uv run pytest -v activity1_caesar/tests/test_caesar.py
```

### 5.2 Running the Command-Line Interface (CLI)

#### Command-line arguments:
```bash
uv run python activity1_caesar/cli.py --plaintext "Hello, World! 2026" --key 3
```
or using module syntax:
```bash
uv run python -m activity1_caesar.cli -p "Hello, World! 2026" -k 3
```

#### Interactive prompt:
Run without flags to be guided through inputs:
```bash
uv run python activity1_caesar/cli.py
```

#### Display algorithm and security analysis only:
```bash
uv run python activity1_caesar/cli.py --explanation-only
```

---

## 6. Sample Run

```text
$ uv run python activity1_caesar/cli.py -p "CNS Lab: Activity-01 (Caesar Cipher) @ 2026!" -k 3

================================================================================
           CNS ACTIVITY 1: CAESAR CIPHER DEMONSTRATION
================================================================================
Original Plaintext : CNS Lab: Activity-01 (Caesar Cipher) @ 2026!
Input Key          : 3 (Normalized shift: 3)
Encrypted Ciphertext: FQV Ode: Dfwlylwb-01 (Fdhvdu Flskhu) @ 2026!
Recovered Plaintext : CNS Lab: Activity-01 (Caesar Cipher) @ 2026!
--------------------------------------------------------------------------------
Round-Trip Verified: SUCCESS (Original == Recovered)

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
```

---

## 7. Automated Test Results Summary

| Test Identifier | Category | Input / Scenario | Expected Outcome | Actual Result |
| :--- | :--- | :--- | :--- | :--- |
| `test_normalize_key_standard` | Key normalization | Key = 3 | Normalized = 3 | PASS |
| `test_normalize_key_zero` | Boundary | Key = 0 | Normalized = 0 | PASS |
| `test_normalize_key_twenty_five` | Boundary | Key = 25 | Normalized = 25 | PASS |
| `test_normalize_key_greater_than_twenty_five`| Boundary / Modulo | Key = 26, 29 | Normalized = 0, 3 | PASS |
| `test_normalize_key_negative` | Negative Shift | Key = -1, -3 | Normalized = 25, 23 | PASS |
| `test_normalize_key_invalid_types` | Input Validation | String "3", Float 3.14, None, Bool True | Raises `TypeError` | PASS |
| `test_encrypt_known_answers` | Known Answer (KAT) | "HELLO" (k=3), ROT13 pangram (k=13) | Matches standard ciphertext | PASS |
| `test_encrypt_wrap_boundaries` | Alphabet Wrapping | "XYZ" (k=3) -> "ABC", "B" (k=25) -> "A" | Correct modular wrap | PASS |
| `test_encrypt_key_variations` | Equivalence | Key 0, 26, 29, -1 | Matches expected shifts | PASS |
| `test_encrypt_invalid_plaintext_type` | Input Validation | Integer 12345, None | Raises `TypeError` | PASS |
| `test_encrypt_empty_message` | Edge Case | Empty string `""` | Returns `""` | PASS |
| `test_encrypt_non_alphabetic_preservation` | Character Handling | Digits, punctuation, symbols | Verbatim preservation | PASS |
| `test_encrypt_repeated_characters` | Pattern Handling | "AAAA" (k=1) -> "BBBB", "...." -> "...." | Repeated outputs preserved | PASS |
| `test_decrypt_known_answers` | Decryption KAT | "KHOOR" (k=3) -> "HELLO" | Matches original | PASS |
| `test_round_trip_property` | Formal Invertibility | 10 varied inputs across pangrams and keys | `D(E(P)) == P` (100%) | PASS |
| `test_decrypt_invalid_types` | Input Validation | Non-string ciphertext, non-int key | Raises `TypeError` | PASS |
| `test_cli_run_demo` | Integration / CLI | Full demo workflow with explanation | Structured dict & round-trip OK | PASS |

**Total Tests**: 17  
**Passed**: 17  
**Failed**: 0  
**Test Suite Execution Time**: ~0.06s  
