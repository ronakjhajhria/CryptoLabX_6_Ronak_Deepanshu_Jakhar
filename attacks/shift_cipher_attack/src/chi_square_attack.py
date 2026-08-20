from shift_cipher import decrypt


ENGLISH_FREQUENCIES = {
    'A': 8.167,
    'B': 1.492,
    'C': 2.782,
    'D': 4.253,
    'E': 12.702,
    'F': 2.228,
    'G': 2.015,
    'H': 6.094,
    'I': 6.966,
    'J': 0.153,
    'K': 0.772,
    'L': 4.025,
    'M': 2.406,
    'N': 6.749,
    'O': 7.507,
    'P': 1.929,
    'Q': 0.095,
    'R': 5.987,
    'S': 6.327,
    'T': 9.056,
    'U': 2.758,
    'V': 0.978,
    'W': 2.360,
    'X': 0.150,
    'Y': 1.974,
    'Z': 0.074
}

def calculate_frequencies(text):
    frequencies = {}

    for letter in ENGLISH_FREQUENCIES:
        frequencies[letter] = 0

    total_letters = 0

    for ch in text.upper():
        if 'A' <= ch <= 'Z':
            frequencies[ch] += 1
            total_letters += 1

    if total_letters == 0:
        return frequencies

    for letter in frequencies:
        frequencies[letter] = (
            frequencies[letter] / total_letters
        ) * 100

    return frequencies

def chi_square_score(text):
    observed = calculate_frequencies(text)

    score = 0.0

    for letter in ENGLISH_FREQUENCIES:
        expected = ENGLISH_FREQUENCIES[letter]
        actual = observed[letter]

        score += ((actual - expected) ** 2) / expected

    return score

def chi_square_attack(ciphertext):
    results = []

    for key in range(26):
        plaintext = decrypt(ciphertext, key)

        score = chi_square_score(plaintext)

        results.append((score, key, plaintext))

    results.sort()

    return results


if __name__ == "__main__":
    ciphertext = "KHOOR ZRUOG"

    results = chi_square_attack(ciphertext)

    print("Chi-Square Results:")
    print()

    for score, key, plaintext in results:
        print(
            f"Key = {key:2d} | "
            f"Chi-Square = {score:.2f} | "
            f"Plaintext = {plaintext}"
        )