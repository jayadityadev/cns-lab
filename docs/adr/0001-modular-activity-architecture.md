# Modular Activity Architecture & Interactive TUI Dispatcher

The CNS Laboratory Suite is partitioned into isolated, self-contained packages for each activity (`activity1_caesar`, `activity2_vigenere`, `activity3_one_time_pad`, `activity4_digital_signature`) unified by an interactive Terminal User Interface (TUI) and headless CLI dispatcher in `main.py`.

## Context & Trade-Offs

Each activity has unique algorithmic, cryptographic, and academic analysis requirements. Packaging each activity into its own directory with dedicated core modules, CLI demonstrators, and pytest suites ensures:
1. Complete isolation of cryptographic logic and unit test vectors.
2. Independent execution via direct CLI scripts for automation and grading.
3. Centralized interactive evaluation via `main.py` with real-time character/byte data flow pipelines without introducing tight cross-activity coupling.

## Consequences

- Each activity maintains its own `README.md` and verified `execution_record.txt`.
- Unit tests are discovered automatically across all packages by `pytest` via `pyproject.toml`'s `testpaths`.
- Adding future laboratory activities requires only creating a new activity directory and registering its runner in `main.py`.
