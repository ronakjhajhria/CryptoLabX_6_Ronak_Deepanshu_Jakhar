import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from os_random_analysis import analyze, bit_distribution, repeated_pattern_metrics, serial_correlation


class OSRandomAnalysisTests(unittest.TestCase):
    def test_analyze_reports_required_metrics(self):
        data = bytes(i % 256 for i in range(4096))
        result = analyze(data)
        self.assertEqual(result["size_bytes"], 4096)
        self.assertIn("zero_bits", result)
        self.assertIn("serial_correlation_lag1", result)
        self.assertIn("repeated_16_byte_blocks", result)

    def test_bit_distribution_is_consistent(self):
        data = bytes([0x00, 0xFF])
        zeros, ones, ratio = bit_distribution(data)
        self.assertEqual(zeros, 8)
        self.assertEqual(ones, 8)
        self.assertAlmostEqual(ratio, 0.5)

    def test_repeated_pattern_metrics_counts_unique_blocks(self):
        data = b"AAAAAAAAAAAAAAAA" + b"AAAAAAAAAAAAAAAA"
        total, unique = repeated_pattern_metrics(data)
        self.assertEqual(total, 2)
        self.assertEqual(unique, 1)

    def test_serial_correlation_is_bounded(self):
        correlation = serial_correlation(bytes([0, 1, 0, 1, 0, 1]))
        self.assertGreaterEqual(correlation, -1.0)
        self.assertLessEqual(correlation, 1.0)


if __name__ == "__main__":
    unittest.main()
