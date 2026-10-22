# CNS Activity 3: One-Time Pad (OTP)

**Course**: Cryptography and Network Security  
**Batch**: 2026_CNS_A_01  
**Course Outcome Mapping**: Activity 3 – CO3  
**Group Members**: Jayaditya Dev, Durgashree M, Aryaman Tiwari, Chirag T  

---

## 1. Introduction and Objective

The objective of this activity is to implement, test, and analyze the **One-Time Pad (OTP)** algorithm using cryptographically secure randomness, demonstrating:
- Key generation using a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG via Python's `secrets` module).
- Bytewise Exclusive-OR (XOR) encryption and decryption over UTF-8 message bytes.
- Exact key-length enforcement ($|K| == |M|$).
- The formal mathematical foundation of **Shannon's Perfect Secrecy**.
- The disastrous consequences of key reuse (**Two-Time Pad Attack**).
- The fundamental key-management limitations (distribution, storage, and synchronization) that make OTP impractical for general modern digital communication.

---

## 2. Theoretical Background and Working Principle

### 2.1 Mathematical Formulation of Bytewise XOR

Let the message $M$ be represented as a sequence of $L$ bytes:
$$M = (m_0, m_1, \dots, m_{L-1}), \quad m_i \in \{0, 1\}^8 = \mathbb{Z}_{256}$$

The key pad $K$ is an independent sequence of $L$ uniformly random bytes:
$$K = (k_0, k_1, \dots, k_{L-1}), \quad k_i \sim \mathcal{U}(\{0, 1\}^8)$$

#### Encryption
Each ciphertext byte $c_i$ is computed by the bitwise Exclusive-OR (addition modulo 2) of the message byte and key byte:
$$c_i = \mathcal{E}_K(m_i) = m_i \oplus k_i$$

#### Decryption
Decryption applies the identical XOR operation with the same key byte:
$$m'_i = \mathcal{D}_K(c_i) = c_i \oplus k_i = (m_i \oplus k_i) \oplus k_i$$

Because XOR is associative, commutative, and self-inverse ($x \oplus x = 0$ and $x \oplus 0 = x$):
$$m'_i = m_i \oplus (k_i \oplus k_i) = m_i \oplus 0 = m_i$$

The XOR operation acts as its own inverse, meaning no distinct mathematical algorithm is required for decryption.

### 2.2 Text and Key Handling Rules
1. **UTF-8 Byte Encoding**: Text messages are encoded to UTF-8 bytes before encryption. This natively preserves ASCII characters, whitespace, punctuation, digits, and multi-byte Unicode characters (e.g. accented characters, Asian glyphs, emojis).
2. **Exact Length Matching**: The key byte length must strictly equal the message byte length ($|K| = |M|$). Any discrepancy triggers an immediate `ValueError`.
3. **Decryption Robustness**: Decryption recovers the raw bytes and attempts UTF-8 decoding. Decryption with an incorrect key yields pseudo-random bytes which will fail UTF-8 decoding and are reported as raw bytes.

---

## 3. Shannon's Perfect Secrecy and Security Analysis

### 3.1 Information-Theoretic Perfect Secrecy

In 1949, Claude Shannon mathematically proved that the One-Time Pad provides **perfect secrecy** (information-theoretic or unconditional secrecy):

$$\mathbb{P}(M = m \mid C = c) = \mathbb{P}(M = m)$$

Or equivalently, the conditional Shannon entropy satisfies:
$$H(M \mid C) = H(M)$$

This means observing the ciphertext $c$ reveals **zero information** about the plaintext $m$, even to an adversary with infinite computational time and resources. For any candidate plaintext $m^*$ of length $L$, there exists a unique valid key $k^* = c \oplus m^*$ that would have produced the observed ciphertext $c$. Because all keys are equally likely under a uniform distribution ($\mathbb{P}(K=k^*) = 2^{-8L}$), every possible plaintext is equally likely.

### 3.2 The Five Mandatory Conditions for Perfect Secrecy

Perfect secrecy is a mathematical property of the overall protocol, NOT merely the XOR operator. All five of the following conditions must hold simultaneously:

1. **Uniform Randomness**: Every byte of the key must be chosen uniformly at random from $\{0, \dots, 255\}$, with zero bias and zero correlation.
2. **Key Length Equality**: The key must be at least as long as the message representation ($|K| \ge |M|$).
3. **Absolute Confidentiality**: The key must remain completely secret from all unauthorized parties.
4. **Strict Single Use**: The key pad must be used **strictly once** and immediately destroyed. It must never be reused or recycled.
5. **Secure Pre-Sharing**: Both communicating parties must securely exchange and synchronize the key pad prior to communication.

### 3.3 The Catastrophic Two-Time Pad Attack

If an identical key $K$ is reused to encrypt two separate messages $M_1$ and $M_2$:
$$C_1 = M_1 \oplus K$$
$$C_2 = M_2 \oplus K$$

An adversary intercepting both ciphertexts computes their XOR sum:
$$C_1 \oplus C_2 = (M_1 \oplus K) \oplus (M_2 \oplus K) = M_1 \oplus M_2$$

The key $K$ completely cancels out! The adversary now possesses $M_1 \oplus M_2$, which leaks massive statistical information and can be solved using **crib dragging** (sliding common words like " the ", " that ", " and " across the XOR difference to reveal readable words in both plaintexts).

### 3.4 Practical Key-Management Limitations

While mathematically unbreakable, the OTP is fundamentally impractical for modern digital infrastructure:
1. **Key Distribution Bottleneck**: Transmitting a key that is as large as the data requires an already secure channel of equal capacity. If a secure channel exists to transmit the key, the message itself could have been sent over that channel.
2. **Storage and Entropy Exhaustion**: Encrypting 1 Terabyte of data consumes 1 Terabyte of high-entropy key material that must be pre-generated, securely stored, and deleted.
3. **Synchronization Overhead**: Sender and receiver must remain in perfect byte synchronization. A dropped packet or offset desynchronizes all subsequent decryptions.
4. **Physical Destruction**: Used pad material must be securely erased (zeroized) or shredded to prevent retrospective decryption if storage is compromised.

---

## 4. Educational Demonstration vs. Real-World Key Management

> [!CAUTION]
> **Educational Notice**: This implementation displays the generated key and ciphertext in hexadecimal format for instructional demonstration. In an operational cryptographic deployment, printing or exposing the secret key to terminal output, logs, or monitors completely destroys confidentiality and invalidates all security guarantees.

---

## 5. Execution Instructions

### Prerequisites
- Python 3.11+ managed via `uv`.

### 5.1 Running the Automated Test Suite
From the repository root:
```bash
uv run pytest -v activity3_one_time_pad/tests/test_otp.py
```
Or run the complete test suite across all three activities:
```bash
uv run pytest -v
```

### 5.2 Running the Demonstration CLI

#### Automatic Random Key Generation:
```bash
uv run python activity3_one_time_pad/cli.py --plaintext "Top Secret CNS Dispatch 2026!"
```
Or via the root dispatcher:
```bash
uv run main.py activity3 -p "Top Secret CNS Dispatch 2026!"
```

#### Supplying a Custom Hex Key:
```bash
uv run python activity3_one_time_pad/cli.py -p "CNS 2026" -k aabbccddeeff1122
```

#### Demonstrating the Two-Time Pad Attack:
```bash
uv run python activity3_one_time_pad/cli.py --demo-key-reuse
```

#### Displaying Academic Theory Only:
```bash
uv run python activity3_one_time_pad/cli.py --explanation-only
```

---

## 6. Sample Runs

### 6.1 Standard Demonstration
```text
$ uv run python activity3_one_time_pad/cli.py -p "Top Secret CNS Dispatch 2026!"

================================================================================
           CNS ACTIVITY 3: ONE-TIME PAD (OTP) DEMONSTRATION
================================================================================
Original Plaintext     : Top Secret CNS Dispatch 2026!
Plaintext UTF-8 Bytes  : 29 bytes
Generated Random Key   : E86580E53B0282E2E62858888D930D880E95A1E5BF9CE82BA1A6494F3C (Length: 29 bytes)
Encrypted Ciphertext   : BCA4F0955B72E391854D2BEEECFC6CC96FBECCD6D3FDEE4BD2C3656E1D (Length: 29 bytes)
Recovered Plaintext    : Top Secret CNS Dispatch 2026!
--------------------------------------------------------------------------------
Round-Trip Verified    : SUCCESS (Original == Recovered)

[!] EDUCATIONAL NOTICE:
    Printing the secret key above is strictly for academic demonstration.
    In production cryptography, exposing the key on terminal output completely
    destroys confidentiality and violates the secrecy requirement.
```

### 6.2 Key Reuse Attack Demonstration
```text
$ uv run python activity3_one_time_pad/cli.py --demo-key-reuse

================================================================================
           DEMONSTRATION: CATASTROPHIC TWO-TIME PAD ATTACK
================================================================================
Plaintext 1 (M1)       : ATTACK AT DAWN!
Plaintext 2 (M2)       : DEFEND THE WALL
Shared Reused Key (Hex): 10FB4279D7D62311E26CD8393A0648
Ciphertext 1 (C1 Hex)  : 51AF1638949D0350B64C9C786D4869
Ciphertext 2 (C2 Hex)  : 54BE043C99920345AA29F86E7B4A04
--------------------------------------------------------------------------------
Adversary computes C1 ^ C2:
C1 ^ C2 (Hex)          : 051112040D0F00151C65641616026D
M1 ^ M2 (Hex)          : 051112040D0F00151C65641616026D
Key Canceled Out?      : YES (C1 ^ C2 == M1 ^ M2)

Conclusion: Reusing a One-Time Pad key destroys perfect secrecy entirely,
allowing an eavesdropper to recover the plaintext difference without knowing the key!
================================================================================
```

---

## 7. Automated Test Results Summary

| Test Identifier | Category | Input / Scenario | Expected Outcome | Actual Result |
| :--- | :--- | :--- | :--- | :--- |
| `test_generate_key_length` | Key Generation | Requests for 0, 10, 100 bytes | Returns exact requested byte length | PASS |
| `test_generate_key_independence` | CSPRNG Randomness | Two 32-byte key generation calls | Successive keys are distinct ($k_1 \ne k_2$) | PASS |
| `test_generate_key_invalid_length` | Validation | Negative length, float, string, `None`, `bool` | Raises `ValueError` / `TypeError` | PASS |
| `test_xor_bytes_known_vector` | Fixed KAT | Known test vector bytes | Exact expected XOR output | PASS |
| `test_xor_bytes_mathematical_properties` | Invertibility & Algebra | Invertibility, self-inverse, identity | $(A \oplus B) \oplus B = A$; $A \oplus A = 0$ | PASS |
| `test_xor_bytes_length_mismatch` | Length Enforcement | Key shorter or longer than data | Raises `ValueError` | PASS |
| `test_xor_bytes_invalid_types` | Type Validation | String, integer, `None` for data or key | Raises `TypeError` | PASS |
| `test_encrypt_decrypt_known_vector` | Deterministic KAT | `"CNS 2026"` with fixed hex key | Verified ciphertext and round-trip recovery | PASS |
| `test_encrypt_accepts_raw_bytes` | Interface Leverage | Arbitrary binary byte sequence | Preserves and recovers raw bytes | PASS |
| `test_encrypt_decrypt_random_key_round_trip` | Fuzzing Round-Trip | Sentences, pangrams, symbols | Perfect recovery across all samples | PASS |
| `test_encrypt_invalid_types` | Type Validation | Plaintext int `12345`, `None`, string key | Raises `TypeError` | PASS |
| `test_empty_message` | Edge Case | Empty string `""` | 0-byte key and 0-byte ciphertext round trip | PASS |
| `test_multibyte_utf8_characters` | Unicode / Multibyte | Accents, kanji, lock emoji 🔐 | Multi-byte expansion preserved | PASS |
| `test_decrypt_with_incorrect_key` | Security / Integrity | Decryption with wrong key | Fails recovery; returns raw random bytes | PASS |
| `test_two_time_pad_vulnerability` | Cryptanalysis | Reusing key across two messages | $C_1 \oplus C_2 == M_1 \oplus M_2$ verified | PASS |
| `test_cli_run_demo` | Integration / CLI | Full CLI workflow with explanation | Structured dict and explanation valid | PASS |
| `test_cli_demo_key_reuse` | Integration / CLI | Two-time pad demo routine | Executes cleanly without errors | PASS |

**Total Tests**: 17  
**Passed**: 17  
**Failed**: 0  
**Execution Time**: ~0.08s  
