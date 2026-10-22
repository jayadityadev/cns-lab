import pytest
from activity3_one_time_pad.otp import generate_key, xor_bytes, encrypt, decrypt


def test_generate_key_length():
    key10 = generate_key(10)
    assert isinstance(key10, bytes)
    assert len(key10) == 10

    key0 = generate_key(0)
    assert isinstance(key0, bytes)
    assert len(key0) == 0

    key100 = generate_key(100)
    assert len(key100) == 100


def test_generate_key_independence():
    # CSPRNG successive calls should generate distinct bytes
    k1 = generate_key(32)
    k2 = generate_key(32)
    assert k1 != k2


def test_generate_key_invalid_length():
    with pytest.raises(ValueError):
        generate_key(-1)
    with pytest.raises(TypeError):
        generate_key("10")
    with pytest.raises(TypeError):
        generate_key(10.5)
    with pytest.raises(TypeError):
        generate_key(None)
    with pytest.raises(TypeError):
        generate_key(True)  # bool is subclass of int in Python, should be rejected


def test_xor_bytes_known_vector():
    data = b"\x01\x02\x03\x04"
    key = b"\x10\x20\x30\x40"
    expected = b"\x11\x22\x33\x44"
    assert xor_bytes(data, key) == expected


def test_xor_bytes_mathematical_properties():
    data = b"Hello, World!"
    key = generate_key(len(data))
    
    # Invertibility: (data ^ key) ^ key == data
    cipher = xor_bytes(data, key)
    assert xor_bytes(cipher, key) == data
    
    # Self-inverse: data ^ data == 0x00 * len
    assert xor_bytes(data, data) == b"\x00" * len(data)
    
    # Identity: data ^ zeros == data
    zeros = b"\x00" * len(data)
    assert xor_bytes(data, zeros) == data


def test_xor_bytes_length_mismatch():
    # Key shorter than data
    with pytest.raises(ValueError, match="match"):
        xor_bytes(b"HELLO", b"KEY")
        
    # Key longer than data
    with pytest.raises(ValueError, match="match"):
        xor_bytes(b"KEY", b"LONGERKEY")


def test_xor_bytes_invalid_types():
    with pytest.raises(TypeError):
        xor_bytes("string", b"bytes")
    with pytest.raises(TypeError):
        xor_bytes(b"bytes", "string")
    with pytest.raises(TypeError):
        xor_bytes(123, b"bytes")
    with pytest.raises(TypeError):
        xor_bytes(b"bytes", None)


def test_encrypt_decrypt_known_vector():
    plaintext = "CNS 2026"
    key = b"\xaa\xbb\xcc\xdd\xee\xff\x11\x22"
    expected_cipher = b"\xe9\xf5\x9f\xfd\xdc\xcf\x23\x14"
    
    ciphertext = encrypt(plaintext, key)
    assert ciphertext == expected_cipher
    assert len(ciphertext) == len(plaintext.encode("utf-8"))
    
    decoded_text, raw_bytes = decrypt(ciphertext, key)
    assert decoded_text == plaintext
    assert raw_bytes == plaintext.encode("utf-8")


def test_encrypt_accepts_raw_bytes():
    raw_data = b"\x00\xff\x12\x34\x56"
    key = b"\xaa\xbb\xcc\xdd\xee"
    cipher = encrypt(raw_data, key)
    _, recovered = decrypt(cipher, key)
    assert recovered == raw_data


def test_encrypt_decrypt_random_key_round_trip():
    messages = [
        "The quick brown fox jumps over the lazy dog.",
        "One-Time Pad provides information-theoretic perfect secrecy.",
        "A",
        "Short message",
        "Numbers 1234567890 and symbols !@#$%^&*()_+",
    ]
    for msg in messages:
        msg_bytes = msg.encode("utf-8")
        key = generate_key(len(msg_bytes))
        ciphertext = encrypt(msg, key)
        assert len(ciphertext) == len(msg_bytes)
        
        decoded, raw = decrypt(ciphertext, key)
        assert decoded == msg
        assert raw == msg_bytes


def test_encrypt_invalid_types():
    with pytest.raises(TypeError):
        encrypt(12345, b"key")
    with pytest.raises(TypeError):
        encrypt(None, b"key")
    with pytest.raises(TypeError):
        encrypt("hello", "string_key")


def test_empty_message():
    key0 = generate_key(0)
    ciphertext = encrypt("", key0)
    assert ciphertext == b""
    decoded, raw = decrypt(ciphertext, key0)
    assert decoded == ""
    assert raw == b""


def test_multibyte_utf8_characters():
    # Multibyte characters: Zurich (ü: 2 bytes), Tokyo in kanji (東京: 6 bytes), lock emoji (🔐: 4 bytes)
    plaintext = "Cryptography 🔐: Zürich & Tokyo 東京 2026!"
    msg_bytes = plaintext.encode("utf-8")
    assert len(msg_bytes) > len(plaintext)  # Confirm multibyte expansion
    
    key = generate_key(len(msg_bytes))
    ciphertext = encrypt(plaintext, key)
    assert len(ciphertext) == len(msg_bytes)
    
    decoded, raw = decrypt(ciphertext, key)
    assert decoded == plaintext
    assert raw == msg_bytes


def test_decrypt_with_incorrect_key():
    plaintext = "Confidential military plan."
    msg_bytes = plaintext.encode("utf-8")
    correct_key = generate_key(len(msg_bytes))
    wrong_key = generate_key(len(msg_bytes))
    
    ciphertext = encrypt(plaintext, correct_key)
    decoded, raw = decrypt(ciphertext, wrong_key)
    
    # Must not recover original plaintext
    assert decoded != plaintext
    assert raw != msg_bytes


def test_two_time_pad_vulnerability():
    # Demonstrates catastrophic key reuse: C1 ^ C2 == M1 ^ M2
    m1 = "ATTACK AT DAWN!"
    m2 = "DEFEND THE WALL"
    b1 = m1.encode("utf-8")
    b2 = m2.encode("utf-8")
    assert len(b1) == len(b2)
    
    shared_key = generate_key(len(b1))
    c1 = encrypt(m1, shared_key)
    c2 = encrypt(m2, shared_key)
    
    # The XOR difference of ciphertexts equals XOR difference of plaintexts
    xor_ciphertexts = xor_bytes(c1, c2)
    xor_plaintexts = xor_bytes(b1, b2)
    assert xor_ciphertexts == xor_plaintexts
    
    # Given m1 and both ciphertexts, adversary derives m2 without knowing key
    recovered_m2 = xor_bytes(xor_ciphertexts, b1)
    assert recovered_m2.decode("utf-8") == m2


def test_cli_run_demo():
    from activity3_one_time_pad.cli import run_demo, format_explanation

    result = run_demo("CNS Lab OTP Test 2026!")
    assert result["plaintext"] == "CNS Lab OTP Test 2026!"
    assert result["round_trip_success"] is True
    assert len(result["key_hex"]) == len(result["ciphertext_hex"])
    
    explanation = format_explanation()
    assert "PERFECT SECRECY" in explanation
    assert "CSPRNG" in explanation
    assert "Two-Time Pad Attack" in explanation


def test_cli_demo_key_reuse():
    from activity3_one_time_pad.cli import demo_key_reuse
    
    # Ensures demo_key_reuse executes without exceptions
    demo_key_reuse()




