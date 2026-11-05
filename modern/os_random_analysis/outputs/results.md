# Operating-System Cryptographic Random-Number Analysis

| Source | Bytes | Chi-square | Byte uniformity | One-bit ratio | Monobit z | Runs z | Lag-1 correlation | Unique/Total 16-byte blocks | Shannon entropy |
|---|---:|---:|:---:|---:|---:|---:|---:|---:|---:|
| Linux /dev/urandom | 1048576 | 252.23 | PASS | 0.500107 | 0.6201 | 0.3431 | -0.00087558 | 65536/65536 | 7.999826 |
| OpenSSL rand | 1048576 | 271.42 | PASS | 0.500136 | 0.7858 | 0.0403 | 0.00161518 | 65536/65536 | 7.999813 |
| Windows CNG API | 1048576 | 231.60 | PASS | 0.499902 | 0.5676 | 0.1790 | 0.00018041 | 65536/65536 | 7.999841 |

## Interpretation
A byte chi-square below the reported 255-degree-of-freedom threshold and one-bit/runs ratios near their expected values support statistical randomness, not cryptographic security.
Serious repeated blocks are expected to remain rare over 1 MB; these counts are not proof of independence.
The monobit and runs tests are bounded examples, not a replacement for the full NIST or Dieharder suites.