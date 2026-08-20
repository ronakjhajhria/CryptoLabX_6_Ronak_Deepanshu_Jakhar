import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from brute_force_dictionary import brute_force_attack
from chi_square_attack import chi_square_attack
from shift_cipher import decrypt, encrypt


class ShiftCipherEdgeCaseTests(unittest.TestCase):
    def test_key_zero_and_round_trip(self):
        text = "Hello, WORLD! 123"
        self.assertEqual(encrypt(text, 0), text)
        self.assertEqual(decrypt(encrypt(text, 25), 25), text)

    def test_case_and_punctuation_are_preserved(self):
        text = "Abc xyz! Lowercase, UPPERCASE."
        encrypted = encrypt(text, 3)
        self.assertEqual(encrypted, "Def abc! Orzhufdvh, XSSHUFDVH.")
        self.assertEqual(decrypt(encrypted, 3), text)

    def test_attacks_try_all_keys_and_accept_empty_text(self):
        dictionary_results = brute_force_attack("", set())
        chi_results = chi_square_attack("")
        self.assertEqual(len(dictionary_results), 26)
        self.assertEqual(len(chi_results), 26)
        self.assertEqual(dictionary_results[0][0], 0)


if __name__ == "__main__":
    unittest.main()
