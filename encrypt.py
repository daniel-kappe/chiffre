import itertools
import os.path
import re


UPPER_CASE_RANGE = (65, 91)
LETTER_RANGE = UPPER_CASE_RANGE[1] - UPPER_CASE_RANGE[0]
LOWER_CASE_OFFSET = 32


def shifted_alphabet(shift: int) -> dict:
    r"""
        Calculates a mapping of letters to other letters. Each letter is shifted by *shift*

        Parameters
        ----------
        shift: int
            Number of positions each letter is shifted in the alphabet

        Returns
        -------
        dict
            A mapping of letters to other letters.
    """
    shifted_range = [value % LETTER_RANGE + UPPER_CASE_RANGE[0] for value in range(shift, shift + LETTER_RANGE)]
    mapping = {chr(origin): chr(dest) for origin, dest in zip(range(*UPPER_CASE_RANGE), shifted_range)}
    mapping.update({chr(origin + LOWER_CASE_OFFSET): chr(dest + LOWER_CASE_OFFSET)
                    for origin, dest in zip(range(*UPPER_CASE_RANGE), shifted_range)})
    return mapping


def strip_non_letters(in_string: str) -> str:
    return re.sub(r"[\W\d]", "", in_string)


def scytale(in_string: str, block: int) -> str:
    r"""
        Uses a Scytale Chiffre to encode a message using a fixed block size.

        Parameters
        ----------
        in_string: str
            Message to be encoded.
        block: int
            Blocksize

        Returns
        -------
        str
            The Scytale encoded message.
    """
    blocking = [[letter for letter in in_string[start_idx::block]] for start_idx in range(block)]
    return ''.join(itertools.chain.from_iterable(blocking))


def caesar(in_string: str, shift: str) -> str:
    r"""
        Uses a Caesar Chiffre to encode a message using a fixed shift.

        Parameters
        ----------
        in_string: str
            Message to be encoded.
        shift: str
            Letter where A is shifted to.

        Returns
        -------
        str
            The input Message, but all characters are shifed by *shift*.
    """
    shift = ord(shift.upper()) - UPPER_CASE_RANGE[0]
    mapping = str.maketrans(shifted_alphabet(shift))
    cleaned_string = strip_non_letters(in_string)
    encoded_string = cleaned_string.translate(mapping)
    return encoded_string


def vigenere(in_string: str, shift_string: str) -> str:
    r"""
        Uses the same principle as the Caesar Chiffre, but a shiftphrase instead of a shiftletter is used.
    :param in_string:
    :param shift_string:
    :return:
    """
    encoded_string = ""
    mappings = [str.maketrans(shifted_alphabet(ord(letter.upper()) - UPPER_CASE_RANGE[0])) for letter in shift_string]
    cleaned_string = strip_non_letters(in_string)
    for letter, mapping in zip(cleaned_string, itertools.cycle(mappings)):
        encoded_string += letter.translate(mapping)
    return encoded_string


if __name__ == "__main__":
    print(caesar("Hallo, Welt!", "x"))
    print(vigenere("Hallo, Welt!", "xaa"))

    scytale_write_flag = "w" if os.path.isfile("encrypted_scytale.txt") else "x"
    with open("source_scytale.txt", "r") as source_scytale:
        with open("encrypted_scytale.txt", scytale_write_flag) as encoded_scytale:
            encoded_scytale.write(scytale(source_scytale.read(), 13))

    caesar_write_flag = "w" if os.path.isfile("encrypted_caesar.txt") else "x"
    with open("source_caesar.txt", "r") as source_caesar:
        with open("encrypted_caesar.txt", caesar_write_flag) as encoded_caesar:
            encoded_caesar.write(caesar(source_caesar.read(), "H"))

    vigenere_write_flag = "w" if os.path.isfile("encrypted_vigenere.txt") else "x"
    with open("source_vigenere.txt", "r") as source_vigenere:
        with open("encrypted_vigenere.txt", vigenere_write_flag) as encoded_vigenere:
            encoded_vigenere.write(vigenere(source_vigenere.read(), "AveCaesar"))