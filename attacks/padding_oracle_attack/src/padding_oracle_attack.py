"""AES-CBC padding-oracle demonstration and attack implementation."""

from __future__ import annotations

import argparse
import secrets
from pathlib import Path
from typing import Callable

from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size
Oracle = Callable[[bytes, bytes], bool]


def _pad_pkcs7(plaintext: bytes) -> bytes:
    padding_length = BLOCK_SIZE - len(plaintext) % BLOCK_SIZE
    return plaintext + bytes([padding_length]) * padding_length


def _has_valid_pkcs7_padding(plaintext: bytes) -> bool:
    if not plaintext:
        return False
    padding_length = plaintext[-1]
    return (
        1 <= padding_length <= BLOCK_SIZE
        and plaintext[-padding_length:] == bytes([padding_length]) * padding_length
    )


def _unpad_pkcs7(plaintext: bytes) -> bytes:
    if not _has_valid_pkcs7_padding(plaintext):
        raise ValueError("decrypted plaintext has invalid PKCS#7 padding")
    return plaintext[: -plaintext[-1]]


def encrypt_message(key: bytes, plaintext: bytes, iv: bytes) -> bytes:
    """Encrypt plaintext with AES-CBC and PKCS#7 padding."""
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"IV must be exactly {BLOCK_SIZE} bytes")
    return AES.new(key, AES.MODE_CBC, iv).encrypt(_pad_pkcs7(plaintext))


class PaddingOracle:
    """Oracle service: reveal only whether decrypted CBC data has valid padding."""

    def __init__(self, key: bytes) -> None:
        self.__key = key
        self.queries = 0

    def __call__(self, iv: bytes, ciphertext: bytes) -> bool:
        self.queries += 1
        if len(iv) != BLOCK_SIZE or not ciphertext or len(ciphertext) % BLOCK_SIZE:
            return False
        plaintext = AES.new(self.__key, AES.MODE_CBC, iv).decrypt(ciphertext)
        return _has_valid_pkcs7_padding(plaintext)


def recover_plaintext(iv: bytes, ciphertext: bytes, oracle: Oracle) -> bytes:
    """Recover and unpad CBC plaintext using only an IV, ciphertext, and oracle."""
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"IV must be exactly {BLOCK_SIZE} bytes")
    if not ciphertext or len(ciphertext) % BLOCK_SIZE:
        raise ValueError("ciphertext must contain one or more complete AES blocks")

    blocks = [ciphertext[offset : offset + BLOCK_SIZE] for offset in range(0, len(ciphertext), BLOCK_SIZE)]
    previous = iv
    recovered = bytearray()

    for target in blocks:
        intermediate = bytearray(BLOCK_SIZE)
        crafted_previous = bytearray(BLOCK_SIZE)

        for index in range(BLOCK_SIZE - 1, -1, -1):
            padding_length = BLOCK_SIZE - index
            for suffix_index in range(index + 1, BLOCK_SIZE):
                crafted_previous[suffix_index] = intermediate[suffix_index] ^ padding_length

            matching_guess = None
            for guess in range(256):
                crafted_previous[index] = guess
                if not oracle(bytes(crafted_previous), target):
                    continue

                if index > 0:
                    confirmation = bytearray(crafted_previous)
                    confirmation[index - 1] ^= 1
                    if not oracle(bytes(confirmation), target):
                        continue

                matching_guess = guess
                break

            if matching_guess is None:
                raise RuntimeError(f"oracle yielded no candidate for byte index {index}")
            intermediate[index] = matching_guess ^ padding_length

        recovered.extend(value ^ previous[index] for index, value in enumerate(intermediate))
        previous = target

    return _unpad_pkcs7(bytes(recovered))


def run_demo(message: bytes) -> str:
    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(BLOCK_SIZE)
    ciphertext = encrypt_message(key, message, iv)
    oracle = PaddingOracle(key)

    recovered = recover_plaintext(iv, ciphertext, oracle)
    try:
        recovered_text = recovered.decode("utf-8")
    except UnicodeDecodeError:
        recovered_text = repr(recovered)

    return "\n".join(
        [
            "AES-CBC padding-oracle attack demonstration",
            f"IV: {iv.hex()}",
            f"Ciphertext: {ciphertext.hex()}",
            f"Recovered plaintext: {recovered_text}",
            f"Oracle queries: {oracle.queries}",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--message",
        default="Padding oracles reveal plaintext one byte at a time.",
        help="UTF-8 message to encrypt for the demonstration",
    )
    args = parser.parse_args()

    result = run_demo(args.message.encode("utf-8"))
    print(result)
    output_path = Path(__file__).resolve().parents[1] / "outputs" / "results.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()