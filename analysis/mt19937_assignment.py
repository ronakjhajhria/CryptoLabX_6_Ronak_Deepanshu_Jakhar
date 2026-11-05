"""Assignment 10: MT19937 stream cipher and predictable reset tokens."""

import random
import secrets
import string
import time
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class SeedRecoveryResult:
    seed: int
    plaintext: bytes


@dataclass(frozen=True)
class TokenPredictionResult:
    timestamp: int
    observed_token: bytes
    candidates_tested: int
    matches: tuple[int, ...]


def generate_keystream(seed: int, length: int) -> bytes:
    """Generate length bytes using Python's MT19937 and getrandbits(8)."""
    rng = random.Random(seed)
    return bytes(rng.getrandbits(8) for _ in range(length))


def mt19937_xor(data: bytes, seed: int) -> bytes:
    """Encrypt or decrypt data with an MT19937 byte keystream."""
    keystream = generate_keystream(seed, len(data))
    return bytes(value ^ key for value, key in zip(data, keystream))


def generate_known_plaintext(prefix_length: Optional[int] = None) -> bytes:
    """Create printable ASCII prefix followed by exactly 14 ASCII 'A' bytes."""
    if prefix_length is None:
        prefix_length = secrets.randbelow(16) + 5  # 5 through 20 inclusive
    if not 5 <= prefix_length <= 20:
        raise ValueError("prefix_length must be between 5 and 20")
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    prefix = "".join(secrets.choice(alphabet) for _ in range(prefix_length))
    return (prefix + "A" * 14).encode("ascii")


def recover_mt19937_seed(ciphertext: bytes, known: bytes = b"A" * 14) -> SeedRecoveryResult:
    """Brute-force every 16-bit seed and locate a valid known-plaintext candidate."""
    matches = []
    for seed in range(1 << 16):
        plaintext = mt19937_xor(ciphertext, seed)
        if known not in plaintext:
            continue
        location = len(plaintext) - len(known)
        if 5 <= location <= 20 and plaintext.endswith(known) and all(32 <= b <= 126 for b in plaintext):
            matches.append(SeedRecoveryResult(seed=seed, plaintext=plaintext))

    if len(matches) != 1:
        raise RuntimeError(f"Expected one matching seed, found {len(matches)}")
    return matches[0]


def generate_reset_token(timestamp: int) -> bytes:
    """Generate a 16-byte token using 16 consecutive 8-bit MT19937 outputs."""
    return generate_keystream(timestamp, 16)


def predict_reset_token(observed_token: bytes, timestamp: int, window_seconds: int = 300) -> TokenPredictionResult:
    """Search every timestamp in [timestamp-window, timestamp+window]."""
    if len(observed_token) != 16:
        raise ValueError("observed_token must be exactly 16 bytes")

    matches = []
    candidates = range(timestamp - window_seconds, timestamp + window_seconds + 1)
    for candidate in candidates:
        if generate_reset_token(candidate) == observed_token:
            matches.append(candidate)

    return TokenPredictionResult(
        timestamp=timestamp,
        observed_token=observed_token,
        candidates_tested=2 * window_seconds + 1,
        matches=tuple(matches),
    )


def format_hex(data: bytes) -> str:
    return data.hex()


def run_assignment(seed: Optional[int] = None, prefix_length: Optional[int] = None) -> dict:
    """Run both demonstrations and return structured self-test information."""
    test_message = b"Cryptography Lab Assignment 10"
    test_seed = 0x1234 if seed is None else seed
    encrypted_test = mt19937_xor(test_message, test_seed)
    decrypted_test = mt19937_xor(encrypted_test, test_seed)

    stream_seed = secrets.randbelow(1 << 16)
    plaintext = generate_known_plaintext(prefix_length=prefix_length)
    ciphertext = mt19937_xor(plaintext, stream_seed)
    recovered = recover_mt19937_seed(ciphertext)
    recovered_verified = mt19937_xor(ciphertext, recovered.seed) == plaintext

    token_timestamp = int(time.time())
    observed_token = generate_reset_token(token_timestamp)
    prediction = predict_reset_token(observed_token, token_timestamp)
    verified_timestamp = bool(prediction.matches and prediction.matches[0] == token_timestamp)
    regenerated_token = generate_reset_token(prediction.matches[0]) if prediction.matches else None

    return {
        "part_a_test": {
            "seed": test_seed,
            "plaintext": test_message.decode("ascii"),
            "ciphertext_hex": format_hex(encrypted_test),
            "decrypted": decrypted_test.decode("ascii"),
            "round_trip_ok": decrypted_test == test_message,
        },
        "part_a_seed_recovery": {
            "selected_seed": stream_seed,
            "plaintext": plaintext.decode("ascii"),
            "ciphertext_hex": format_hex(ciphertext),
            "recovered_seed": recovered.seed,
            "full_plaintext_verified": recovered_verified,
            "known_sequence_verified": b"A" * 14 in recovered.plaintext,
        },
        "part_b_token_prediction": {
            "timestamp": token_timestamp,
            "interval": [token_timestamp - 300, token_timestamp + 300],
            "candidates_tested": prediction.candidates_tested,
            "observed_token_hex": format_hex(observed_token),
            "matches": list(prediction.matches),
            "timestamp_verified": verified_timestamp,
            "regenerated_token_hex": format_hex(regenerated_token) if regenerated_token else None,
        },
    }


def main() -> None:
    result = run_assignment()

    print("Assignment 10 - MT19937 Stream Cipher and Predictable Tokens")
    print("\nPART A: Encryption/decryption verification")
    test = result["part_a_test"]
    print(f"Seed: {test['seed']}")
    print(f"Plaintext: {test['plaintext']}")
    print(f"Ciphertext (hex): {test['ciphertext_hex']}")
    print(f"Decrypted: {test['decrypted']}")
    print(f"Round trip successful: {test['round_trip_ok']}")

    print("\nPART A: Known-plaintext seed recovery")
    recovery = result["part_a_seed_recovery"]
    print(f"Randomly selected seed: {recovery['selected_seed']}")
    print(f"Plaintext: {recovery['plaintext']}")
    print(f"Ciphertext (hex): {recovery['ciphertext_hex']}")
    print(f"Search space: 65,536 seeds (16-bit)")
    print(f"Recovered seed: {recovery['recovered_seed']}")
    print(f"Full plaintext verified: {recovery['full_plaintext_verified']}")
    print(f"Known 14-character sequence verified: {recovery['known_sequence_verified']}")

    print("\nPART B: Timestamp token prediction")
    prediction = result["part_b_token_prediction"]
    print(f"Token generation timestamp T: {prediction['timestamp']}")
    print(f"Search interval: T-300 to T+300 = {prediction['interval']}")
    print(f"Candidates tested: {prediction['candidates_tested']}")
    print(f"Observed token (hex): {prediction['observed_token_hex']}")
    print(f"Matching timestamp(s): {prediction['matches']}")
    print(f"Timestamp verified: {prediction['timestamp_verified']}")
    print(f"Regenerated token (hex): {prediction['regenerated_token_hex']}")


if __name__ == "__main__":
    main()
