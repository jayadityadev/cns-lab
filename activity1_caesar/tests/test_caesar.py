import pytest
from activity1_caesar.caesar import normalize_key, encrypt, decrypt


def test_normalize_key_standard():
    assert normalize_key(3) == 3


def test_normalize_key_zero():
    assert normalize_key(0) == 0


def test_normalize_key_twenty_five():
    assert normalize_key(25) == 25


def test_normalize_key_greater_than_twenty_five():
    assert normalize_key(26) == 0
    assert normalize_key(29) == 3


def test_normalize_key_negative():
    assert normalize_key(-1) == 25
    assert normalize_key(-3) == 23


def test_normalize_key_invalid_types():
    with pytest.raises(TypeError):
        normalize_key("3")
    with pytest.raises(TypeError):
        normalize_key(3.14)
    with pytest.raises(TypeError):
        normalize_key(None)
    with pytest.raises(TypeError):
        normalize_key(True)  # bool is subclass of int in Python, should be explicitly rejected


def test_encrypt_known_answers():
    assert encrypt("HELLO", 3) == "KHOOR"
    assert encrypt("hello", 3) == "khoor"
    assert encrypt("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", 13) == "GUR DHVPX OEBJA SBK WHZCF BIRE GUR YNML QBT"


def test_encrypt_wrap_boundaries():
    assert encrypt("XYZ", 3) == "ABC"
    assert encrypt("xyz", 3) == "abc"
    assert encrypt("B", 25) == "A"
    assert encrypt("b", 25) == "a"


def test_encrypt_key_variations():
    assert encrypt("Python", 0) == "Python"
    assert encrypt("Python", 26) == "Python"
    assert encrypt("Python", 29) == encrypt("Python", 3)
    assert encrypt("Python", -1) == encrypt("Python", 25)


def test_encrypt_invalid_plaintext_type():
    with pytest.raises(TypeError):
        encrypt(12345, 3)
    with pytest.raises(TypeError):
        encrypt(None, 3)


def test_encrypt_empty_message():
    assert encrypt("", 3) == ""
    assert encrypt("", 0) == ""


def test_encrypt_non_alphabetic_preservation():
    # Only punctuation and digits
    assert encrypt("1234567890", 5) == "1234567890"
    assert encrypt("!@#$%^&*()_+-=[]{}|;':\",./<>?", 7) == "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    
    # Mixed alphanumeric and punctuation
    plaintext = "CNS Lab: Activity-01 (Caesar Cipher) @ 2026!"
    expected = "FQV Ode: Dfwlylwb-01 (Fdhvdu Flskhu) @ 2026!"
    assert encrypt(plaintext, 3) == expected


def test_encrypt_repeated_characters():
    assert encrypt("AAAA", 1) == "BBBB"
    assert encrypt("zzzz", 2) == "bbbb"
    assert encrypt("....", 4) == "...."


def test_decrypt_known_answers():
    assert decrypt("KHOOR", 3) == "HELLO"
    assert decrypt("khoor", 3) == "hello"
    assert decrypt("GUR DHVPX OEBJA SBK WHZCF BIRE GUR YNML QBT", 13) == "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"


def test_round_trip_property():
    test_cases = [
        ("The quick brown fox jumps over the lazy dog.", 3),
        ("Pack my box with five dozen liquor jugs!", 13),
        ("Special chars: 12345 @ # $ % ^ & * ( ) _ +", 7),
        ("Upper and lower CASE mixing!", 25),
        ("Large key normalization test", 100),
        ("Zero key identity", 0),
        ("Negative key shift", -7),
        ("", 15),
        ("1234567890", 10),
        ("AAAAAaaaaa", 4),
    ]
    for plaintext, key in test_cases:
        ciphertext = encrypt(plaintext, key)
        recovered = decrypt(ciphertext, key)
        assert recovered == plaintext, f"Round trip failed for key={key}, plaintext='{plaintext}'"


def test_decrypt_invalid_types():
    with pytest.raises(TypeError):
        decrypt(12345, 3)
    with pytest.raises(TypeError):
        decrypt("HELLO", "3")
    with pytest.raises(TypeError):
        decrypt(None, 3)


def test_cli_run_demo():
    from activity1_caesar.cli import run_demo, format_explanation
    
    result = run_demo("Confidential Dispatch 2026!", 3)
    assert result["plaintext"] == "Confidential Dispatch 2026!"
    assert result["key"] == 3
    assert result["normalized_key"] == 3
    assert result["ciphertext"] == "Frqilghqwldo Glvsdwfk 2026!"
    assert result["recovered"] == "Confidential Dispatch 2026!"
    assert result["round_trip_success"] is True
    
    explanation = format_explanation()
    assert "COMPLETELY INSECURE" in explanation
    assert "Julius Caesar" in explanation




