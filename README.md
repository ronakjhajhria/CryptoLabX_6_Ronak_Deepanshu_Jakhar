# CryptoLabX

## Cryptography Laboratory Toolkit

CryptoLabX is a modular cryptanalysis toolkit developed as part of the
Cryptography Laboratory (22CPP307). The project is designed to gradually
grow into a complete framework for studying classical cryptography,
cryptanalysis attacks, mathematical techniques, modern cryptography,
and security analysis.

## Project Details

- **Students Name & Roll Number:**
  - Ronak Jhajhria (2024ucp1538)
  - Deepanshu Jakhar (2024ucp1743)
- **Assigned Application:** CryptoLabX Toolkit
- **Programming Language:** Python
- **SAST Tool:** Semgrep

## Lab Progress Checklist

- [x] Week 1: Project Setup and Modular Structure
- [x] Week 2: SAST Tool Configuration and Analysis (Semgrep)
- [x] Week 3: Cryptocurrency Wallet Application (Lab Assignment 3)



## Week 1 Objectives

The first version of CryptoLabX establishes the foundation of the toolkit.
The following features have been implemented:

- Modular project structure
- Git and GitHub version control
- Command-line interface
- File analysis
- Character and word counting
- Line counting
- Unique character counting
- Letter frequency analysis
- Execution logging
- Dataset management

No cryptographic algorithms are implemented in Week 1.

## Assignment 10: MT19937 Stream Cipher and Predictable Tokens

- Demonstration source: [analysis/mt19937_assignment.py](analysis/mt19937_assignment.py)
- Notebook: [docs/Assignment_10_MT19937.ipynb](docs/Assignment_10_MT19937.ipynb)
- Tests: [tests/test_mt19937_assignment.py](tests/test_mt19937_assignment.py)

Run the demonstration:

```powershell
.\.venv\Scripts\python.exe analysis\mt19937_assignment.py
```

Run the focused tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mt19937_assignment.py -q
```

The demonstration intentionally uses MT19937 with observable seeds to teach cryptographic weakness; it must not be used for real encryption or reset tokens.

## Miller-Rabin 512-bit Prime Generation

- Assignment implementation: [modern/miller_rabin_prime_generation/src/miller_rabin_prime.py](modern/miller_rabin_prime_generation/src/miller_rabin_prime.py)
- Instructions and experimental format: [modern/miller_rabin_prime_generation/README.md](modern/miller_rabin_prime_generation/README.md)
- Generated report: [modern/miller_rabin_prime_generation/outputs/results.txt](modern/miller_rabin_prime_generation/outputs/results.txt)

Run:

```powershell
.\.venv\Scripts\python.exe modern\miller_rabin_prime_generation\src\miller_rabin_prime.py --bits 512 --rounds 40
```

Run tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s modern\miller_rabin_prime_generation\testcases -p "test_*.py"
```

## Project Structure

```text
CryptoLabX/
│
├── classical/            # Classical cryptography algorithms
├── attacks/              # Cryptanalysis and attack techniques
├── math/                 # Mathematical utilities
├── modern/               # Modern cryptography modules
├── analysis/             # Cryptographic analysis tools
├── datasets/             # Input text datasets
├── outputs/              # Generated outputs and logs
├── docs/                 # Project documentation
├── tests/                # Test cases
├── utils/                # Utility functions
│
├── hashing/              # Future hashing-related modules
├── secure_application/   # Future secure application modules
│
├── main.py               # Main command-line interface
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies