# AES-CBC Padding Oracle Attack

This lab demonstrates recovery of an AES-CBC plaintext using only the IV, ciphertext, and a function that reports whether decrypted data has valid PKCS#7 padding. The attack code never receives or reads the AES key. The local key is used only by the encryption fixture and the simulated oracle.

## Concepts

AES-CBC encrypts each plaintext block after XOR with the preceding ciphertext block:

```text
C_i = AES_K(P_i XOR C_(i-1))
P_i = AES_K^-1(C_i) XOR C_(i-1)
```

For the first block, the IV takes the place of `C_(i-1)`. PKCS#7 fills the final block with `n` bytes each equal to `n`; a full block of padding is added when the input already ends on a block boundary. A padding oracle leaks one bit of information by distinguishing valid from invalid padding.

When the attacker changes a byte in the preceding block by XORing a difference `delta`, the corresponding decrypted byte changes by the same `delta`, because the block-cipher output for the target block has not changed:

```text
P'_i = AES_K^-1(C_i) XOR C'_(i-1)
```

The attack works from the last byte of each plaintext block to the first. It adjusts the previous block to induce padding values `01`, `02 02`, and so on, queries the oracle, and derives the intermediate AES decryption bytes. XORing those bytes with the original previous block reveals the plaintext. A confirmation query avoids mistaking a longer pre-existing valid padding suffix for the one-byte padding case.

## Run

Install the project dependency and run the demonstration from the repository root:

```text
python -m pip install -r requirements.txt
python attacks/padding_oracle_attack/src/padding_oracle.py
python attacks/padding_oracle_attack/src/padding_oracle.py --plaintext "A different message, not known to the attack."
```

For standalone padding, import `pad_pkcs7` and `unpad_pkcs7` from `padding_oracle.py`:

```python
from padding_oracle import pad_pkcs7, unpad_pkcs7

padded = pad_pkcs7(b"hello")
plaintext = unpad_pkcs7(padded)
```

`unpad_pkcs7` raises `ValueError` if the input is empty, not block-aligned, or has invalid padding.

The demo generates a fresh key and IV, encrypts the supplied message, then gives the attack only the IV, ciphertext, and oracle callback. It prints the recovered plaintext and actual number of oracle calls. The exact query count varies with the generated ciphertext. To use an existing ciphertext in a real exercise, call `recover_plaintext(iv, ciphertext, oracle)` with the provided data and an oracle callback implementing that exercise's interface.

Run tests with:

```text
python -m unittest discover -s attacks/padding_oracle_attack/testcases -p "test_*.py"
```

The tests check binary plaintexts around block boundaries, a complete padding-only block, multiple ciphertext blocks, and query-count accounting. No plaintext is assumed by the recovery function.

## Analysis and Prevention

The measured query count includes every boolean oracle call, including confirmation checks. Recovery is byte-by-byte: each byte requires up to 256 candidate queries, so the worst-case cost is approximately `256 * 16 * number_of_ciphertext_blocks`, plus confirmation queries. Average work is lower because candidates are tried sequentially and typically succeed partway through the range.

Never expose distinguishable padding errors. More importantly, authenticate ciphertext before attempting CBC decryption or padding validation, using encrypt-then-MAC with a strong MAC and constant-time verification. Prefer an authenticated-encryption mode such as AES-GCM or ChaCha20-Poly1305, and return uniform errors for all authentication failures. Hiding error text alone is insufficient if timing or other behavior still reveals padding validity.