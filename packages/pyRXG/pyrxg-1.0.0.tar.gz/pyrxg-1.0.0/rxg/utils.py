#! /usr/bin/env python

from __future__ import annotations

from rxg.charsets import *


def _char_to_regex(c: str) -> str:
    """ Return suitable character class or (escaped) char if none fit.

    :param c:
    :type c: str
    :rtype: str
    """
    char_class = _character_class(c)
    if char_class == REGEX_OTHER:
        if c in REGEX_ILLEGAL_CHARS:
            # escape char
            c = "\\" + c

        return c

    return char_class


def _character_class(c: str) -> str:
    """ Infer character class.

    :param c:
    :type c: str
    :rtype: str
    """
    if c.isalpha():
        char_class = REGEX_LOWER if c.islower() else REGEX_UPPER
    elif c.isdigit():
        char_class = REGEX_DIGIT
    elif c.isspace():
        char_class = REGEX_WHITE_SPACE
    elif c == "." or c == "?" or c == "!":
        char_class = REGEX_PUNCT
    else:
        char_class = REGEX_OTHER

    return char_class


def _inrange(charset: str, char: str, complement: bool = False) -> bool:
    """ Return true if character is part of a character set, or false if
        the complement is asked.

    :param charset:
    :type charset: str
    :param char:
    :type char: str
    :param complement:
    :type complement: bool
    :rtype: bool

    """
    isin = False
    if charset[0] == '[' and charset[-1] == ']':
        charset = charset[1:-1]

    # range [x-y]
    if '-' in charset:
        assert len(charset) == 3
        begin, end = charset.split('-')
        if ord(char) in range(ord(begin), ord(end) + 1):
            isin = True
    else:
        if charset[0] == '(' and charset[-1] == ")":
            # group (...)
            values = charset[1:-1].split('|')
        else:  # fallback check
            values = charset

        if char in values:
            isin = True

    if complement:
        isin = not isin

    return isin
