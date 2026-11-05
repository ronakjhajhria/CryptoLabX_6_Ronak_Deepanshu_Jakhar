import secrets
import unittest

from Crypto.Cipher import AES

from attacks.padding_oracle_attack.src.padding_oracle_attack import (
    PaddingOracle,
    encrypt_message,
    recover_plaintext,
)


class PaddingOracleAttackTests(unittest.TestCase):
    def test_recovers_arbitrary_multiblock_plaintext_without_attack_key(self) -> None:
        plaintext = b"A different message, across multiple blocks: \x00\xff"
        key = secrets.token_bytes(32)
        iv = secrets.token_bytes(AES.block_size)
        ciphertext = encrypt_message(key, plaintext, iv)
        oracle = PaddingOracle(key)

        recovered = recover_plaintext(iv, ciphertext, oracle)

        self.assertEqual(recovered, plaintext)
        self.assertGreater(oracle.queries, 0)

    def test_rejects_malformed_ciphertext(self) -> None:
        with self.assertRaises(ValueError):
            recover_plaintext(bytes(AES.block_size), b"short", lambda _iv, _data: False)


if __name__ == "__main__":
    unittest.main()