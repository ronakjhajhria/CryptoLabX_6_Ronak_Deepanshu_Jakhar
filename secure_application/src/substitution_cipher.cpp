#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <cctype>
#include <iomanip>

using namespace std;

// 1. Encryption Function
string encryptText(const string& text, const string& key)
{
    string result;
    for (char ch : text)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            bool upper = isupper(static_cast<unsigned char>(ch));
            char encrypted = key[toupper(static_cast<unsigned char>(ch)) - 'A'];

            if (!upper)
                encrypted = tolower(static_cast<unsigned char>(encrypted));

            result += encrypted;
        }
        else
        {
            result += ch;
        }
    }
    return result;
}

// 2. Letter Frequency Analysis
void frequency_analysis(const string& text)
{
    map<char, int> frequency;
    int totalLetters = 0;

    for (char ch : text)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            char c = toupper(static_cast<unsigned char>(ch));
            frequency[c]++;
            totalLetters++;
        }
    }

    vector<pair<char, int>> data(frequency.begin(), frequency.end());
    sort(data.begin(), data.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
        return a.second > b.second;
    });

    cout << "\n=================== LETTER FREQUENCY ANALYSIS ===================\n";
    cout << left << setw(10) << "Letter" << setw(10) << "Count" << "Percentage\n";
    cout << "-----------------------------------------------------------------\n";

    for (const auto& p : data)
    {
        double percentage = (100.0 * p.second) / totalLetters;
        cout << left << setw(10) << p.first
             << setw(10) << p.second
             << fixed << setprecision(2) << percentage << "%\n";
    }

    if (!data.empty())
    {
        cout << "\nMost frequent letters in Ciphertext: ";
        for (size_t i = 0; i < min<size_t>(5, data.size()); ++i)
        {
            cout << data[i].first << " (" << data[i].second << ")  ";
        }
        cout << "\n";
    }
}

// Helper to extract words
vector<string> getWords(const string& text)
{
    vector<string> words;
    string word;

    for (char ch : text)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            word += tolower(static_cast<unsigned char>(ch));
        }
        else if (!word.empty())
        {
            words.push_back(word);
            word.clear();
        }
    }
    if (!word.empty())
        words.push_back(word);

    return words;
}

// 3. Word Frequency Analysis
void word_frequency_analysis(const string& text)
{
    vector<string> words = getWords(text);
    map<string, int> frequency;

    for (const string& word : words)
        frequency[word]++;

    cout << "\n===================== WORD FREQUENCY ANALYSIS =====================\n";

    cout << "\nRepeated Words (Count > 1):\n";
    for (const auto& p : frequency)
    {
        if (p.second > 1)
            cout << "  " << left << setw(15) << p.first << ": " << p.second << "\n";
    }

    cout << "\nOne-letter words:\n";
    for (const auto& p : frequency)
    {
        if (p.first.length() == 1)
            cout << "  " << p.first << " (" << p.second << ")\n";
    }

    cout << "\nTwo-letter words:\n";
    for (const auto& p : frequency)
    {
        if (p.first.length() == 2)
            cout << "  " << p.first << " (" << p.second << ")\n";
    }

    cout << "\nThree-letter words:\n";
    for (const auto& p : frequency)
    {
        if (p.first.length() == 3)
            cout << "  " << p.first << " (" << p.second << ")\n";
    }
}

// Pattern generator
string getPattern(const string& word)
{
    map<char, char> mapping;
    string pattern = "";
    char nextChar = 'A';

    for (char ch : word)
    {
        char lowerCh = tolower(static_cast<unsigned char>(ch));
        if (mapping.find(lowerCh) == mapping.end())
        {
            mapping[lowerCh] = nextChar++;
        }
        pattern += mapping[lowerCh];
    }
    return pattern;
}

// 4. Pattern Analysis
void pattern_analysis(const string& text)
{
    vector<string> words = getWords(text);
    map<string, set<string>> patterns;

    for (const string& word : words)
    {
        if (word.length() >= 3)
        {
            patterns[getPattern(word)].insert(word);
        }
    }

    cout << "\n======================= PATTERN ANALYSIS =======================\n";
    for (const auto& p : patterns)
    {
        if (p.second.size() > 1)
        {
            cout << "Pattern [" << left << setw(8) << p.first << "] matches: ";
            for (const string& word : p.second)
                cout << word << " ";
            cout << "\n";
        }
    }
}

// 5. Apply Substitution
string apply_substitution(const string& cipherText, const string& substitution)
{
    string result;
    for (char ch : cipherText)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            bool upper = isupper(static_cast<unsigned char>(ch));
            char mapped = substitution[toupper(static_cast<unsigned char>(ch)) - 'A'];

            if (mapped == '?')
            {
                result += '_';
            }
            else
            {
                if (!upper)
                    mapped = tolower(static_cast<unsigned char>(mapped));
                result += mapped;
            }
        }
        else
        {
            result += ch;
        }
    }
    return result;
}

// 6. Display Partial Plaintext
void display_partial_plaintext(const string& cipherText, const string& substitution)
{
    cout << "\n====================== PARTIAL PLAINTEXT ======================\n";
    cout << apply_substitution(cipherText, substitution) << "\n";
}

// 7. Verification Function
bool verify_solution(const string& plaintext, const string& ciphertext, const string& key)
{
    return encryptText(plaintext, key) == ciphertext;
}

int main()
{
    // Exact Text from Page 36 ("Modern Cryptography" - Katz & Lindell)
    string plaintext =
        "We conclude that perfect secrecy is attainable. Unfortunately, the one-time pad encryption "
        "scheme has a number of drawbacks. Most prominent is that the key is required to be as long "
        "as the message. First and foremost, this means that a long key must be securely stored, "
        "something that is highly problematic in practice and often not achievable. In addition, "
        "this limits applicability of the scheme if we want to send very long messages or if we "
        "don't know in advance an upper bound on how long the message will be. Moreover, the "
        "one-time pad scheme is only secure if used once with the same key. Although we did not "
        "yet define a notion of security when multiple messages are encrypted, it is easy to see "
        "informally that encrypting more than one message leaks a lot of information. In particular, "
        "say two messages m and m' are encrypted using the same key k. An adversary who obtains c and c' "
        "can compute their XOR and learn something about the exclusive-or of the two messages. While "
        "this may not seem very significant, it is enough to rule out any claims of perfect secrecy "
        "when encrypting two messages. Limitations of Perfect Secrecy: In this section, we show "
        "that the aforementioned limitations of the one-time pad encryption scheme are inherent. "
        "Specifically, we prove that any perfectly-secret encryption scheme must have a key space "
        "that is at least as large as the message space.";

    string key = "QWERTYUIOPASDFGHJKLZXCVBNM";
    string ciphertext = encryptText(plaintext, key);

    cout << "=================== MONOALPHABETIC CIPHER ANALYZER ===================\n";
    cout << "\n--- Plaintext (Page 36) ---\n" << plaintext << "\n";
    cout << "\n--- Ciphertext ---\n" << ciphertext << "\n";

    // Run Cryptanalysis Modules
    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    // Initial Known Step Demonstration
    string candidateSub(26, '?');
    candidateSub['T' - 'A'] = 'E'; // T -> e
    candidateSub['Z' - 'A'] = 'T'; // Z -> t
    candidateSub['I' - 'A'] = 'H'; // I -> h

    cout << "\n--- Sample Candidate Hypotheses Applied (T->e, Z->t, I->h) ---\n";
    display_partial_plaintext(ciphertext, candidateSub);

    return 0;
}