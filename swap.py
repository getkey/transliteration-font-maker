#!/usr/bin/env python3

import sys
import re

def swap_characters(sfd_file, char_map, output_file):
    with open(sfd_file, 'r', encoding='utf-8') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        match = re.match(r'^Encoding: (\d+)', line)
        if match:
            old_char = match.group(1)
            if old_char in char_map:
                new_char = char_map[old_char]
                content[i] = re.sub(rf'^Encoding: {old_char} ', f'Encoding: {new_char} ', line)
                print(f'Swapped {old_char} -> {new_char}')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(content)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python swap_sfd_chars.py <input.sfd> <output.sfd> <transcription_map.tsv>")
        sys.exit(1)

    sfd_file = sys.argv[1]
    output_file = sys.argv[2]
    char_map_file = sys.argv[3]
    with open(char_map_file, 'r', encoding='utf-8') as file:
        char_map = {}
        for line in file.readlines():
            key, value = line.strip().split('\t')

            # for now, we don't do ligatures
            if len(key) > 1 or len(value) > 1:
                continue

            char_map[ord(key)] = ord(value)
            char_map[ord(value)] = ord(key)

    swap_characters(sfd_file, char_map, output_file)
