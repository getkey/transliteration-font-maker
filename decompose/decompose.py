#!/usr/bin/env python3

"""
Unicode has a lot of characters that can be decomposed into multiple characters.
It is impractical to generate a mapping by hand, so this script generates a mapping based on a list of base characters
"""

import unicodedata
import os

base = os.path.join(os.path.dirname(__file__), 'traditional_greek_romanization_base.tsv')
extended = os.path.join(os.path.dirname(__file__), 'extended.tsv')

with open(base, 'r') as file:
    mappings = {}
    for line in file:
        key, value = line.strip().split('\t')

        mappings[key] = value

with open(extended, 'r') as f:
    for line in f:
        old = line.strip()
        new = ''
        for codepoint in unicodedata.normalize('NFD', old):
            if mappings.get(codepoint):
                new += mappings[codepoint]
                continue

            new += codepoint

        new = unicodedata.normalize('NFC', new)
        if old == new:
            continue

        print(old + '\t' + new)
