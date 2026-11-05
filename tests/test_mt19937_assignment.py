import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.mt19937_assignment import (
    generate_keystream,
    generate_reset_token,
    mt19937_xor,
    predict_reset_token,
    recover_mt19937_seed,
)


def test_round_trip_encryption():
    message = b"Assignment 10 test message"
    ciphertext = mt19937_xor(message, 4660)
    assert mt19937_xor(ciphertext, 4660) == message


def test_16_bit_seed_recovery():
    plaintext = b"ABCDEFGHIJKLMNOPQRST" + b"A" * 14
    seed = 4242
    ciphertext = mt19937_xor(plaintext, seed)
    result = recover_mt19937_seed(ciphertext)
    assert result.seed == seed
    assert mt19937_xor(ciphertext, result.seed) == plaintext


def test_generate_reset_token_is_deterministic():
    rng = random.Random(123456)
    expected = bytes(rng.getrandbits(8) for _ in range(16))
    assert generate_reset_token(123456) == expected


def test_reset_token_prediction_in_window():
    timestamp = 1760000000
    token = generate_reset_token(timestamp)
    result = predict_reset_token(token, timestamp, window_seconds=300)
    assert result.candidates_tested == 601
    assert timestamp in result.matches
    assert generate_reset_token(result.matches[0]) == token
