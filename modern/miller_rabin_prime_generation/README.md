# Cryptographic Prime Generation Using Miller-Rabin

This lab generates a probable prime with exactly 512 bits. It uses Python's cryptographically secure `secrets` module to produce random odd candidates and a custom Miller-Rabin implementation with multiple random bases.

## Run

From the repository root:

```powershell
.\.venv\Scripts\python.exe modern\miller_rabin_prime_generation\src\miller_rabin_prime.py --bits 512 --rounds 40
```

The default parameters generate a 512-bit candidate using 40 rounds. The program prints and saves a Markdown table to `outputs/results.txt`.

## Miller-Rabin Method

Given an odd candidate `n`, write `n - 1 = 2^s * d`, where `d` is odd. For each base `a`:

```text
x = a^d mod n
if x == 1 or x == n - 1:
    continue to next base
repeat s - 1 times:
    x = x^2 mod n
    if x == n - 1:
        continue to next base
return composite
return probable prime
```

The implementation repeats for 40 random bases in the usual range `2 <= a < n - 1`. This makes accidental composite acceptance negligible, but Miller-Rabin remains a probable-prime test rather than a mathematical deterministic proof for arbitrary 512-bit values.

## Independent Verification

The final candidate is verified by both:

1. The custom Miller-Rabin implementation with 40 or more specified bases.
2. The independent SymPy `isprime()` library function.

SymPy is listed in `requirements.txt`; it is not used during candidate generation.

## Experimental Output

The run reports:

| Parameter | Meaning |
|---|---|
| Assigned bit length | Requested number of candidate bits |
| Generated prime candidate | Final decimal probable prime |
| Actual bit length | Verified with `candidate.bit_length()` |
| Candidates tested | Number of odd values submitted to Miller-Rabin |
| Miller-Rabin rounds | Random bases tested for each candidate |
| Execution time | Wall-clock generation time |

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s modern\miller_rabin_prime_generation\testcases -p "test_*.py"
```
