#!/usr/bin/env python3

import fontforge
import argparse

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
            try:
                if len(key) > 1 and len(value) > 1:
                    # not implemented, this require contextual substitution which is non-trivial
                    continue

                if len(key) > 1:
                    src = font[ord(value)]
                    dest = tuple([font[ord(char)].glyphname for char in key])

                    src.addPosSub(ligature_table_name, dest)
                    continue

                if len(value) > 1:
                    src = font[ord(key)]
                    dest = tuple([font[ord(char)].glyphname for char in value])

                    src.addPosSub(decompose_table_name, dest)
                    continue

                font[ord(key)].addPosSub(swap_table_name, font[ord(value)].glyphname)
            except TypeError as err:
                if 'No such glyph' in str(err):
                    print(f"Glyph not found: {key} or {value}", file=sys.stderr)
                    continue

                raise err

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
    parser = argparse.ArgumentParser(description='Swap characters in a font')
    parser.add_argument('input', type=str, help='Input font file')
    parser.add_argument('-o', '--output', type=str, action="append", required=True, help='Output font file (e.g. .otf, .ttf, .sfd)')
    parser.add_argument('-n', '--name', type=str, help='Font name')
    parser.add_argument('-t', '--transcription-table', required=True, type=str, help='Transcription TSV file')
    args = parser.parse_args()

    with open(args.transcription_table, 'r', encoding='utf-8') as transcription_file:
        mappings = gen_mappings(transcription_file)

    font = fontforge.open(args.input)
    font.encoding = 'UnicodeBmp' # make sure the unicode is taken into account
    if args.name:
        rename(font, args.name)
    swap(font, mappings)

    for output in args.output:
        if output.endswith('.sfd'):
            font.save(output)
        else:
            font.generate(output)

        print(f"Font saved as {output}")
