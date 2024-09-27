#!/usr/bin/env python

import unittest

from rxg.main import generate
from rxg.structures import RegexPattern, RegexPatternList

Precision = RegexPattern.Precision


class TestGenerator():
    def test_RegexGenerator(self):
        patterns = generate(self.STR_LST, exact=self.EXACT)

        self.assertIsInstance(patterns, RegexPatternList)
        for i, pattern in enumerate(patterns):
            self.assertIsInstance(pattern, RegexPattern)
            self.assertEqual(str(pattern), self.RGX_LST[i])

class TestGeneraliser():
    def test_RegexGeneraliser(self):
        patterns = generate(self.STR_LST)

        self.assertIsInstance(patterns, RegexPatternList)
        for i, (pattern, members) in enumerate(patterns.generalize()):
            self.assertIsInstance(pattern, RegexPattern)
            self.assertEqual(str(pattern), self.RGX_LST[i][0])
            self.assertEqual(members, self.RGX_LST[i][1])


class TestPrecise(TestGenerator, unittest.TestCase):
    EXACT = True
    STR_LST = ['Pizza Cats', 'Donkey Kong', 'Salty Dogs', 'ace123', 'pillow50', 'john99']
    RGX_LST = ['^P[a-z]{4}\\sC[a-t]{3}$', '^D[e-y]{5}\\sK[g-o]{3}$', '^S[a-y]{4}\\sD[g-s]{3}$',
               '^[a-e]{3}[1-3]{3}$', '^[i-w]{6}[0-5]{2}$', '^[h-o]{4}9{2}$']

class TestImprecise(TestGenerator, unittest.TestCase):
    EXACT = False
    STR_LST = ['Pizza Cats', 'Donkey Kong', 'Salty Dogs', 'ace123', 'pillow50', 'john99']
    RGX_LST = ['^[A-Z][a-z]{4}\\s[A-Z][a-z]{3}$', '^[A-Z][a-z]{5}\\s[A-Z][a-z]{3}$',
               '^[A-Z][a-z]{4}\\s[A-Z][a-z]{3}$', '^[a-z]{3}[0-9]{3}$',
               '^[a-z]{6}[0-9]{2}$', '^[a-z]{4}[0-9]{2}$']

class TestGeneralising(TestGeneraliser, unittest.TestCase):
    STR_LST = ['Pizza Cats', 'Donkey Kong', 'Salty Dogs', 'ace123', 'pillow50', 'john99']
    RGX_LST = [('^[a-w]{3,6}[0-9]{2,3}$', {3, 4, 5}), ('^[D-S][a-z]{4,5}\\s[C-K][a-t]{3}$', {0, 1, 2})]

if __name__ == '__main__':
    unittest.main()
