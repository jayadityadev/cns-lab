# CNS Activity 2: Polyalphabetic Substitution Cipher (Vigenère Cipher)

**Course**: Cryptography and Network Security  
**Batch**: 2026_CNS_A_01  
**Course Outcome Mapping**: Activity 2 – CO4  
**Group Members**: Jayaditya Dev, Durgashree M, Aryaman Tiwari, Chirag T  

---

## 1. Introduction and Objective

The objective of this activity is to implement, test, and analyze the **Vigenère Cipher**, a foundational classical polyalphabetic substitution cipher. This activity demonstrates:
- The mathematical encryption and decryption transformations using a repeating keyword stream.
- The use of the classical **Tabula Recta** (Vigenère square).
- Key stream alignment conventions: the key advances strictly on alphabetic characters, ensuring punctuation and whitespace do not desynchronize the stream.
- Case and symbol preservation across encryption and decryption.
- Formal round-trip recovery: $\mathcal{D}_K(\mathcal{E}_K(P)) = P$.
- Comprehensive cryptanalytic vulnerability assessment explaining why the cipher is vulnerable to **Kasiski Examination** and **Friedman's Index of Coincidence**, rendering it completely unsuitable for modern secure communication.

---

## 2. Theoretical Background and Working Principle

### 2.1 From Monoalphabetic to Polyalphabetic Substitution

In a monoalphabetic cipher (such as Caesar), each letter in the plaintext always maps to the same ciphertext letter throughout the message. This makes it trivial to break via simple letter frequency analysis.

The **Vigenère Cipher** overcomes this limitation by employing **polyalphabetic substitution**. It cycles through multiple shift keys derived from a keyword, meaning that a single letter in the plaintext (e.g. `'E'`) can be enciphered into several different ciphertext letters depending on its position in the message.

### 2.2 Tabula Recta

Conceptually, the cipher operates using a $26 \times 26$ grid called the **Tabula Recta**, where:
- The row is indexed by the plaintext letter $P_i \in [A-Z]$.
- The column is indexed by the key letter $K_j \in [A-Z]$.
- Each row represents an alphabet shifted circularly by one additional position compared to the row above it.

### 2.3 Mathematical Formulation

Let the English alphabet be mapped to integer residues modulo 26:
$$\mathbb{Z}_{26} = \{0, 1, 2, \dots, 25\}, \quad A \mapsto 0, B \mapsto 1, \dots, Z \mapsto 25$$

Given a plaintext character $P_i$ and the corresponding key character $K_j$ from a keyword of length $L$:

#### Encryption
$$C_i = \mathcal{E}_K(P_i) = (P_i + K_j) \pmod{26}$$

#### Decryption
$$P_i = \mathcal{D}_K(C_i) = (C_i - K_j) \pmod{26}$$

### 2.4 Text and Key Handling Rules
1. **Key Stream Alignment**: The key index $j$ advances **only** when an alphabetic character ($A-Z$ or $a-z$) is processed. Spaces, punctuation, symbols, and numeric digits do NOT consume a key character or advance the key stream.
2. **Case Preservation**:
   - Uppercase letters shift within $[A-Z]$ relative to `'A'`.
   - Lowercase letters shift within $[a-z]$ relative to `'a'`.
3. **Non-Alphabetic Characters**: Digits, punctuation, whitespace, and special characters remain unmodified.
4. **Key Validation & Normalization**: The key must be a non-empty string consisting exclusively of ASCII alphabetic characters. It is normalized to uppercase for consistent shift calculations ($A=0 \dots Z=25$).

---

## 3. Algorithm and Pseudocode

### 3.1 Encryption Algorithm
```text
Algorithm VigenereEncrypt(plaintext, key):
    clean_key = ToUpperCase(key)
    L = Length(clean_key)
    key_idx = 0
    ciphertext = ""
    for each char in plaintext:
        if char is uppercase letter:
            shift = ord(clean_key[key_idx mod L]) - ord('A')
            ciphertext += chr((ord(char) - ord('A') + shift) mod 26 + ord('A'))
            key_idx += 1
        else if char is lowercase letter:
            shift = ord(clean_key[key_idx mod L]) - ord('A')
            ciphertext += chr((ord(char) - ord('a') + shift) mod 26 + ord('a'))
            key_idx += 1
        else:
            ciphertext += char
    return ciphertext
```

### 3.2 Decryption Algorithm
```text
Algorithm VigenereDecrypt(ciphertext, key):
    clean_key = ToUpperCase(key)
    L = Length(clean_key)
    key_idx = 0
    plaintext = ""
    for each char in ciphertext:
        if char is uppercase letter:
            shift = ord(clean_key[key_idx mod L]) - ord('A')
            plaintext += chr((ord(char) - ord('A') - shift) mod 26 + ord('A'))
            key_idx += 1
        else if char is lowercase letter:
            shift = ord(clean_key[key_idx mod L]) - ord('A')
            plaintext += chr((ord(char) - ord('a') - shift) mod 26 + ord('a'))
            key_idx += 1
        else:
            plaintext += char
    return plaintext
```

---

## 4. Security Analysis, Advantages, and Limitations

### 4.1 Cryptanalytic Vulnerabilities

> [!WARNING]
> **Modern Security Warning**: The Vigenère cipher is **completely insecure** for modern digital communication and offers zero computational secrecy against automated or manual cryptanalysis.

1. **Kasiski Examination (Determining Key Length $L$)**:
   - Because the key repeats periodically every $L$ characters, common n-grams (e.g. "THE", "ING", "AND") in the plaintext that happen to align with the same key positions will produce identical ciphertext sequences.
   - An attacker locates repeated sequences in the ciphertext, calculates the distances between occurrences, and finds their greatest common divisor (GCD). The GCD strongly indicates the key length $L$ or a multiple thereof.

2. **Index of Coincidence & Friedman Test**:
   - The Index of Coincidence ($I_c$) measures the probability that two randomly selected letters from a text are identical:
     $$I_c = \frac{\sum_{i=0}^{25} f_i (f_i - 1)}{N(N - 1)}$$
   - In natural English, $I_c \approx 0.067$. In purely random text (infinite polyalphabetic alphabet), $I_c \approx \frac{1}{26} \approx 0.0385$.
   - By calculating $I_c$ of the ciphertext or across candidate slice intervals, an attacker mathematically confirms the key length $L$.

3. **Caesar Decomposition**:
   - Once $L$ is determined, the ciphertext is partitioned into $L$ separate subsets:
     $$\text{Subset } m = \{C_m, C_{m+L}, C_{m+2L}, \dots\} \quad \text{for } m \in \{0, \dots, L-1\}$$
   - Each subset is an independent, monoalphabetic Caesar cipher!
   - Each subset can be solved independently in microseconds using standard frequency analysis on the letter 'E'.

### 4.2 Contrast with One-Time Pad (OTP)
- **Vigenère Cipher**: Reuses a short, human-memorable key periodically. Repeating the key introduces periodic correlation, breaking security.
- **One-Time Pad**: Uses a non-repeating key of truly random characters that is as long as the plaintext message and used only once. OTP provides **perfect (information-theoretic) secrecy** because every possible plaintext is equally likely.

### 4.3 Advantages
- Substantially more secure than monoalphabetic substitution ciphers (e.g. Caesar).
- Flattened unigram letter frequency distributions defeat naive letter-counting attacks.
- Simple to implement and demonstrate algorithmically.

### 4.4 Limitations
- Periodic key stream allows key-length deduction via Kasiski examination and Index of Coincidence.
- Zero computational resistance against modern cryptanalysis.
- Lacks message integrity, authentication, and replay protection.

### 4.5 Historical Applications
- Described in 1553 by Giovan Battista Bellaso and later misattributed to Blaise de Vigenère in the 19th century.
- Regarded as *"le chiffre indéchiffrable"* (the indecipherable cipher) for over 300 years until Charles Babbage (1854) and Friedrich Kasiski (1863) independently published general attacks.
- Used during the American Civil War by Confederate military forces using brass cipher disks.

---

## 5. Execution Instructions

### Prerequisites
- Python 3.11+ managed via `uv`.

### 5.1 Running the Automated Tests
From the repository root:
```bash
uv run pytest -v activity2_vigenere/tests/test_vigenere.py
```
Or run all laboratory tests across both activities:
```bash
uv run pytest -v
```

### 5.2 Running the Demonstration CLI

#### Command-line arguments:
```bash
uv run python activity2_vigenere/cli.py --plaintext "ATTACK AT DAWN!" --key "LEMON"
```
Or via module syntax:
```bash
uv run python -m activity2_vigenere.cli -p "ATTACK AT DAWN!" -k "LEMON"
```
Or via the root dispatcher:
```bash
uv run main.py activity2 -p "ATTACK AT DAWN!" -k "LEMON"
```

#### Interactive prompt:
Run without arguments to be guided through plaintext and key entry:
```bash
uv run python activity2_vigenere/cli.py
```

#### Display algorithm and security explanation only:
```bash
uv run python activity2_vigenere/cli.py --explanation-only
```

---

## 6. Sample Run

```text
$ uv run python activity2_vigenere/cli.py -p "The quick brown fox jumps over the lazy dog!" -k "LEMON"

================================================================================
           CNS ACTIVITY 2: VIGENERE CIPHER DEMONSTRATION
================================================================================
Original Plaintext : The quick brown fox jumps over the lazy dog!
Input Key          : LEMON (Normalized: LEMON)
Encrypted Ciphertext: Elq ehtgw pezaz tbi ngacd shse elq znkc pct!
Recovered Plaintext : The quick brown fox jumps over the lazy dog!
--------------------------------------------------------------------------------
Round-Trip Verified: SUCCESS (Original == Recovered)

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
```

---

## 7. Automated Test Results Summary

| Test Identifier | Category | Input / Scenario | Expected Outcome | Actual Result |
| :--- | :--- | :--- | :--- | :--- |
| `test_normalize_key_standard` | Normalization | Key `"LEMON"`, `"lemon"`, `"LeMoN"`, `"a"` | Normalized uppercase `[A-Z]` | PASS |
| `test_normalize_key_empty` | Key Validation | Empty string `""` | Raises `ValueError` | PASS |
| `test_normalize_key_non_alphabetic` | Key Validation | `"LEMON123"`, `"LE MON"`, `"LEMON!"` | Raises `ValueError` | PASS |
| `test_normalize_key_invalid_types` | Type Validation | Integer, `None`, `bool`, `list` | Raises `TypeError` | PASS |
| `test_encrypt_known_answers` | Known Answer (KAT) | `"ATTACKATDAWN"` with `"LEMON"`, `"CRYPTO"` with `"KEY"` | Standard historical vectors match | PASS |
| `test_encrypt_single_character_key` | Boundary / Caesar Equiv | Key `"D"` (shift 3) | Exactly equals Caesar shift 3 | PASS |
| `test_encrypt_key_longer_than_plaintext` | Boundary | Plaintext `"HELLO"` (len 5), key `"VERYLONGKEY"` (len 11) | Uses first 5 letters (`"CICJZ"`) | PASS |
| `test_encrypt_plaintext_longer_than_key` | Key Repetition | Plaintext `"AAAAAA"`, key `"ABC"` | Cyclic repetition (`"ABCABC"`) | PASS |
| `test_encrypt_invalid_plaintext_type` | Type Validation | Plaintext integer `12345`, `None` | Raises `TypeError` | PASS |
| `test_encrypt_case_and_punctuation_preservation` | Stream Advance Rule | `"Attack at DAWN!"` with key `"LEMON"` | Key advances only on letters; casing preserved | PASS |
| `test_encrypt_no_alphabetic_characters` | Edge Case | Only digits `"12345"`, symbols `"!@#$%"` | Output equals input verbatim | PASS |
| `test_encrypt_empty_plaintext` | Edge Case | Empty string `""` | Returns `""` | PASS |
| `test_encrypt_repeated_patterns` | Repetition | `"AAAA"` (k="B"), `"ABAB"` (k="AB") | Repeated patterns transformed correctly | PASS |
| `test_decrypt_known_answers` | Decryption KAT | `"LXFOPVEFRNHR"` with `"LEMON"` | Recovers `"ATTACKATDAWN"` | PASS |
| `test_round_trip_property` | Formal Invertibility | 8 varied test cases across pangrams and edge conditions | `D(E(P)) == P` (100%) | PASS |
| `test_decrypt_invalid_types` | Type Validation | Non-string ciphertext, empty key, invalid key type | Raises `TypeError` / `ValueError` | PASS |
| `test_cli_run_demo` | Integration / CLI | Full CLI workflow with explanation | Structured dict and explanation valid | PASS |

**Total Tests**: 17  
**Passed**: 17  
**Failed**: 0  
**Execution Time**: ~0.06s  
