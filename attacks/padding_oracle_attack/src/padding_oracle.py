"""AES-CBC PKCS#7 padding-oracle attack demonstration."""

import argparse
from dataclasses import dataclass
from typing import Callable

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


BLOCK_SIZE = AES.block_size
Oracle = Callable[[bytes, bytes], bool]


@dataclass(frozen=True)
class AttackResult:
    plaintext: bytes
    oracle_queries: int


def pad_pkcs7(data: bytes) -> bytes:
    """Add PKCS#7 padding so data is a multiple of the AES block size."""
    padding_length = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding_length]) * padding_length


def unpad_pkcs7(data: bytes) -> bytes:
    """Remove valid PKCS#7 padding or raise ValueError."""
    if not data or len(data) % BLOCK_SIZE:
        raise ValueError("data must contain complete padded blocks")

    padding_length = data[-1]
    if not 1 <= padding_length <= BLOCK_SIZE or not data.endswith(
        bytes([padding_length]) * padding_length
    ):
        raise ValueError("data has invalid PKCS#7 padding")
    return data[:-padding_length]


def encrypt_message(plaintext: bytes, key: bytes = None, iv: bytes = None):
    """Encrypt bytes for the self-contained demonstration fixture."""
    key = get_random_bytes(BLOCK_SIZE) if key is None else key
    iv = get_random_bytes(BLOCK_SIZE) if iv is None else iv
    padded_plaintext = pad_pkcs7(plaintext)
    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(padded_plaintext)
    return key, iv, ciphertext


def make_padding_oracle(key: bytes) -> Oracle:
    """Return a boolean oracle; the key remains private to this closure."""
    def oracle(iv: bytes, ciphertext: bytes) -> bool:
        if len(iv) != BLOCK_SIZE or not ciphertext or len(ciphertext) % BLOCK_SIZE:
            return False

        plaintext = AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext)
        try:
            unpad_pkcs7(plaintext)
        except ValueError:
            return False
        return True

    return oracle


def recover_plaintext(iv: bytes, ciphertext: bytes, oracle: Oracle) -> AttackResult:
    """Recover padded CBC plaintext using only an IV, ciphertext, and oracle."""
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"IV must be {BLOCK_SIZE} bytes")
    if not ciphertext or len(ciphertext) % BLOCK_SIZE:
        raise ValueError("ciphertext must contain one or more complete blocks")

    previous_blocks = [iv] + [
        ciphertext[offset:offset + BLOCK_SIZE]
        for offset in range(0, len(ciphertext), BLOCK_SIZE)
    ]
    recovered = bytearray()
    query_count = 0

    def query(candidate_iv: bytes, target_block: bytes) -> bool:
        nonlocal query_count
        query_count += 1
        return oracle(candidate_iv, target_block)

    for block_index in range(1, len(previous_blocks)):
        original_previous = previous_blocks[block_index - 1]
        target_block = previous_blocks[block_index]
        intermediate = bytearray(BLOCK_SIZE)
        plaintext_block = bytearray(BLOCK_SIZE)

        for byte_index in range(BLOCK_SIZE - 1, -1, -1):
            padding_length = BLOCK_SIZE - byte_index
            crafted_previous = bytearray(original_previous)

            for known_index in range(byte_index + 1, BLOCK_SIZE):
                crafted_previous[known_index] = (
                    intermediate[known_index] ^ padding_length
                )

            for candidate in range(256):
                crafted_previous[byte_index] = candidate
                if not query(bytes(crafted_previous), target_block):
                    continue

                if byte_index > 0:
                    confirmation = bytearray(crafted_previous)
                    confirmation[byte_index - 1] ^= 1
                    if not query(bytes(confirmation), target_block):
                        continue

                intermediate[byte_index] = candidate ^ padding_length
                plaintext_block[byte_index] = (
                    intermediate[byte_index] ^ original_previous[byte_index]
                )
                break
            else:
                raise RuntimeError(
                    f"oracle did not reveal byte {byte_index} of block {block_index}"
                )

        recovered.extend(plaintext_block)

    try:
        plaintext = unpad_pkcs7(recovered)
    except ValueError as error:
        raise RuntimeError("recovered plaintext has invalid PKCS#7 padding") from error

    return AttackResult(plaintext, query_count)


def run_demo(plaintext: str) -> AttackResult:
    key, iv, ciphertext = encrypt_message(plaintext.encode("utf-8"))
    oracle = make_padding_oracle(key)
    return recover_plaintext(iv, ciphertext, oracle)


def main():
    parser = argparse.ArgumentParser(
        description="Demonstrate AES-CBC plaintext recovery via a padding oracle"
    )
    parser.add_argument(
        "--plaintext",
        default="Padding oracle attacks recover plaintext without the AES key.",
        help="UTF-8 message used by the local encryption/oracle demonstration",
    )
    args = parser.parse_args()

    result = run_demo(args.plaintext)
    print("Recovered plaintext:")
    print(result.plaintext.decode("utf-8", errors="replace"))
    print(f"Oracle queries: {result.oracle_queries}")
    print("AES key used by attack: none (key is held only by the demo oracle)")


if __name__ == "__main__":
    main()