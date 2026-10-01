import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from padding_oracle import (
    encrypt_message,
    make_padding_oracle,
    pad_pkcs7,
    recover_plaintext,
    unpad_pkcs7,
)


class PaddingOracleAttackTests(unittest.TestCase):
    def test_pkcs7_helpers_round_trip_block_boundaries(self):
        for length in (0, 1, 15, 16, 17, 32):
            with self.subTest(length=length):
                plaintext = bytes(index % 256 for index in range(length))
                padded = pad_pkcs7(plaintext)

                self.assertEqual(len(padded) % 16, 0)
                self.assertEqual(unpad_pkcs7(padded), plaintext)

    def test_unpad_pkcs7_rejects_invalid_data(self):
        for invalid_data in (b"", b"short", bytes(15) + b"\x00", bytes(15) + b"\x02"):
            with self.subTest(invalid_data=invalid_data):
                with self.assertRaises(ValueError):
                    unpad_pkcs7(invalid_data)

    def test_recovers_binary_plaintext_at_padding_boundaries(self):
        key = bytes(range(16))
        iv = bytes(reversed(range(16)))

        for length in (0, 1, 15, 16, 17, 31, 32, 33):
            with self.subTest(length=length):
                plaintext = bytes(index % 256 for index in range(length))
                _, message_iv, ciphertext = encrypt_message(plaintext, key, iv)
                oracle_calls = 0
                padding_oracle = make_padding_oracle(key)

                def counted_oracle(candidate_iv, candidate_ciphertext):
                    nonlocal oracle_calls
                    oracle_calls += 1
                    return padding_oracle(candidate_iv, candidate_ciphertext)

                result = recover_plaintext(message_iv, ciphertext, counted_oracle)

                self.assertEqual(result.plaintext, plaintext)
                self.assertEqual(result.oracle_queries, oracle_calls)
                self.assertGreater(result.oracle_queries, 0)

    def test_rejects_malformed_ciphertext_before_querying_oracle(self):
        def unexpected_oracle(_iv, _ciphertext):
            self.fail("oracle must not be called for malformed ciphertext")

        with self.assertRaises(ValueError):
            recover_plaintext(bytes(16), b"short", unexpected_oracle)


if __name__ == "__main__":
    unittest.main()