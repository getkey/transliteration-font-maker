#!/usr/bin/env python3

"""
Unicode has a lot of characters that can be decomposed into multiple characters.
It is impractical to generate a mapping by hand, so this script generates a mapping based on a list of base characters
"""

import unicodedata
import argparse

def gen_mappings(files):
    mappings = {}
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                key, value = line.strip().split('\t')

                mappings[key] = value

    return mappings

def print_decomposed(files, mappings):
    for file in files:
        with open(file, 'r') as f:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base', action='append', type=str, required=True, help='Base .tsv file')
    parser.add_argument('-c', '--char-list', action='append', type=str, required=True, help='Char list file')
    args = parser.parse_args()

    mappings = gen_mappings(args.base)
    print_decomposed(args.char_list, mappings)
