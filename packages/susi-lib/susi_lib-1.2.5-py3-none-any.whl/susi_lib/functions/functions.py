"""Contains some useful functions"""

from enum import Enum, auto

from susi_lib.types import Symbols


def is_palindrome(word) -> bool:
    """Checks if a value is a palindrome (is the same from front and back).

    :param word: value to check, it needs to have :py:meth:`__getitem__`, :py:meth:`__len__` and :py:meth:`__ne__`
    :return: ``True`` if it is a palindrome, ``False`` when it is not
    """
    for i in range(len(word) // 2):
        if word[i] != word[-(i + 1)]:
            return False
    return True


def decode(string: str) -> str:
    """Decodes a given value.

    Supported encodings are :py:class:`Braille`, :py:class:`Numbers`, :py:class:`Morse`
    and :py:class:`Semaphore`. Encoding should be the same as the strings returned
    by :py:meth:`__str__` method of classes in :py:mod:`susi_lib.types`.

    :raises: :py:class:`TypeError` when invalid parameter types are passed

    :param string: The string to decode
    :return: Decoded string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return Symbols.from_string(string)


def _encode_morse(string: str):
    """Encode the given string into morse.

    :raises: :py:class:`TypeError` when invalid parameter types are passed

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :return: Encoded morse string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return str(Symbols(string).to_morse())


def _encode_braille(string: str):
    """Encode the given string into braille.

    :raises: :py:class:`TypeError` when invalid parameter types are passed

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :return: Encoded braille string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return str(Symbols(string).to_braille())


def _encode_semaphore(string: str):
    """Encode the given string into semaphore.

    :raises: :py:class:`TypeError` when invalid parameter types are passed

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :return: Encoded semaphore string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return str(Symbols(string).to_semaphore())


def _encode_numbers(string: str, base=10):
    """Encode the given string into numbers of given base

    :raises: :py:class:`TypeError` when invalid parameter types are passed
    :raises: :py:class:`ValueError` when invalid value for ``base`` is passed

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :param base: The base of the number system (2, 10, 16)
    :return: Encoded numbers string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    if not isinstance(base, int):
        raise TypeError("Base must be an int")
    if base not in [2, 10, 16]:
        raise ValueError("Valid values for base are 2, 10, 16")
    return str(Symbols(string).to_number_systems(base))


class Encoding(Enum):
    """:class:`Enum` class to specify encoding for :py:func:`encode`."""

    MORSE = auto()
    """Encode to morse"""
    BRAILLE = auto()
    """Encode to braille"""
    SEMAPHORE = auto()
    """Encode to semaphore"""
    NUMBERS = auto()
    """Encode to numbers"""


def encode(string: str, encoding: Encoding, base: int = 10) -> str:
    """Encode the given string into desired encoding

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :param encoding: Desired encoding, see :py:class:`Encoding`
    :param base: The base of the number system (2, 10, 16), needed only for :py:attr:`Encoding.NUMBERS`
    :return: Encoded string
    """
    match (encoding):
        case Encoding.MORSE:
            return _encode_morse(string)
        case Encoding.BRAILLE:
            return _encode_braille(string)
        case Encoding.SEMAPHORE:
            return _encode_semaphore(string)
        case Encoding.NUMBERS:
            return _encode_numbers(string, base)
        case _:
            raise ValueError("Invalid enum value")


def _calculate_freq(word: str) -> dict[str, int]:
    word_freq: dict[str, int] = {}
    for c in word:
        word_freq[c] = word_freq.get(c, 0) + 1
    return word_freq


def find_anagrams(word: str, word_list: list[str]) -> list[str]:
    """Function for finding anagrams of a word from a specified list.

    :raises: :py:class:`TypeError` when invalid parameter types are passed

    :param word: Word for which it tries to find anagrams
    :param word_list: List of strings against which it compares permutations of ``word``
    :return: List of anagrams for ``word``
    """
    if not isinstance(word, str):
        raise TypeError("Word must be a string")
    if not isinstance(word_list, list):
        raise TypeError("Word_list must be a list")
    if not all(isinstance(val, str) for val in word_list):
        raise TypeError("Word_list must be a list of strings")
    filtered_words = [w for w in word_list if len(w) == len(word) and w != word]
    word_freq = _calculate_freq(word)
    found_words: list[str] = []

    for w in filtered_words:
        if word_freq == _calculate_freq(w):
            found_words.append(w)

    return found_words


def unique_letters(word: str) -> bool:
    """Function for checking if given ``word`` contains only unique letters.

    :raises: :py:class:`TypeError` when ``word`` is not :py:class:`str`

    :param word: Word to check
    :return: ``True`` if it contains unique letters, ``False`` otherwise
    """
    if not isinstance(word, str):
        raise TypeError("Word must be a string")
    found: set[str] = set()
    for c in word:
        if c in found:
            return False
        found.add(c)
    return True
