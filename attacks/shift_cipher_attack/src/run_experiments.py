import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from brute_force_dictionary import brute_force_attack, load_dictionary
from chi_square_attack import chi_square_attack
from shift_cipher import encrypt


BASE_DIR = Path(__file__).resolve().parent.parent
TESTCASE_DIR = BASE_DIR / "testcases"
DICTIONARY_FILE = BASE_DIR / "dictionary" / "english_words.txt"
OUTPUT_FILE = BASE_DIR / "outputs" / "results.txt"


def run_experiments():
    dictionary = load_dictionary(DICTIONARY_FILE)
    rows = []
    for testcase_file in sorted(TESTCASE_DIR.glob("case*.json")):
        testcase = json.loads(testcase_file.read_text(encoding="utf-8"))
        ciphertext = testcase["ciphertext"]
        if encrypt(testcase["plaintext"], testcase["key"]) != ciphertext:
            raise ValueError(f"Stored ciphertext does not match {testcase_file.name}")
        dictionary_results = brute_force_attack(ciphertext, dictionary)
        chi_results = chi_square_attack(ciphertext)
        dictionary_key = dictionary_results[0][1]
        chi_key = chi_results[0][1]
        rows.append((testcase_file.name, testcase["key"], dictionary_key, chi_key,
                     dictionary_key == testcase["key"], chi_key == testcase["key"]))

    header = "Test Case | Actual Key | Dictionary Key | Chi-Square Key | Dictionary Correct? | Chi-Square Correct?"
    separator = "-" * len(header)
    lines = [header, separator]
    for row in rows:
        lines.append(f"{row[0]:9} | {row[1]:10} | {row[2]:15} | {row[3]:14} | "
                     f"{str(row[4]):18} | {str(row[5])}")

    output = "\n".join(lines) + "\n"
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(output, encoding="utf-8")
    print(output, end="")
    return rows


if __name__ == "__main__":
    run_experiments()