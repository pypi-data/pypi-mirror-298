#! /usr/bin/env python

from string import punctuation
from typing import Sequence

from rxg.structures import (RegexPattern, RegexPatternList, _mkcharset,
                            _generalize_patterns)
from rxg.utils import _char_to_regex


def generate(s_lst: str | Sequence[str],
             merge_charsets: bool = False,
             exact: bool = True,
             omit_empty: bool = True)\
                   -> RegexPatternList:
    """ Generate Regex patterns for all string literals in the
    input Sequence. Optionally merge adjacent character sets or
    generalize to standard character sets. Returns a list of
    generated pattern objects.


    :param s_lst: Sequence of string literals (or singular literal)
    :type s_lst: Sequence
    :param merge_charsets: Merge adjacent character sets (False)
    :type merge_charsets: bool
    :param exact: Display exact character sets (True)
    :type exact: bool
    :param omit_empty: Omit empty patterns if generation fails (True)
    :type omit_empty: bool
    :rtype: list[RegexPattern]
    """

    if isinstance(s_lst, str):
        # in case a single string is given
        s_lst = [s_lst]

    patterns = RegexPatternList()
    for s in s_lst:
        try:
            pattern = _generate_regex(s)
            if not exact:
                pattern.precision = RegexPattern.Precision.INEXACT
        except:
            continue

        if not (omit_empty and len(pattern) <= 0):
            patterns.append(pattern)

    # merge character sets on word level
    if merge_charsets:
        for i, p in enumerate(patterns):
            patterns[i] = p.generalize()

    return patterns


def generalize(p_lst: Sequence[RegexPattern])\
        -> list[tuple[RegexPattern, set[int]]]:
    """ Generalize patterns on similarity. Returns the
    generalized patterns (if any) together with a set of
    integers that map to the input sequence, and which
    convey membership.

    :param p_list: Sequence of Regex patterns to cluster.
    :type p_list: Sequence[RegexPattern]
    :rtype: dict[RegexPattern, set[int]]
    """
    patterns = dict()
    for i, p in enumerate(p_lst):
        patterns[p] = {i}

    # generalize found patterns
    patterns_generalized = dict()
    for p, members in _generalize_patterns(patterns).items():
        if p not in patterns_generalized.keys():
            patterns_generalized[p] = set()

        patterns_generalized[p] = patterns_generalized[p].union(members)

    return list(patterns_generalized.items())


def _generate_regex(s: str, strip_punctuation: bool = True) -> RegexPattern:
    """ Generate regular expresion that fits string.

    :param s:
    :type s: str
    :param strip_punctuation:
    :type strip_punctuation: bool
    :rtype: RegexPattern
    """
    # remove unecessary white space and punctuation
    s = ' '.join(s.split())
    if strip_punctuation:
        s.translate(str.maketrans('', '', punctuation))
    slen = len(s)

    pattern = RegexPattern()
    if slen <= 0:
        # empty string
        return pattern

    char_set = _mkcharset(_char_to_regex(s[0]))
    char_set.add(s[0])
    for i in range(1, slen):
        symbol_char_set = _char_to_regex(s[i])
        if symbol_char_set == char_set.charset():
            # pattern continues still
            char_set.add(s[i])

            # account for final character
            if i >= slen - 1:
                pattern.add(char_set)

            continue

        # add interupted pattern to output
        pattern.add(char_set)

        # start next char set
        char_set = _mkcharset(symbol_char_set)
        char_set.add(s[i])

        # account for final character
        if i >= slen - 1:
            pattern.add(char_set)

    return pattern
