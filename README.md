# CryptoLabX

## Cryptography Laboratory Toolkit

CryptoLabX is a modular cryptanalysis toolkit developed as part of the
Cryptography Laboratory (22CPP307). The project is designed to gradually
grow into a complete framework for studying classical cryptography,
cryptanalysis attacks, mathematical techniques, modern cryptography,
and security analysis.

## Team Members

- Ronak Jhajhria -> 2024ucp1538
- Deepanshu Jakhar -> 2024ucp1743

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