from datetime import datetime
from collections import Counter
import os


# Create output folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)


while True:

    print("\n==============================")
    print("       CryptoLabX Toolkit")
    print("==============================")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")
    print("==============================")

    choice = input("Enter your choice: ")

    # Save choice in log file
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("outputs/cryptolabx.log", "a") as log:
        log.write(f"{time} - Selected option: {choice}\n")


    # Encrypt
    if choice == "1":
        print("\nEncryption: Coming Soon")


    # Decrypt
    elif choice == "2":
        print("\nDecryption: Coming Soon")


    # Attack
    elif choice == "3":
        print("\nAttack: Coming Soon")


    # Analyze
    elif choice == "4":

        print("\nFiles available in datasets:")

        files = os.listdir("datasets")

        for i, file in enumerate(files):
            print(i + 1, ".", file)

        number = int(input("\nSelect file number: "))

        filename = files[number - 1]

        path = "datasets/" + filename

        with open(path, "r") as file:
            text = file.read()

        characters = len(text)
        words = len(text.split())
        lines = len(text.splitlines())
        unique = len(set(text))

        frequency = Counter(text.lower())

        print("\n==============================")
        print("        FILE ANALYSIS")
        print("==============================")

        print("File:", filename)
        print("Characters:", characters)
        print("Words:", words)
        print("Lines:", lines)
        print("Unique Characters:", unique)

        print("\nLetter Frequency:")

        for letter in sorted(frequency):

            if letter.isalpha():
                print(letter, ":", frequency[letter])


    # Exit
    elif choice == "5":

        print("\nThank you for using CryptoLabX!")
        break


    # Wrong choice
    else:

        print("\nInvalid choice!")