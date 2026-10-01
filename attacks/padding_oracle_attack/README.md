# AES-CBC Padding Oracle Lab

This lab demonstrates how an attacker can recover plaintext from AES-CBC ciphertext when a service reveals whether the decrypted data has valid PKCS#7 padding. It includes a local encryption fixture, a simulated boolean oracle, and an attack that uses only the IV, ciphertext, and oracle callback.

> **Scope:** This is an educational demonstration for local, authorized use. Do not use the attack against systems or ciphertexts without permission. The example intentionally exposes a vulnerable padding signal and is not a secure encryption design.

## Quick Start

From the repository root, install the dependency and run the demo:

```shell
python -m pip install -r requirements.txt
python attacks/padding_oracle_attack/src/padding_oracle.py
```

Supply a different UTF-8 message with `--plaintext`:

```shell
python attacks/padding_oracle_attack/src/padding_oracle.py --plaintext "Try another message."
```

The program prints the recovered plaintext and the number of oracle queries. Query counts vary because the key and IV are generated randomly for each run.

## PKCS#7 Helpers

`pad_pkcs7(data)` pads bytes to an AES block boundary. A complete 16-byte padding block is added when the input is already aligned. `unpad_pkcs7(data)` returns the original bytes and raises `ValueError` if the input is empty, not block-aligned, or has invalid padding.

To try the helpers interactively, start Python from the source directory:

```shell
cd attacks/padding_oracle_attack/src
python
```

```python
from padding_oracle import pad_pkcs7, unpad_pkcs7

padded = pad_pkcs7(b"hello")
print(unpad_pkcs7(padded))  # b'hello'
```

## How the Attack Works

For each AES-CBC block, decryption combines the AES inverse of the ciphertext block with the preceding ciphertext block. For the first plaintext block, the IV is used as the preceding block:

```text
C_i = AES_K(P_i XOR C_(i-1))
P_i = AES_K^-1(C_i) XOR C_(i-1)
```

Changing a byte in the preceding block changes the matching decrypted byte by the same XOR difference. The attack uses this property to make the final bytes of a target block look like `01`, then `02 02`, and so on. It tries candidate byte values against the oracle, recovers each block from right to left, and removes the final PKCS#7 padding.

The simulated oracle returns `True` for valid padding and `False` otherwise. The recovery function accepts an oracle with this interface:

```python
oracle(candidate_iv: bytes, candidate_ciphertext: bytes) -> bool
```

Call `recover_plaintext(iv, ciphertext, oracle)` with one 16-byte IV and one or more complete ciphertext blocks. It returns an `AttackResult` containing the recovered `plaintext` and total `oracle_queries`. The attack function itself does not receive the AES key; the local key is held by the demo oracle.

## Tests

Run the focused test suite from the repository root:

```shell
python -m unittest discover -s attacks/padding_oracle_attack/testcases -p "test_*.py"
```

Tests cover PKCS#7 padding boundaries, malformed padding and ciphertext, multi-block recovery, and oracle-query accounting.

## Prevention

Do not reveal distinguishable padding errors. More importantly, authenticate ciphertext before CBC decryption or padding validation, using encrypt-then-MAC with a strong MAC and constant-time verification. Prefer authenticated encryption such as AES-GCM or ChaCha20-Poly1305. Return uniform errors for authentication failures; hiding error text alone is not enough if timing or other behavior still reveals padding validity.