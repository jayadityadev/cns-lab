# CNS Activity 4: Digital Signature Implementation (RSA-PSS with SHA-256)

**Course**: Cryptography and Network Security  
**Batch**: 2026_CNS_A_01  
**Course Outcome Mapping**: Activity 4 – CO3  
**Group Members**: Jayaditya Dev, Durgashree M, Aryaman Tiwari, Chirag T  

---

## 1. Introduction and Objective

The objective of this activity is to implement, test, and analyze an industry-grade **Digital Signature** system using asymmetric cryptography. Utilizing the reputable Python `cryptography` library, this implementation demonstrates:
- 2048-bit RSA key pair generation with public exponent $e = 65537$.
- Message signing using **RSA-PSS** (Probabilistic Signature Scheme, RFC 8017 / PKCS#1 v2.1) combined with **SHA-256** hashing and Mask Generation Function 1 (MGF1).
- Public-key signature verification with clean boolean status and tampering detection.
- Public key fingerprinting (SHA-256 digest of SubjectPublicKeyInfo DER).
- Mathematical explanations of the roles of hashing, private-key signing, and public-key verification.
- Comprehensive security analysis explaining **authenticity**, **integrity**, and **non-repudiation**.
- Critical clarification of the distinction between digital signatures and encryption, and the necessity of Public Key Infrastructure (PKI) for real-world identity binding.

---

## 2. Theoretical Background and Working Principle

A digital signature is the asymmetric cryptographic analog of a handwritten signature, but with vastly superior mathematical security: it is unforgeable, message-dependent, and publicly verifiable.

### 2.1 The Three Cryptographic Roles

```
[Plaintext M] ---> [SHA-256 Hash] ---> [Digest h] ---> [RSA Private Key d] ---> [Signature S]
                                                                                      |
[Plaintext M] ---> [SHA-256 Hash] ---> [Digest h']                                    |
                                              \                                      /
                                           [Verify Equality: h' == PSS_Verify(S, e)]
```

1. **Role of Cryptographic Hashing (SHA-256)**:
   - Arbitrary-length message $M$ is mapped to a fixed-size 256-bit digest $h = \text{SHA-256}(M)$.
   - **Efficiency**: Signing a 32-byte hash requires a single modular exponentiation, regardless of whether $M$ is a 10-word text or a 10-Gigabyte file.
   - **Collision Resistance**: Computationally infeasible to find two distinct messages $M_1 \ne M_2$ such that $\text{SHA-256}(M_1) = \text{SHA-256}(M_2)$.
2. **Role of Private-Key Signing**:
   - The signer applies their secret private exponent $d$ to the padded message digest:
     $$S = \mu^d \pmod n, \quad \text{where } \mu = \text{PSS-Encode}(h, \text{salt})$$
   - Because $d$ is kept strictly secret by the signer, only the legitimate owner can produce a valid signature $S$.
3. **Role of Public-Key Verification**:
   - Any verifier holding the public key $(e, n)$ recovers the encoded digest:
     $$\mu' = S^e \pmod n$$
   - The verifier validates the PSS padding format, extracts the salt, and confirms that the message hash matches $h' = \text{SHA-256}(M)$.
   - Verification requires **zero access** to the private key.

### 2.2 Why RSA-PSS instead of Legacy PKCS#1 v1.5?

- **RSA-PSS (RFC 8017)** is provably secure in the Random Oracle Model, meaning its security reduction to the RSA problem is tight.
- **Probabilistic Property**: PSS incorporates a cryptographically random salt (up to maximum salt length) into each signature. Therefore, signing the exact same message multiple times produces distinct signature byte sequences, preventing chosen-message and deterministic signature attacks while all verifying successfully.

---

## 3. Security Analysis, Distinctions, and Real-World Limitations

### 3.1 Security Properties Provided

1. **Authenticity**: Assures the verifier that the message was signed by the specific private key corresponding to the public key.
2. **Integrity**: Guarantees that the message has not been altered, inserted, or modified in transit. Changing even a single bit of $M$ completely changes $\text{SHA-256}(M)$, causing verification to fail.
3. **Non-Repudiation**: The signer cannot credibly deny creating the signature, provided the private key remained secure and uncompromised.

### 3.2 Critical Security Distinctions

> [!IMPORTANT]
> **Digital Signatures vs. Encryption**:
> - **Encryption** provides **confidentiality** (conceals the plaintext so unauthorized parties cannot read it).
> - **Digital Signatures** provide **authenticity and integrity** (the message is in plaintext; anyone can read it).
> - Signing a message does NOT encrypt or hide its contents! For confidentiality, hybrid encryption (e.g. AES-GCM + RSA-OAEP) must be combined with digital signatures.

> [!WARNING]
> **Key Possession vs. Real-World Identity**:
> - Mathematically, a digital signature proves only that the entity holding the private key generated the signature.
> - A signature does NOT automatically prove a physical person's or organization's identity unless that public key is bound to an identity through **Public Key Infrastructure (PKI)**, **X.509 Digital Certificates**, and trusted **Certificate Authorities (CAs)**.

### 3.3 Private Key Protection Best Practices
- Private keys must never be hard-coded into source code or committed to version control.
- In production, private keys should reside inside Hardware Security Modules (HSMs) or secure enclaves with access auditing.

---

## 4. Execution Instructions

### Prerequisites
- Python 3.11+ managed via `uv` with `cryptography` installed.

### 4.1 Running the Automated Test Suite
From the repository root:
```bash
uv run pytest -v activity4_digital_signature/tests/test_signature.py
```
Or run all 69 laboratory tests across all four activities:
```bash
uv run pytest -v
```

### 4.2 Running the Demonstration CLI

#### Signing and Verifying a Message:
```bash
uv run python activity4_digital_signature/cli.py --message "Confidential Academic Dispatch 2026"
```
Or via the root dispatcher:
```bash
uv run main.py activity4 -m "Confidential Academic Dispatch 2026"
```

#### Demonstrating Tamper Detection & Wrong-Key Rejection:
```bash
uv run python activity4_digital_signature/cli.py --demo-tamper
```

#### Displaying Academic Explanation Only:
```bash
uv run python activity4_digital_signature/cli.py --explanation-only
```

---

## 5. Sample Runs

### 5.1 Standard Digital Signature Execution
```text
$ uv run python activity4_digital_signature/cli.py -m "Academic CNS Signature 2026"

================================================================================
      CNS ACTIVITY 4: RSA-PSS DIGITAL SIGNATURE DEMONSTRATION
================================================================================
Message                : Academic CNS Signature 2026
Hash Algorithm         : SHA-256
Signature Scheme       : RSA-PSS (MGF1 with SHA-256, salt=MAX_LENGTH)
Public Key Modulus     : 2048 bits (e = 65537)
Public Key Fingerprint : 2df6f78e411b7b05537f5b4f8d672ea4e64f02888cf91054324f686ca98f5a54
Signature (Base64)     : T53o9rVlB0mR6q+4bC307eY5qKjP... (256 bytes)
Signature (Hex Sample) : 4F9DE8F6B565...
--------------------------------------------------------------------------------
Verification Result    : VALID (Authenticity & Integrity Confirmed)
```

### 5.2 Tamper and Fraud Detection Demonstration
```text
$ uv run python activity4_digital_signature/cli.py --demo-tamper

================================================================================
      DEMONSTRATION: DIGITAL SIGNATURE INTEGRITY & TAMPER DETECTION
================================================================================
Original Message       : Authorise payment of 5000 INR to Student Club.
Tampered Message       : Authorise payment of 50000 INR to Student Club.
--------------------------------------------------------------------------------
1. Authentic Message + Original Signature : VALID [Passed]
2. Tampered Message + Original Signature  : INVALID [Tampering Detected!]
3. Original Message + Corrupted Signature : INVALID [Corruption Detected!]
4. Original Message + Unrelated Public Key: INVALID [Key Mismatch Detected!]
--------------------------------------------------------------------------------
Conclusion: Any modification of the message, signature corruption, or key mismatch
immediately invalidates the digital signature, providing strict integrity assurance.
================================================================================
```

---

## 6. Automated Test Results Summary

| Test Identifier | Category | Input / Scenario | Expected Outcome | Actual Result |
| :--- | :--- | :--- | :--- | :--- |
| `test_generate_key_pair_defaults` | Key Generation | Default 2048-bit RSA generation | Returns RSAPrivateKey & RSAPublicKey ($e=65537$) | PASS |
| `test_generate_key_pair_custom_size` | Custom Keys | 1024-bit generation | Key size matches 1024 | PASS |
| `test_generate_key_pair_invalid_size` | Key Validation | Sub-1024 bits, string, `None` | Raises `ValueError` / `TypeError` | PASS |
| `test_export_public_key_pem` | Serialization | Public key export | Valid SubjectPublicKeyInfo PEM string | PASS |
| `test_get_public_key_fingerprint` | Identification | Public key fingerprinting | 64-character SHA-256 hex digest | PASS |
| `test_sign_and_verify_normal_message` | Functional Seam | Standard message text | 256-byte signature verifies as `True` | PASS |
| `test_sign_accepts_raw_bytes` | Interface Flexibility | Raw binary byte message | Verifies as `True` | PASS |
| `test_sign_invalid_types` | Type Validation | Integer message, public key signing | Raises `TypeError` | PASS |
| `test_verification_failure_on_message_tampering` | Integrity | Modified message content | Verification returns `False` | PASS |
| `test_verification_failure_on_signature_tampering` | Integrity | Flipped bit in signature | Verification returns `False` | PASS |
| `test_verification_failure_on_wrong_public_key` | Authenticity | Independent public key | Verification returns `False` | PASS |
| `test_verification_failure_on_malformed_signature` | Robustness | Truncated bytes, string, non-bytes | Returns `False` safely without crashing | PASS |
| `test_probabilistic_signature_pss_property` | PSS Randomness | Sign same message twice | Signatures differ ($S_1 \ne S_2$); both verify `True` | PASS |
| `test_empty_message_signing_and_verification` | Edge Case | Empty string `""` | Signs and verifies `True` | PASS |
| `test_multibyte_unicode_characters` | Unicode / Multibyte | Accents, kanji, emoji ✍️ | Signs and verifies `True` | PASS |
| `test_verify_signature_invalid_public_key` | Validation | Non-public key passed to verify | Raises `TypeError` | PASS |
| `test_cli_run_demo` | Integration / CLI | Full CLI workflow with explanation | Structured dict and explanation valid | PASS |
| `test_cli_demo_tamper` | Integration / CLI | 4-way tamper detection routine | Executes cleanly without errors | PASS |

**Total Tests**: 18  
**Passed**: 18  
**Failed**: 0  
**Execution Time**: ~0.44s  
