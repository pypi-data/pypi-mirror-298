#! /usr/bin/env python


REGEX_ILLEGAL_CHARS = ['[', ']', '\\', '^', '*', '+', '?', '{',
                       '}', '|', '(', ')', '$', '.', '"']
REGEX_WHITE_SPACE = r"\s"
REGEX_LOWER = r"[a-z]"
REGEX_UPPER = r"[A-Z]"
REGEX_DIGIT = r"[0-9]"
REGEX_PUNCT = r"[(\.|\?|!)]"  # subset
REGEX_OTHER = r"[^a-zA-Z0-9\.\?! ]"
