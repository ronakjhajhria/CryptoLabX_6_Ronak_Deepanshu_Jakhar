"""Collect and statistically analyze OS cryptographic random number sources."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

BLOCK_SIZE = 1024 * 1024


def generate_via_dev_urandom(size: int, output_path: Path) -> bool:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if sys.platform.startswith("linux"):
        command = f"dd if=/dev/urandom of={str(output_path)} bs=1M count={math.ceil(size / BLOCK_SIZE)} status=none"
        subprocess.run(command, shell=True, check=True)
        with output_path.open("rb") as source:
            data = source.read(size)
        output_path.write_bytes(data)
        return True

    wsl = shutil.which("wsl")
    if wsl:
        data = bytearray()
        remaining = size
        while remaining:
            block = min(BLOCK_SIZE, remaining)
            completed = subprocess.run([wsl, "dd", "if=/dev/urandom", "bs=1", f"count={block}", "status=none"], stdout=subprocess.PIPE, check=True)
            chunk = completed.stdout
            if len(chunk) != block:
                return False
            data.extend(chunk)
            remaining -= block
        output_path.write_bytes(data)
        return True
    return False


def generate_via_openssl(size: int, output_path: Path) -> bool:
    openssl = shutil.which("openssl")
    if not openssl:
        return False
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as output:
        subprocess.run([openssl, "rand", str(size)], stdout=output, check=True)
    return True


def chi_square_uniform_bytes(data: bytes) -> tuple[float, float]:
    counts = Counter(data)
    expected = len(data) / 256
    statistic = sum((counts[value] - expected) ** 2 / expected for value in range(256))
    dof = 255
    threshold = 310.457  # Approximate chi-square 99% critical value for 255 degrees of freedom.
    return statistic, threshold


def bit_distribution(data: bytes) -> tuple[int, int, float]:
    bit_count = len(data) * 8
    ones = sum(byte.bit_count() for byte in data)
    zeros = bit_count - ones
    return zeros, ones, ones / bit_count


def monobit_z_test(data: bytes) -> tuple[float, bool]:
    n = len(data) * 8
    ones = sum(byte.bit_count() for byte in data)
    difference = 2 * ones - n
    z = abs(difference) / math.sqrt(n)
    return z, z < 2.576


def runs_test(data: bytes) -> tuple[float, bool, int]:
    bits = [(byte >> shift) & 1 for byte in data for shift in range(7, -1, -1)]
    ones = sum(bits)
    zeroes = len(bits) - ones
    runs = 1
    for previous, current in zip(bits, bits[1:]):
        if previous != current:
            runs += 1
    if ones == 0 or zeroes == 0:
        return 0.0, False, runs
    expected = ((2 * ones * zeroes) / len(bits)) + 1
    variance = (2 * ones * zeroes * (2 * ones * zeroes - len(bits))) / (len(bits) ** 2 * (len(bits) - 1))
    z = abs((runs - expected) / math.sqrt(variance)) if variance else 0.0
    return z, z < 2.576, runs


def serial_correlation(data: bytes, lag: int = 1) -> float:
    if len(data) <= lag:
        return 0.0
    left = data[:-lag]
    right = data[lag:]
    mean_left = sum(left) / len(left)
    mean_right = sum(right) / len(right)
    numerator = sum((a - mean_left) * (b - mean_right) for a, b in zip(left, right))
    denominator_left = sum((a - mean_left) ** 2 for a in left)
    denominator_right = sum((b - mean_right) ** 2 for b in right)
    denominator = math.sqrt(denominator_left * denominator_right)
    return numerator / denominator if denominator else 0.0


def repeated_pattern_metrics(data: bytes, block_size: int = 16) -> tuple[int, int]:
    blocks = [data[i:i + block_size] for i in range(0, len(data), block_size)]
    total_blocks = len(blocks)
    unique_blocks = len(set(blocks))
    return total_blocks, unique_blocks


def shannon_byte_entropy(data: bytes) -> float:
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def analyze(data: bytes) -> dict:
    chi2, threshold = chi_square_uniform_bytes(data)
    zeros, ones, one_ratio = bit_distribution(data)
    monobit_z, monobit_pass = monobit_z_test(data)
    runs_z, runs_pass, runs = runs_test(data)
    total_blocks, unique_blocks = repeated_pattern_metrics(data)
    return {
        "size_bytes": len(data),
        "byte_chi_square": chi2,
        "chi_square_threshold_p099": threshold,
        "byte_uniformity_pass": chi2 < threshold,
        "zero_bits": zeros,
        "one_bits": ones,
        "one_bit_ratio": one_ratio,
        "monobit_z": monobit_z,
        "monobit_pass": monobit_pass,
        "runs": runs,
        "runs_z": runs_z,
        "runs_pass": runs_pass,
        "serial_correlation_lag1": serial_correlation(data, 1),
        "total_16_byte_blocks": total_blocks,
        "unique_16_byte_blocks": unique_blocks,
        "repeated_16_byte_blocks": total_blocks - unique_blocks,
        "shannon_byte_entropy": shannon_byte_entropy(data),
    }


def format_report(source_results: dict[str, dict]) -> str:
    lines = ["# Operating-System Cryptographic Random-Number Analysis", "", "| Source | Bytes | Chi-square | Byte uniformity | One-bit ratio | Monobit z | Runs z | Lag-1 correlation | Unique/Total 16-byte blocks | Shannon entropy |", "|---|---:|---:|:---:|---:|---:|---:|---:|---:|---:|"]
    for source, result in source_results.items():
        lines.append(
            f"| {source} | {result['size_bytes']} | {result['byte_chi_square']:.2f} | "
            f"{'PASS' if result['byte_uniformity_pass'] else 'FAIL'} | {result['one_bit_ratio']:.6f} | "
            f"{result['monobit_z']:.4f} | {result['runs_z']:.4f} | {result['serial_correlation_lag1']:.8f} | "
            f"{result['unique_16_byte_blocks']}/{result['total_16_byte_blocks']} | {result['shannon_byte_entropy']:.6f} |"
        )
    lines += [
        "",
        "## Interpretation",
        "A byte chi-square below the reported 255-degree-of-freedom threshold and one-bit/runs ratios near their expected values support statistical randomness, not cryptographic security.",
        "Serious repeated blocks are expected to remain rare over 1 MB; these counts are not proof of independence.",
        "The monobit and runs tests are bounded examples, not a replacement for the full NIST or Dieharder suites.",
    ]
    return "\n".join(lines)


def generate_via_windows_cng(size: int, output_path: Path) -> bool:
    """Generate bytes using Windows CNG BCryptGenRandom directly."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        import ctypes.wintypes
        bcrypt = ctypes.WinDLL("bcrypt.dll")
        buffer = ctypes.create_string_buffer(size)
        status = bcrypt.BCryptGenRandom(None, buffer, size, 2)  # BCRYPT_USE_SYSTEM_PREFERRED_RNG
        if status != 0:
            return False
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(buffer.raw)
        return True
    except (AttributeError, OSError):
        return False


def run_collectors(size: int, output_dir: Path) -> dict[str, dict]:
    source_results: dict[str, dict] = {}
    urandom = output_dir / "urandom.bin"
    openssl = output_dir / "openssl.bin"

    if generate_via_dev_urandom(size, urandom):
        source_results["Linux /dev/urandom"] = analyze(urandom.read_bytes())

    if generate_via_openssl(size, openssl):
        source_results["OpenSSL rand"] = analyze(openssl.read_bytes())

    cng = output_dir / "windows_cng.bin"
    if generate_via_windows_cng(size, cng):
        source_results["Windows CNG API"] = analyze(cng.read_bytes())

    return source_results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bytes", type=int, default=1024 * 1024, help="Bytes to generate for each source")
    args = parser.parse_args()

    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    results = run_collectors(args.bytes, output_dir)
    report = format_report(results)
    print(report)
    (output_dir / "results.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
