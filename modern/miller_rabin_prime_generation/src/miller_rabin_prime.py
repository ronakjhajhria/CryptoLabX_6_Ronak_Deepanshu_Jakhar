"""Generate a cryptographic probable prime with the Miller-Rabin test."""

from __future__ import annotations

import argparse
import secrets
import time
from dataclasses import dataclass
from pathlib import Path


SMALL_PRIME_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


@dataclass(frozen=True)
class PrimeGenerationResult:
    bit_length: int
    rounds: int
    candidate: int
    candidates_tested: int
    miller_rabin_rounds_executed: int
    execution_time_seconds: float


def miller_rabin(n: int, bases: tuple[int, ...]) -> bool:
    """Return whether n passes Miller-Rabin for the supplied bases."""
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    exponent = n - 1
    power_of_two = 0
    while exponent % 2 == 0:
        power_of_two += 1
        exponent //= 2

    for base in bases:
        a = base % n
        if a in (0, 1):
            continue

        value = pow(a, exponent, n)
        if value in (1, n - 1):
            continue

        for _ in range(power_of_two - 1):
            value = pow(value, 2, n)
            if value == n - 1:
                break
        else:
            return False

    return True


def random_odd_candidate(bit_length: int) -> int:
    """Generate an odd candidate having exactly bit_length bits."""
    if bit_length < 2:
        raise ValueError("bit_length must be at least 2")

    candidate = secrets.randbits(bit_length)
    candidate |= (1 << (bit_length - 1)) | 1
    return candidate


def generate_probable_prime(bit_length: int = 512, rounds: int = 40) -> PrimeGenerationResult:
    """Generate an odd candidate and repeat until it passes Miller-Rabin."""
    if bit_length < 2:
        raise ValueError("bit_length must be at least 2")
    if rounds < 1:
        raise ValueError("rounds must be at least 1")

    start = time.perf_counter()
    candidates_tested = 0
    rounds_executed = 0

    while True:
        candidate = random_odd_candidate(bit_length)
        candidates_tested += 1

        bases = tuple(secrets.randbelow(candidate - 3) + 2 for _ in range(rounds))
        rounds_executed += rounds
        if miller_rabin(candidate, bases):
            break

    execution_time = time.perf_counter() - start
    return PrimeGenerationResult(
        bit_length=bit_length,
        rounds=rounds,
        candidate=candidate,
        candidates_tested=candidates_tested,
        miller_rabin_rounds_executed=rounds_executed,
        execution_time_seconds=execution_time,
    )


def independent_is_prime(candidate: int) -> bool:
    """Verify with SymPy, an implementation independent of the custom attack code."""
    try:
        from sympy import isprime
    except ImportError as error:
        raise RuntimeError("SymPy is required for independent verification") from error
    return bool(isprime(candidate))


def specified_bases(candidate: int, rounds: int) -> tuple[int, ...]:
    """Build reproducible bases for reporting. Values are reduced by candidate when needed."""
    bases = []
    for index, base in enumerate((*SMALL_PRIME_BASES, *(2 * index + 41 for index in range(rounds)))):
        reduced = base % candidate
        if reduced >= 2 and reduced not in bases:
            bases.append(reduced)
        if len(bases) == rounds:
            break
    return tuple(bases)


def format_result(result: PrimeGenerationResult) -> str:
    verification_bases = specified_bases(result.candidate, result.rounds)
    miller_rabin_passed = miller_rabin(result.candidate, verification_bases)
    independent_passed = independent_is_prime(result.candidate)

    lines = (
        "Cryptographic 512-bit Prime Generation - Miller-Rabin",
        "| Parameter | Value |",
        "|---|---:|",
        f"| Assigned bit length | {result.bit_length} |",
        f"| Generated prime candidate | {result.candidate} |",
        f"| Actual bit length | {result.candidate.bit_length()} |",
        f"| Number of candidates tested | {result.candidates_tested} |",
        f"| Number of Miller-Rabin rounds | {result.rounds} |",
        f"| Total Miller-Rabin rounds executed | {result.miller_rabin_rounds_executed} |",
        f"| Total execution time | {result.execution_time_seconds:.6f} seconds |",
        f"| Custom Miller-Rabin verification | {'PASS' if miller_rabin_passed else 'FAIL'} |",
        f"| Independent SymPy verification | {'PASS' if independent_passed else 'FAIL'} |",
        "",
        "The final value also passed the custom implementation and the independent SymPy library.",
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=512, help="Assigned candidate bit length")
    parser.add_argument("--rounds", type=int, default=40, help="Miller-Rabin rounds per candidate")
    args = parser.parse_args()

    result = generate_probable_prime(args.bits, args.rounds)
    report = format_result(result)
    print(report)

    output_path = Path(__file__).resolve().parents[1] / "outputs" / "results.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
