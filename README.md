# Cryptography and Network Security (CNS) Laboratory & Activities

**Batch**: 2026_CNS_A_01  
**Group Members**: Jayaditya Dev, Durgashree M, Aryaman Tiwari, Chirag T  
**Course Outcomes**: CO1 (Classical Ciphers), CO4 (Modern Block/Stream Ciphers), CO3 (Public Key & Integrity)

---

## Workspace Structure

- `activity1_caesar/`: **Activity 1 — Classical Substitution Cipher (Caesar Cipher)**
  - `caesar.py`: Core encryption, decryption, and key normalization.
  - `cli.py`: Interactive and scripted CLI demonstration with academic explanations.
  - `tests/test_caesar.py`: Automated test suite covering known vectors, round-trip correctness, and edge cases.
  - `README.md`: Complete theoretical background, mathematical formulation, cryptanalysis, and report.
  - `execution_record.txt`: Genuine terminal output of test and CLI runs.
- `activity2_vigenere/`: **Activity 2 — Polyalphabetic Substitution Cipher (Vigenère Cipher)**
  - `vigenere.py`: Core encryption, decryption, key normalization, and stream advancement.
  - `cli.py`: Interactive and scripted CLI demonstration with academic explanations.
  - `tests/test_vigenere.py`: Automated test suite covering KAT, Caesar equivalence, key repetition, and edge cases.
  - `README.md`: Theoretical background, Tabula Recta, Kasiski/Friedman cryptanalysis, and report.
  - `execution_record.txt`: Genuine terminal output of test and CLI runs.
- `activity3_one_time_pad/`: **Activity 3 — One-Time Pad (OTP)**
  - `otp.py`: CSPRNG key generation (`secrets`), bytewise XOR, UTF-8 text wrappers.
  - `cli.py`: Interactive and scripted CLI demonstration, educational hex formatting, and two-time pad demo.
  - `tests/test_otp.py`: Automated test suite covering deterministic fixed KAT, CSPRNG randomness, length mismatch, and key reuse.
  - `README.md`: Mathematical formulation, Shannon's perfect secrecy proof, five mandatory conditions, and key management analysis.
  - `execution_record.txt`: Genuine terminal output of test and CLI runs.
- `activity4_digital_signature/`: **Activity 4 — Digital Signature Implementation**
  - `signature.py`: 2048-bit RSA key generation, RSA-PSS with SHA-256 signing, verification, and fingerprinting.
  - `cli.py`: Interactive and scripted CLI demonstration, tamper detection demo, and public key metadata.
  - `tests/test_signature.py`: Automated test suite covering valid verification, message tampering, signature corruption, and wrong key rejection.
  - `README.md`: Theoretical background, hashing and signing roles, authenticity/integrity/non-repudiation, and PKI analysis.
  - `execution_record.txt`: Genuine terminal output of test and CLI runs.
- `main.py`: Interactive Terminal User Interface (TUI) and unified CLI dispatcher. Features character/byte-level **Data Flow Pipeline Visualizations** for every activity, arrow-key navigation, and headless subcommand routing (`activity1`, `activity2`, `activity3`, `activity4`).
- `GLOSSARY.md`: Canonical cryptographic domain terminology.
- `AGENTS.md` & `docs/agents/`: Repository configuration for engineering skills and local markdown issue tracking.
- `docs/adr/`: Architecture Decision Records (e.g. `0001-modular-activity-architecture.md`).
- `docs/assignment/`: Course assignment specification ([`GROUP ASSIGNMENT on CNS.docx`](docs/assignment/GROUP%20ASSIGNMENT%20on%20CNS.docx)) and topic allocation screenshot ([`task.png`](docs/assignment/task.png)).

---

## Quickstart

### Launch Interactive TUI (Recommended)
```bash
uv run main.py
```
*Features interactive arrow-key navigation ($\uparrow$ / $\downarrow$), direct numeric keys (`1`-`6`), in-TUI activity execution, and integrated automated test runner.*

### Run All 69 Automated Tests
```bash
uv run pytest -v
```

### Direct CLI Invocations
```bash
# Activity 1: Caesar Cipher
uv run main.py activity1 -p "Hello, World!" -k 3

# Activity 2: Vigenère Cipher
uv run main.py activity2 -p "ATTACK AT DAWN!" -k "LEMON"

# Activity 3: One-Time Pad
uv run main.py activity3 -p "Top Secret Message"
uv run python activity3_one_time_pad/cli.py --demo-key-reuse

# Activity 4: Digital Signature (RSA-PSS with SHA-256)
uv run main.py activity4 -m "Academic CNS Dispatch 2026"
uv run python activity4_digital_signature/cli.py --demo-tamper
```
