import argparse
from pathlib import Path

from brute_force_dictionary import brute_force_attack, load_dictionary
from chi_square_attack import chi_square_attack
from shift_cipher import decrypt, encrypt


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DICTIONARY = BASE_DIR / "dictionary" / "english_words.txt"


def print_dictionary_results(results):
    print("Key | Dictionary Score | Plaintext")
    print("----+------------------+----------")
    for score, key, plaintext in results:
        print(f"{key:3d} | {score:16d} | {plaintext}")


def print_chi_square_results(results):
    print("Key | Chi-Square Score | Plaintext")
    print("----+------------------+----------")
    for score, key, plaintext in results:
        print(f"{key:3d} | {score:16.4f} | {plaintext}")


def run_dictionary(ciphertext, dictionary_path):
    dictionary = load_dictionary(dictionary_path)
    results = brute_force_attack(ciphertext, dictionary)
    print_dictionary_results(results)
    print(f"\nPredicted key: {results[0][1]}")
    return results


def run_chi_square(ciphertext):
    results = chi_square_attack(ciphertext)
    print_chi_square_results(results)
    print(f"\nPredicted key: {results[0][1]}")
    return results


def build_parser():
    parser = argparse.ArgumentParser(description="Shift cipher tools and attacks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encrypt_parser = subparsers.add_parser("encrypt", help="encrypt plaintext")
    encrypt_parser.add_argument("key", type=int)
    encrypt_parser.add_argument("text")

    decrypt_parser = subparsers.add_parser("decrypt", help="decrypt with a known key")
    decrypt_parser.add_argument("key", type=int)
    decrypt_parser.add_argument("text")

    attack_parser = subparsers.add_parser("dictionary", help="run dictionary attack")
    attack_parser.add_argument("ciphertext")
    attack_parser.add_argument("--dictionary", default=str(DEFAULT_DICTIONARY))

    chi_parser = subparsers.add_parser("chi-square", help="run chi-square attack")
    chi_parser.add_argument("ciphertext")

    compare_parser = subparsers.add_parser("compare", help="run and compare both attacks")
    compare_parser.add_argument("ciphertext")
    compare_parser.add_argument("--dictionary", default=str(DEFAULT_DICTIONARY))

    return parser


def main():
    args = build_parser().parse_args()

    if args.command == "encrypt":
        print(encrypt(args.text, args.key))
    elif args.command == "decrypt":
        print(decrypt(args.text, args.key))
    elif args.command == "dictionary":
        run_dictionary(args.ciphertext, args.dictionary)
    elif args.command == "chi-square":
        run_chi_square(args.ciphertext)
    else:
        dictionary_results = run_dictionary(args.ciphertext, args.dictionary)
        chi_results = run_chi_square(args.ciphertext)
        print("\nComparison")
        print(f"Dictionary key:  {dictionary_results[0][1]}")
        print(f"Chi-Square key:  {chi_results[0][1]}")


if __name__ == "__main__":
    main()