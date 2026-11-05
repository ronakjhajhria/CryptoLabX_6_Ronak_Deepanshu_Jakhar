# Operating-System Cryptographic Random-Number Analysis

This lab collects at least 1 MB from each available operating-system CSPRNG source, analyzes its byte and bit distributions, and performs bounded statistical tests.

## Sources

- **Linux `/dev/urandom`** — On Linux, the collector reads `/dev/urandom` directly. On Windows with WSL installed, it calls WSL's Linux `/dev/urandom`.
- **OpenSSL `rand` utility** — Generates bytes through `openssl rand`.
- **Windows CNG API** — The collector calls the native Windows CNG `BCryptGenRandom` function using `BCRYPT_USE_SYSTEM_PREFERRED_RNG`.

## Run

```powershell
.\.venv\Scripts\python.exe modern\os_random_analysis\src\os_random_analysis.py --bytes 1048576
```

The generated `.bin` files and Markdown report are saved under `outputs/`.

## Analysis

The program reports:

- 256-bin byte-frequency chi-square statistic
- Zero/one bit counts and one-bit ratio
- Monobit test approximate z-score
- Runs count and approximate z-score
- Lag-1 byte serial correlation
- 16-byte block repetition and uniqueness
- Shannon entropy over bytes

The tests are intended for demonstration; they do not replace a complete third-party statistical suite. A source can pass these tests while remaining weak or predictable, for example if it were a fixed generator with good short-range distributions. A source is cryptographically suitable based on its design, entropy inputs, state protection, implementation validation, and resistance to prediction—not because statistics are favorable.

## Linux and Windows Randomness

Linux exposes `/dev/urandom` as a non-blocking userspace interface backed by the kernel CSPRNG. Kernel entropy sources include interrupts, device timing, disks, and hardware RNGs where available. Initialization blocks random devices initially when needed; modern systems continually mix entropy and reseed the CSPRNG. `/dev/random` historically differed by blocking for entropy; `/dev/urandom` is intended for normal random use on modern Linux.

Windows CNG provides cryptographic entropy through APIs such as `BCryptGenRandom` and the higher-level .NET `RandomNumberGenerator.GetBytes`. This assignment calls `BCryptGenRandom` directly with `BCRYPT_USE_SYSTEM_PREFERRED_RNG`. Internally Windows combines OS entropy sources, hardware RNG support, and kernel RNG state to expose a CSPRNG-backed interface. Applications should use BCrypt/CNG or the equivalent .NET API, not statistical PRNGs such as MT19937.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s modern\os_random_analysis\testcases -p "test_*.py"
```
