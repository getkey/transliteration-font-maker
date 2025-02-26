#!/usr/bin/env python3

import fontforge
import sys

def rename(font, new_font_name):
    font.fontname = new_font_name
    font.familyname = new_font_name
    font.fullname = new_font_name

def swap(font, char_map):
    font.encoding = 'UnicodeBmp' # make sure the unicode is taken into account
    for glyph in font.glyphs():
        if glyph.unicode in char_map:
            glyph.unicode = char_map[glyph.unicode]

def gen_1_to_1_mappings(file):
    char_map = {}
    file.seek(0)
    for line in file:
        key, value = line.strip().split('\t')

        # exclude ligatures
        if len(key) > 1 or len(value) > 1:
            continue

        char_map[ord(key)] = ord(value)
        char_map[ord(value)] = ord(key)

    return char_map

def gen_ligature_mappings(file):
    char_map = {}
    file.seek(0)
    for line in file:
        key, value = line.strip().split('\t')


        print(key, value)

        if len(key) > 1 and len(value) == 1:
            char_map[key] = value

        if len(value) > 1 and len(key) == 1:
            char_map[value] = key

    return char_map

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: fontforge -script test.py <input.sfd> <output.otf> <new_font_name> <transcription_map.tsv>")
        sys.exit(1)

    output_otf = sys.argv[2]

    with open(sys.argv[4], 'r', encoding='utf-8') as transcription_file:
        simple_mappings = gen_1_to_1_mappings(transcription_file)
        ligature_mappings = gen_ligature_mappings(transcription_file)

    print(ligature_mappings)

    font = fontforge.open(sys.argv[1])
    rename(font, sys.argv[3])
    swap(font, simple_mappings)

    # font.save("test.sfd")
    font.generate(sys.argv[2])
    print(f"Font saved as {sys.argv[2]}")
