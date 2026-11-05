import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from miller_rabin_prime import (
    generate_probable_prime,
    independent_is_prime,
    miller_rabin,
    random_odd_candidate,
)


class MillerRabinPrimeTests(unittest.TestCase):
    def test_known_small_primes_and_composites(self):
        bases = (2, 3, 5, 7, 11)
        for prime in (2, 3, 5, 7, 11, 13, 97, 101, 997):
            self.assertTrue(miller_rabin(prime, bases), prime)
        for composite in (4, 9, 15, 21, 221, 341):
            self.assertFalse(miller_rabin(composite, bases), composite)

    def test_random_candidate_has_exact_bit_length_and_is_odd(self):
        for bits in (16, 32, 512):
            candidate = random_odd_candidate(bits)
            self.assertEqual(candidate.bit_length(), bits)
            self.assertEqual(candidate & 1, 1)

    def test_generated_512_bit_prime_passes_both_verifications(self):
        result = generate_probable_prime(512, 40)
        self.assertEqual(result.candidate.bit_length(), 512)
        self.assertGreaterEqual(result.candidates_tested, 1)
        self.assertEqual(result.miller_rabin_rounds_executed, result.candidates_tested * 40)
        self.assertTrue(miller_rabin(result.candidate, tuple(range(2, 42))))
        self.assertTrue(independent_is_prime(result.candidate))


if __name__ == "__main__":
    unittest.main()
