# AES-CBC Padding Oracle Lab

This lab demonstrates how an attacker can recover plaintext from AES-CBC ciphertext when a service reveals whether decrypted data has valid PKCS#7 padding. It includes a local encryption fixture, a simulated boolean oracle, and an attack that uses only the IV, ciphertext, and oracle callback.

> **Scope:** This educational demonstration is for local, authorized use only. Do not use it against systems or ciphertext without permission. The example intentionally exposes a vulnerable padding signal and is not a secure encryption design.

## Quick Start

From the repository root, install dependencies and run the demo:

```shell
python -m pip install -r requirements.txt
python attacks/padding_oracle_attack/src/padding_oracle_attack.py
```

Supply a different UTF-8 message with `--plaintext`:

```shell
python attacks/padding_oracle_attack/src/padding_oracle_attack.py --plaintext "Try another message."
```

The program prints the recovered plaintext and the number of oracle queries. Query counts vary because the key and IV are generated randomly for each run.

## PKCS#7 Helpers

`pad_pkcs7(data)` pads bytes to an AES block boundary. A complete 16-byte padding block is added when the input is already aligned. `unpad_pkcs7(data)` returns the original bytes and raises `ValueError` for empty, malformed, or non-block-aligned input.

## How the Attack Works

For AES-CBC, decryption combines the AES inverse of the ciphertext block with the preceding ciphertext block:

```text
P_i = AES_K^-1(C_i) XOR C_(i-1)
```

For the first plaintext block, `C_(i-1)` is the IV. The attack changes bytes in the preceding block and uses the padding responses to recover the final plaintext byte of each block, then repeats from right to left. Padding always contains between one and sixteen bytes equal to the pad length; an exactly aligned plaintext receives a full padding block.

The recovery function accepts an oracle with this interface:

```python
oracle(candidate_iv: bytes, candidate_ciphertext: bytes) -> bool
```

`recover_plaintext(iv, ciphertext, oracle)` returns the recovered plaintext and total oracle-query count. It does not receive the AES key; the local key is held by the demo oracle.

## Tests

Run the focused test suite from the repository root:

```shell
python -m unittest discover -s attacks/padding_oracle_attack/testcases -p "test_*.py"
```

The tests cover PKCS#7 boundaries, malformed padding and ciphertext, multi-block recovery, and oracle-query accounting.

## Prevention

Do not reveal distinguishable padding errors. Prefer authenticated encryption such as AES-GCM or ChaCha20-Poly1305. If CBC must be used, apply encrypt-then-MAC with a strong MAC, authenticate the IV and ciphertext, and verify the MAC in constant time before decryption or padding validation. Return uniform errors and avoid side channels that reveal padding validity.
