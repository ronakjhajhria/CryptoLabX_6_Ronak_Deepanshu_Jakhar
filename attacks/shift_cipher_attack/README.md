# Shift Cipher Cryptanalysis

## Purpose

This laboratory studies cryptanalysis of a monoalphabetic shift (Caesar) cipher using brute force, dictionary scoring, and Chi-Square analysis. The experiments use long English messages so frequency analysis has enough data.

## Shift Cipher

Encryption moves each alphabetic letter forward by a key from 0 through 25. Uppercase and lowercase letters retain their case; spaces, digits, and punctuation are unchanged. Decryption moves letters backward by the same key.

## Attacks

- **Brute force:** decrypt the ciphertext with every one of the 26 possible keys.
- **Dictionary scoring:** tokenize each candidate plaintext into words, count words found in `dictionary/english_words.txt`, and select the key with the highest score. The CLI displays every key, score, and plaintext.
- **Chi-Square:** count A-Z letters only, compare each candidate's observed percentages with standard English frequencies, and select the key with the lowest score. The CLI displays every candidate.

Dictionary scoring depends on vocabulary coverage. Chi-Square uses letter statistics and does not need word boundaries, but it is less reliable on short ciphertexts.

## Running the Programs

Run commands from the repository root:

```text
python attacks/shift_cipher_attack/src/main.py encrypt 3 "HELLO, World!"
python attacks/shift_cipher_attack/src/main.py decrypt 3 "KHOOR, Zruog!"
python attacks/shift_cipher_attack/src/main.py dictionary "KHOOR ZRUOG"
python attacks/shift_cipher_attack/src/main.py chi-square "KHOOR ZRUOG"
python attacks/shift_cipher_attack/src/main.py compare "Wklv oderudwrub ..."
```

The dictionary command accepts an alternate file with `--dictionary path/to/words.txt`. Keys outside the usual range are normalized by the cipher's modulo arithmetic.

## Test Cases and Experiments

`testcases/case1.json` through `case5.json` each record plaintext, the actual key, and ciphertext. They use keys 3, 7, 13, 19, and 23 and contain substantially longer English text than a short example such as `HELLO WORLD`.

Run the experiment and save its real result table to `outputs/results.txt`:

```text
python attacks/shift_cipher_attack/src/run_experiments.py
```

Run edge-case unit tests:

```text
python -m unittest discover -s attacks/shift_cipher_attack/testcases -p "test_*.py"
```

The tests cover key 0, key 25, mixed case, punctuation, spaces, empty input, round trips, and the requirement that both attacks produce 26 candidates.

## Why Longer Text Helps

Chi-Square compares observed and expected letter percentages. With very few letters, one unusual word can change the percentages substantially. A longer ciphertext gives the law of averages more opportunity to reveal the English distribution, so the correct key generally receives the lowest score.

## Possible Failure Cases

- Very short ciphertexts may not contain enough evidence for Chi-Square to choose correctly.
- A message in another language will not match English frequencies.
- Unusual writing, abbreviations, or many names can reduce dictionary scores.
- A small or incomplete dictionary can make the dictionary attack select a wrong key.
- Empty or nearly non-alphabetic text cannot provide useful frequency evidence.
