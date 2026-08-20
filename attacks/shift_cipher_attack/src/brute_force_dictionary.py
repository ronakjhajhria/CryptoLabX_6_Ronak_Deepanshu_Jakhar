import re

from shift_cipher import decrypt


def load_dictionary(filename):
    words = set()

    with open(filename, "r") as file:
        for line in file:
            word = line.strip().upper()

            if word:
                words.add(word)

    return words


def dictionary_score(text, dictionary):
    words = re.findall(r"[A-Za-z]+", text.upper())

    score = 0

    for word in words:
        if word in dictionary:
            score += 1

    return score


def brute_force_attack(ciphertext, dictionary):
    results = []

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = dictionary_score(plaintext, dictionary)

        results.append((score, key, plaintext))

    results.sort(reverse=True)

    return results


if __name__ == "__main__":
    dictionary_file = "dictionary/english_words.txt"

    dictionary = load_dictionary(dictionary_file)

    ciphertext = "KHOOR ZRUOG"

    results = brute_force_attack(ciphertext, dictionary)

    print("Possible plaintexts:")
    print()

    for score, key, plaintext in results:
        print(
            f"Key = {key:2d} | "
            f"Score = {score:2d} | "
            f"Plaintext = {plaintext}"
        )





















