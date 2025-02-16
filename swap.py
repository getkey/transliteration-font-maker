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

def gen_char_map(char_map_file):
    with open(char_map_file, 'r', encoding='utf-8') as file:
        char_map = {}
        for line in file.readlines():
            key, value = line.strip().split('\t')

            # for now, we don't do ligatures
            if len(key) > 1 or len(value) > 1:
                continue

            char_map[ord(key)] = ord(value)
            char_map[ord(value)] = ord(key)
        return char_map
    

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: fontforge -script test.py <input.sfd> <output.otf> <new_font_name> <transcription_map.tsv>")
        sys.exit(1)

    print(sys.argv)
    
    output_otf = sys.argv[2]

    char_map = gen_char_map(sys.argv[4])

    font = fontforge.open(sys.argv[1])
    rename(font, sys.argv[3])
    swap(font, char_map)

    # font.save("test.sfd")
    font.generate(sys.argv[2])
    print(f"Font saved as {sys.argv[2]}")
