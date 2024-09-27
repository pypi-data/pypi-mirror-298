# Regular Expression Generator and Generaliser

A regular expression generator for arbitrary sets of strings. Returns the
patterns with exact or generalised character sets, depending on the choice of
the user, and facilitates clustering over patterns to create superpatterns.

## Installation

Use git and pip to clone this repository and to install the library, respectively.

    git clone https://gitlab.com/wxwilcke/pyRXG.git
    cd pyRXG/

    pip install .

Or install directly from PyPi

    pip install pyRXG

## Usage

Import the package and generate a set of regular expressions:

    In [1]: import rxg

    In [2]: patterns = rxg.generate(['Pizza Cats', 'Donkey Kong', 'Salty Dogs', 'ace123', 'pillow50', 'john99'])

    In [3]: patterns
    Out[3]:
    RegexPatternList([^P[a-z]{4}\sC[a-t]{3}$,
                      ^D[e-y]{5}\sK[g-o]{3}$,
                      ^S[a-y]{4}\sD[g-s]{3}$,
                      ^[a-e]{3}[1-3]{3}$,
                      ^[i-w]{6}[0-5]{2}$,
                      ^[h-o]{4}9{2}$])

Change the precision to inexact for a better comparison between patterns:

    In [4]: patterns.set_precision(rxg.Precision.INEXACT)

    In [5]: patterns
    Out[5]:
    RegexPatternList([^[A-Z][a-z]{4}\s[A-Z][a-z]{3}$,
                      ^[A-Z][a-z]{5}\s[A-Z][a-z]{3}$,
                      ^[A-Z][a-z]{4}\s[A-Z][a-z]{3}$,
                      ^[a-z]{3}[0-9]{3}$,
                      ^[a-z]{6}[0-9]{2}$,
                      ^[a-z]{4}[0-9]{2}$])

Generalise (cluster) over regular expressions. The indices of matching patterns
are returned together with the corresponding superpattern:

    In [6]: patterns.generalize()
    Out[6]:
    [(^[D-S][a-z]{4,5}\s[C-K][a-t]{3}$, {0, 1, 2}),
     (^[a-w]{3,6}[0-9]{2,3}$, {3, 4, 5})]
