#include <bits/stdc++.h>

using namespace std;

string clean_ciphertext(const string& text) {
    string result;
    for (char c : text) {
        if (isalpha(c)) {
            result += toupper(c);
        }
    }
    return result;
}

vector<string> find_repeated_patterns(const string& text) {
    vector<string> patterns;
    for (int len = 3; len <= 5; len++) {
        map<string, vector<int>> positions;
        for (size_t i = 0; i + len <= text.size(); i++) {
            positions[text.substr(i, len)].push_back(i);
        }
        for (const auto& p : positions) {
            if (p.second.size() > 1) {
                patterns.push_back(p.first);
            }
        }
    }
    return patterns;
}

vector<int> calculate_distances(const string& text, const string& pattern) {
    vector<int> positions;
    for (size_t i = 0; i + pattern.size() <= text.size(); i++) {
        if (text.substr(i, pattern.size()) == pattern) {
            positions.push_back(i);
        }
    }
    
    // Pairwise distance calculation
    vector<int> distances;
    for (size_t i = 0; i < positions.size(); i++) {
        for (size_t j = i + 1; j < positions.size(); j++) {
            distances.push_back(positions[j] - positions[i]);
        }
    }
    return distances;
}

vector<int> find_factors(int distance) {
    vector<int> factors;
    for (int i = 2; i <= 20; i++) {
        if (distance % i == 0) {
            factors.push_back(i);
        }
    }
    return factors;
}

double calculate_ic(const string& text) {
    if (text.size() < 2) return 0.0;
    vector<int> freq(26, 0);
    for (char c : text) freq[c - 'A']++;

    double numerator = 0;
    for (int x : freq) numerator += x * (x - 1);
    double denominator = text.size() * (text.size() - 1);

    return numerator / denominator;
}

vector<int> kasiski_analysis(const string& text) {
    vector<string> patterns = find_repeated_patterns(text);
    map<int, int> factorCount;

    for (const string& pattern : patterns) {
        vector<int> distances = calculate_distances(text, pattern);
        for (int distance : distances) {
            vector<int> factors = find_factors(distance);
            for (int factor : factors) {
                factorCount[factor]++;
            }
        }
    }

    vector<pair<int, int>> candidates;
    for (const auto& p : factorCount) {
        candidates.push_back({p.second, p.first});
    }
    sort(candidates.rbegin(), candidates.rend());

    vector<int> result;
    for (size_t i = 0; i < candidates.size() && i < 10; i++) {
        result.push_back(candidates[i].second);
    }
    return result;
}

vector<string> split_into_groups(const string& text, int keyLength) {
    vector<string> groups(keyLength);
    for (size_t i = 0; i < text.size(); i++) {
        groups[i % keyLength] += text[i];
    }
    return groups;
}

vector<int> frequency_analysis(const string& group) {
    vector<int> freq(26, 0);
    for (char c : group) freq[c - 'A']++;
    return freq;
}

int find_shift(const string& group) {
    static const double english[26] = {
        0.082, 0.015, 0.028, 0.043, 0.127,
        0.022, 0.020, 0.061, 0.070, 0.0015,
        0.0077, 0.040, 0.024, 0.0675, 0.075,
        0.019, 0.00095, 0.060, 0.063, 0.091,
        0.028, 0.0098, 0.024, 0.0015, 0.020,
        0.00074
    };

    vector<int> freq = frequency_analysis(group);
    double bestScore = 1e18;
    int bestShift = 0;

    for (int shift = 0; shift < 26; shift++) {
        double score = 0;
        for (int i = 0; i < 26; i++) {
            int cipherIndex = (i + shift) % 26;
            double expected = group.size() * english[i];
            double observed = freq[cipherIndex];

            if (expected > 0) {
                score += (observed - expected) * (observed - expected) / expected;
            }
        }

        if (score < bestScore) {
            bestScore = score;
            bestShift = shift;
        }
    }
    return bestShift;
}

string find_key(const vector<string>& groups) {
    string key;
    for (const string& group : groups) {
        int shift = find_shift(group);
        key += char('A' + shift);
    }
    return key;
}

string vigenere_decrypt(const string& ciphertext, const string& key) {
    string plaintext;
    for (size_t i = 0; i < ciphertext.size(); i++) {
        int c = ciphertext[i] - 'A';
        int k = key[i % key.size()] - 'A';
        int p = (c - k + 26) % 26;
        plaintext += char('A' + p);
    }
    return plaintext;
}

string vigenere_encrypt(const string& plaintext, const string& key) {
    string ciphertext;
    for (size_t i = 0; i < plaintext.size(); i++) {
        int p = plaintext[i] - 'A';
        int k = key[i % key.size()] - 'A';
        int c = (p + k) % 26;
        ciphertext += char('A' + c);
    }
    return ciphertext;
}

bool verify(const string& original, const string& encrypted) {
    return original == encrypted;
}

void print_frequency_table(const vector<string>& groups) {
    for (size_t i = 0; i < groups.size(); i++) {
        vector<int> freq = frequency_analysis(groups[i]);
        cout << "\nGroup " << i + 1 << "\n-------------------------\n";
        for (int j = 0; j < 26; j++) {
            cout << char('A' + j) << " : " << freq[j] << "\n";
        }
    }
}

int main() {
    string raw_ciphertext = R"(QRBAI UWYOK ILBRZ XTUWL EGXSN VDXWR XMHXY FCGMW
WWSME LSXUZ MKMFS BNZIF YEIEG RFZRX WKUFA XQEDX DTTHY NTBRJ
LHTAI KOCZX QHBND ZIGZG PXARJ EDYSJ NUMKI FLBTN HWISW NVLFM
EGXAI AAWSL FMHXR SGRIG HEQTU MLGLV BRSIL AEZSG XCMHT OWHFM
LWMRK HPRFB ELWGF RUGPB HNBEM KBNVW HHUEA KILBN BMLHK XUGML
YQKHP RFBEL EJYNV WSIJB GAXGO TPMXR TXFKI WUALB RGWIE GHWHG
AMEWW LTAEL NUMRE UWTBL SDPRL YVRET LEEDF ROBEQ UXTHX ZYOZB
XLKAC KSOHN VWXKS MAEPH IYQMM FSECH RFYPB BSQTX TPIWH GPXQD
FWTAI KNNBX SIYKE TXTLV BTMQA LAGHG OTPMX RTXTH XSFYG WMVKH
LOIVU ALMLD LTSYV WYNVW MQVXP XRVYA BLXDL XSMLW SUIOI IMELI
SOYEB HPHNR WTVUI AKEYG WIETG WWBVM VDUMA EPAUA KXWHK MAUPA
MUKHQ PWKCX EFXGW WSDDE OMLWL NKMWD FWTAM FAFEA MFZBN WIHYA
LXRWK MAMIK GNGHJ UAZHM HGUAL YSULA ELYHJ BZMSI LAILH WWYIK
EWAHN PMLBN NBVPJ XLBEF WRWGX KWIRH XWWGQ HRRXW IOMFY CZHZL
VXNVI OYZCM YDDEY IPWXT MMSHS VHHXZ YEWNV OAOEL SMLSW KXXFX
STRVI HZLEF JXDAS FIE)";

    string ciphertext = clean_ciphertext(raw_ciphertext);

    cout << "=============================================\n";
    cout << " VIGENERE CIPHER CRYPTANALYSIS\n";
    cout << "=============================================\n";
    cout << "Ciphertext length: " << ciphertext.size() << "\n";

    vector<int> candidates = kasiski_analysis(ciphertext);
    
    // Programmatic key length estimation via maximum Index of Coincidence
    int bestKeyLength = candidates[0];
    double maxIC = 0.0;

    cout << "\nIndex of Coincidence Analysis:\n";
    for (int keyLength : candidates) {
        vector<string> groups = split_into_groups(ciphertext, keyLength);
        double totalIC = 0;
        for (const string& group : groups) {
            totalIC += calculate_ic(group);
        }
        double avgIC = totalIC / keyLength;
        cout << "Key Length " << keyLength << " -> Avg IC = " << avgIC << "\n";

        if (avgIC > maxIC) {
            maxIC = avgIC;
            bestKeyLength = keyLength;
        }
    }

    cout << "\n=============================================\n";
    cout << "Estimated Key Length: " << bestKeyLength << "\n";
    cout << "=============================================\n";

    vector<string> groups = split_into_groups(ciphertext, bestKeyLength);
    print_frequency_table(groups);

    // Dynamic key recovery via chi-squared frequency analysis
    string key = find_key(groups);

    cout << "\nRecovered Key: " << key << "\n";

    string plaintext = vigenere_decrypt(ciphertext, key);

    cout << "\n=============================================\n";
    cout << "Recovered Plaintext\n";
    cout << "=============================================\n";
    cout << plaintext << "\n";

    string encrypted = vigenere_encrypt(plaintext, key);

    cout << "\n=============================================\n";
    cout << "Verification\n";
    cout << "=============================================\n";

    if (verify(ciphertext, encrypted)) {
        cout << "SUCCESS: Re-encrypted ciphertext matches original.\n";
    } else {
        cout << "FAILED: Verification mismatch.\n";
    }

    return 0;
}