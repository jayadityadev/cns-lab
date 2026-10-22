import pytest
from activity2_vigenere.vigenere import normalize_key, encrypt, decrypt


def test_normalize_key_standard():
    assert normalize_key("LEMON") == "LEMON"
    assert normalize_key("lemon") == "LEMON"
    assert normalize_key("LeMoN") == "LEMON"
    assert normalize_key("a") == "A"


def test_normalize_key_empty():
    with pytest.raises(ValueError, match="non-empty"):
        normalize_key("")


def test_normalize_key_non_alphabetic():
    with pytest.raises(ValueError):
        normalize_key("LEMON123")
    with pytest.raises(ValueError):
        normalize_key("LE MON")
    with pytest.raises(ValueError):
        normalize_key("LEMON!")
    with pytest.raises(ValueError):
        normalize_key("12345")


def test_normalize_key_invalid_types():
    with pytest.raises(TypeError):
        normalize_key(123)
    with pytest.raises(TypeError):
        normalize_key(None)
    with pytest.raises(TypeError):
        normalize_key(True)
    with pytest.raises(TypeError):
        normalize_key(["L", "E", "M", "O", "N"])


def test_encrypt_known_answers():
    # Classical standard known answer test vector
    assert encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert encrypt("CRYPTO", "KEY") == "MVWZXM"


def test_encrypt_single_character_key():
    # Single character key 'D' is shift 3, equivalent to Caesar Cipher shift 3
    assert encrypt("HELLO", "D") == "KHOOR"
    assert encrypt("hello", "d") == "khoor"
    assert encrypt("A", "A") == "A"  # Shift 0


def test_encrypt_key_longer_than_plaintext():
    # Key 'VERYLONGKEY' has length 11; plaintext 'HELLO' has length 5
    assert encrypt("HELLO", "VERYLONGKEY") == "CICJZ"


def test_encrypt_plaintext_longer_than_key():
    # Verifies cyclic repetition of short key 'ABC'
    # 'A' shifts 0, 'B' shifts 1, 'C' shifts 2
    assert encrypt("AAAAAA", "ABC") == "ABCABC"


def test_encrypt_invalid_plaintext_type():
    with pytest.raises(TypeError):
        encrypt(12345, "KEY")
    with pytest.raises(TypeError):
        encrypt(None, "KEY")


def test_encrypt_case_and_punctuation_preservation():
    # Key stream advances only on letters
    plaintext = "Attack at DAWN!"
    expected = "Lxfopv ef RNHR!"
    assert encrypt(plaintext, "LEMON") == expected


def test_encrypt_no_alphabetic_characters():
    assert encrypt("1234567890", "KEY") == "1234567890"
    assert encrypt("!@#$%^&*()_+", "KEY") == "!@#$%^&*()_+"
    assert encrypt("   \t\n  ", "KEY") == "   \t\n  "


def test_encrypt_empty_plaintext():
    assert encrypt("", "KEY") == ""


def test_encrypt_repeated_patterns():
    assert encrypt("AAAA", "A") == "AAAA"
    assert encrypt("AAAA", "B") == "BBBB"
    assert encrypt("ABAB", "AB") == "ACAC"


def test_decrypt_known_answers():
    assert decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
    assert decrypt("MVWZXM", "KEY") == "CRYPTO"
    assert decrypt("Lxfopv ef RNHR!", "lemon") == "Attack at DAWN!"
    assert decrypt("KHOOR", "D") == "HELLO"


def test_round_trip_property():
    cases = [
        ("The quick brown fox jumps over the lazy dog.", "SECRET"),
        ("Pack my box with five dozen liquor jugs!", "CRYPTOGRAPHY"),
        ("Polyalphabetic substitution using Vigenere table @ 2026!", "LEMON"),
        ("Short", "VERYLONGKEYWHICHEXCEEDSTHETEXTLENGTH"),
        ("Upper and lower CASE mixing with punctuation: ; , . - !", "CIPHER"),
        ("1234567890", "KEY"),
        ("", "KEY"),
        ("Single char key equivalent to Caesar", "K"),
    ]
    for plaintext, key in cases:
        ciphertext = encrypt(plaintext, key)
        recovered = decrypt(ciphertext, key)
        assert recovered == plaintext, f"Round trip failed for key='{key}', plaintext='{plaintext}'"


def test_decrypt_invalid_types():
    with pytest.raises(TypeError):
        decrypt(12345, "KEY")
    with pytest.raises(TypeError):
        decrypt(None, "KEY")
    with pytest.raises(TypeError):
        decrypt("CIPHER", 123)
    with pytest.raises(ValueError):
        decrypt("CIPHER", "")


def test_cli_run_demo():
    from activity2_vigenere.cli import run_demo, format_explanation

    result = run_demo("ATTACK AT DAWN!", "LEMON")
    assert result["plaintext"] == "ATTACK AT DAWN!"
    assert result["key"] == "LEMON"
    assert result["normalized_key"] == "LEMON"
    assert result["ciphertext"] == "LXFOPV EF RNHR!"
    assert result["recovered"] == "ATTACK AT DAWN!"
    assert result["round_trip_success"] is True

    explanation = format_explanation()
    assert "COMPLETELY INSECURE" in explanation
    assert "Kasiski Examination" in explanation
    assert "Tabula Recta" in explanation




