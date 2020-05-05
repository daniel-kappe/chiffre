import os
from collections import Counter
from itertools import zip_longest, chain
from statistics import mean


import encrypt


UPPER_CASE_RANGE = (65, 91)
LETTER_RANGE = UPPER_CASE_RANGE[1] - UPPER_CASE_RANGE[0]
LOWER_CASE_OFFSET = 32
LETTER_FREQUENCIES_GER = {'E': 0.1740, 'N': 0.0978, 'I': 0.0755, 'S': 0.0727, 'R': 0.0700, 'A': 0.0651, 'T': 0.0615,
                          'D': 0.0508, 'H': 0.0476, 'U': 0.0435, 'L': 0.0344, 'C': 0.0306, 'G': 0.0301, 'M': 0.0253,
                          'O': 0.0251, 'B': 0.0189, 'W': 0.0189, 'F': 0.0166, 'K': 0.0121, 'Z': 0.0113, 'P': 0.0079,
                          'V': 0.0067, 'J': 0.0027, 'Y': 0.0004, 'X': 0.0003, 'Q': 0.0002}
LETTER_FREQUENCIES_ENG = {'E': 0.1270, 'T': 0.0956, 'A': 0.0818, 'O': 0.0751, 'I': 0.0697, 'N': 0.0675}
FREQUENT_GERMAN_WORDS = [
    "der", "die", "und", "in", "zu", "den", "das", "nicht", "von", "sie", "ist", "des", "sich", "mit",
    "dem", "dass", "er", "es", "ein", "ich", "auf", "so", "eine", "auch", "als", "an", "nach", "wie",
    "im", "für", "man", "aber", "aus", "durch", "wenn", "nur", "war", "noch", "werden", "bei", "hat",
    "wir", "was", "wird", "sein", "einen", "welche", "sind", "oder", "zur", "um", "haben", "einer",
    "mir", "über", "ihm", "diese", "einem", "ihr", "uns", "da", "zum", "kann", "doch", "vor", "dieser",
    "mich", "ihn", "du", "hatte", "seine", "mehr", "am", "denn", "nun", "unter", "sehr", "selbst", "schon",
    "hier", "bis", "habe", "ihre", "dann", "ihnen", "seiner", "alle", "wieder", "meine", "Zeit", "gegen",
    "vom", "ganz", "einzelnen", "wo", "muss", "ohne", "eines", "können", "sei"
]


def index_coincidence(in_string: str) -> float:
    r"""
        Calculates the Index of Coincidence see https://en.wikipedia.org/wiki/Index_of_coincidence

        Parameters
        ----------
        in_string: str
            The String to calculate the Index for.

        Returns
        -------
        float
            The Index of Coincidence for *in_string*
    """
    frequency = Counter(in_string)
    length = len(in_string)
    return sum(value * (value - 1) for value in frequency.values()) / (length * (length - 1)) * len(frequency.keys())


def caesar(in_string: str) -> tuple:
    r"""
        Takes a Caesar encrypted string and searches for the key.

        Parameters
        ----------
        in_string: str
            Caesar encrypted string. (German)

        Returns
        -------
        tuple
            A tuple containing the decrypted string and the key.
    """
    upper_string = in_string.upper()
    letter_statistics = Counter(upper_string)
    letter_statistics = {key: value / len(upper_string)
                         for key, value in sorted(letter_statistics.items(), key=lambda item: item[1], reverse=True)}
    shifts = [- ord(freq) + ord(stats) for freq, stats in zip(LETTER_FREQUENCIES_GER.keys(), letter_statistics.keys())]
    likiest_shift = sorted(Counter(shifts[:3]).items(), key=lambda item: item[1], reverse=True)[0][0]
    main_shift = chr(likiest_shift % LETTER_RANGE + UPPER_CASE_RANGE[0])
    back_shift = chr(- likiest_shift % LETTER_RANGE + UPPER_CASE_RANGE[0])
    return encrypt.caesar(in_string, back_shift), main_shift

def vigenere(in_string: str, max_key_length: int = 20) -> tuple:
    r"""
        Takes a Vigenere encrypted string and searches for the keyword.

        Parameters
        ----------
        in_string: str
            Vigenere encrypted string. (German)

        Returns
        -------
        tuple
            A tuple containing the decrypted string and the key.
    """
    upper_text = in_string.upper()
    coincidences = [mean(index_coincidence(upper_text[sid::idx]) for sid in range(idx))
                                                                 for idx in range(1, max_key_length)]
    shortest_likely = min(idx + 1 for idx, coincidence in enumerate(coincidences)
                                  if coincidence > max(coincidences) * 0.95)
    decrypted = [caesar(in_string[start::shortest_likely]) for start in range(shortest_likely)]
    message = [letters for letters in zip_longest(*[item[0] for item in decrypted], fillvalue='')]
    return (''.join(chain.from_iterable(message)), ''.join(item[1] for item in decrypted))


def scytale(in_string: str, max_block_length: int = 100) -> tuple:
    r"""
        Decrypts a german scytale text.

        Parameters
        ----------
        in_string: str
            Encrypted text.
        max_block_length: int
            Maximum block length to be tested.

        Returns
        -------
        tuple
            The decrypted text and the block length used.
    """
    bruteforce_tries = [encrypt.scytale(in_string, len(in_string) // block) for block in range(2, max_block_length)]
    common_word_hits_tries = [sum(btry.count(word) for word in FREQUENT_GERMAN_WORDS) for btry in bruteforce_tries]
    index_max_agree = common_word_hits_tries.index(max(common_word_hits_tries))
    return bruteforce_tries[index_max_agree], index_max_agree + 2


if __name__ == "__main__":
    with open("encrypted_scytale.txt", "r", encoding="utf8") as encrypted_scytale:
        scytale_text, scytale_key = scytale(encrypted_scytale.read())
    scytale_write_flag = "w" if os.path.isfile("decrypted_scytale.txt") else "x"
    with open("decrypted_scytale.txt", scytale_write_flag, encoding="utf8") as decrypted_scytale:
        decrypted_scytale.write(scytale_text)
    print(scytale_key)

    with open("encrypted_caesar.txt", "r", encoding="utf8") as encrypted_caesar:
        caesar_text, caesar_key = caesar(encrypted_caesar.read())
    caesar_write_flag = "w" if os.path.isfile("decrypted_caesar.txt") else "x"
    with open("decrypted_caesar.txt", caesar_write_flag, encoding="utf8") as decrypted_caesar:
        decrypted_caesar.write(caesar_text)
    print(caesar_key)

    with open("encrypted_vigenere.txt", "r", encoding="utf8") as encrypted_vigenere:
        text_encrypt = encrypted_vigenere.read()
        vigenere_text, vigenere_key = vigenere(text_encrypt)
    print(vigenere_key)
    vigenere_write_flag = "w" if os.path.isfile("decrypted_vigenere.txt") else "x"
    with open("decrypted_vigenere.txt", vigenere_write_flag, encoding="utf8") as decrypted_vigenere:
        decrypted_vigenere.write(vigenere_text)

    import matplotlib.pyplot as plt
    max_length = 50
    coins = [mean(index_coincidence(text_encrypt.upper()[sid::idx]) for sid in range(idx)) for idx in range(1, max_length)]
    plt.bar(range(1, max_length), coins, width=0.8)
    plt.title('Mittlerer Koinzidenzindex')
    plt.xlabel('Schlüssellänge')
    plt.ylabel('Koinzidenzindex')
    plt.ylim(1, 1.8)
    plt.xlim(0, 50)
    plt.savefig("mean_coincidence.png")