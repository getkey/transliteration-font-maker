#!/usr/bin/env python3

import argparse
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from sortedcontainers import SortedDict

def rename(font, family_name):
	"""Rename the font family name and update other name fields."""
	name_table = font['name']

	subfamily_name = None
	for record in name_table.names:
		if record.nameID == 2:
			subfamily_name = record.toUnicode()
			break

	if not subfamily_name:
		raise ValueError("Subfamily name (nameID 2) not found in name table.")

	full_name = f"{family_name} {subfamily_name}"
	postscript_name = f"{family_name}-{subfamily_name}".replace(' ', '')

	def update_name(nameID, new_value):
        # we must iterate because the name table might contain the same nameID multiple times
        # for different platforms or languages
		for record in name_table.names:
			if record.nameID == nameID:
				record.string = new_value.encode(record.getEncoding())

	update_name(1, family_name)       # Font Family name
	update_name(4, full_name)         # Full font name
	update_name(6, postscript_name)   # PostScript name


def char_to_glyph(font, char):
    """Get the glyph name for a character using the cmap."""
    unicode_val = ord(char)
    cmap = font.getBestCmap()

    if unicode_val in cmap:
        return cmap[unicode_val]
    raise ValueError(f"Character '{char}' not found in cmap")

def build_feature_string(font, mappings):
    """Build a feature string for the font based on the mappings."""

    features = ""

    for script, simple_map in mappings.items():
        rules = []

        for key, value in simple_map.items():
            try:
                if len(key) > 1 and len(value) > 1:
                    src_glyphs = " ".join(char_to_glyph(font, c) for c in key)
                    dest_glyphs = " ".join(char_to_glyph(font, c) for c in value)
                    dummy_glyph = "_".join(char_to_glyph(font, c) for c in value)

                    if dummy_glyph not in font.getGlyphOrder():
                        font["glyf"].glyphs[dummy_glyph] = Glyph()
                        font["hmtx"].metrics[dummy_glyph] = (0, 0)
                        font.setGlyphOrder(font.getGlyphOrder() + [dummy_glyph])

                    rules.append(f"sub {src_glyphs} by {dummy_glyph};")
                    rules.append(f"sub {dummy_glyph} by {dest_glyphs};")

                elif len(key) > 1:
                    src_glyphs = " ".join(char_to_glyph(font, c) for c in key)
                    dest_glyph = char_to_glyph(font, value)
                    rules.append(f"sub {src_glyphs} by {dest_glyph};")

                elif len(value) > 1:
                    src_glyph = char_to_glyph(font, key)
                    dest_glyphs = " ".join(char_to_glyph(font, c) for c in value)
                    rules.append(f"sub {src_glyph} by {dest_glyphs};")

                else:
                    src_glyph = char_to_glyph(font, key)
                    dest_glyph = char_to_glyph(font, value)
                    rules.append(f"sub {src_glyph} by {dest_glyph};")

            except ValueError as e:
                print(f"Warning: {e}")
                continue

        if len(rules) > 0:
            features += f"""
feature ccmp {{
    script {script};
    language dflt;

    {''.join(rules)}

}} ccmp;
"""

    return features

def sort_long_first(item):
    # when we create the features, we want substitutions with the most characters to be applied first
    # because if a substitution with 1 or few characters is applied first, it will prevent substitutions with more characters containing the same characters
    return -len(item)

def gen_mappings(file):
    script1, script2 = file.readline().strip().split('\t')

    mappings = {}
    mappings[script1] = SortedDict(sort_long_first)
    mappings[script2] = SortedDict(sort_long_first)

    for line in file:
        key, value = line.strip().split('\t')
        mappings[script1][key] = value
        mappings[script2][value] = key

    return mappings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a transliteration font')
    parser.add_argument('input', type=str, help='Input font file (.ttf, .otf)')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output font file (.ttf, .otf)')
    parser.add_argument('-n', '--name', type=str, help='New font family name')
    parser.add_argument('-t', '--transliteration-table', required=True, type=str, help='Transcription file (.tsv)')
    args = parser.parse_args()

    if args.input.endswith('.ttf') and not args.output.endswith('.ttf') or args.input.endswith('.otf') and not args.output.endswith('.otf'):
        raise ValueError("Input and output file must have the same extension")

    with open(args.transliteration_table, 'r', encoding='utf-8') as transliteration_file:
        mappings = gen_mappings(transliteration_file)

    font = TTFont(args.input)

    if args.name:
        rename(font, args.name)

    feature_str = build_feature_string(font, mappings)
    addOpenTypeFeaturesFromString(font, feature_str)

    font.save(args.output)
    print(f"Font saved as {args.output}")

    font.close()
