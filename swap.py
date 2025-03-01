#!/usr/bin/env python3

import fontforge
import sys

def rename(font, new_font_name):
    font.fontname = new_font_name.replace(' ', '')
    font.familyname = new_font_name
    font.fullname = new_font_name

def swap(font, mappings):
    for script, simple_map in mappings.items():
        swap_table_name = f"crossswap_{script}"
        font.addLookup(swap_table_name, "gsub_single", (), (("ccmp", ((script, ("dflt")),)),))
        font.addLookupSubtable(swap_table_name, swap_table_name)

        ligature_table_name = f"crosslig_{script}"
        font.addLookup(ligature_table_name, "gsub_ligature", (), (("ccmp", ((script, ("dflt")),)),))
        font.addLookupSubtable(ligature_table_name, ligature_table_name)

        decompose_table_name = f"crossdecomp_{script}"
        font.addLookup(decompose_table_name, "gsub_multiple", (), (("ccmp", ((script, ("dflt")),)),))
        font.addLookupSubtable(decompose_table_name, decompose_table_name)

        for key, value in simple_map.items():
            if len(key) > 1 and len(value) > 1:
                # not implemented, this require contextual substitution which is non-trivial
                continue

            if len(key) > 1:
                font[ord(value)].addPosSub(ligature_table_name, tuple([font[ord(char)].glyphname for char in key]))
                continue

            if len(value) > 1:
                font[ord(key)].addPosSub(decompose_table_name, tuple([font[ord(char)].glyphname for char in value]))
                continue

            font[ord(key)].addPosSub(swap_table_name, font[ord(value)].glyphname)

def gen_mappings(file):
    script1, script2 = file.readline().strip().split('\t')

    mappings = {}
    mappings[script1] = {}
    mappings[script2] = {}
    
    for line in file:
        key, value = line.strip().split('\t')

        mappings[script1][key] = value
        mappings[script2][value] = key

    return mappings

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: fontforge -script test.py <input.sfd> <output.otf> <new_font_name> <transcription_map.tsv>")
        sys.exit(1)

    output_otf = sys.argv[2]

    with open(sys.argv[4], 'r', encoding='utf-8') as transcription_file:
        mappings = gen_mappings(transcription_file)

    font = fontforge.open(sys.argv[1])
    font.encoding = 'UnicodeBmp' # make sure the unicode is taken into account
    rename(font, sys.argv[3])
    swap(font, mappings)

    # font.save("test.sfd")
    font.generate(sys.argv[2])
    print(f"Font saved as {sys.argv[2]}")
