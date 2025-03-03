#!/bin/sh

# A font based on [Liberation](https://github.com/liberationfonts/liberation-fonts) can be built and installed with the following script.

liberation_fonts_dir=../liberation-fonts/src/
swap_csv=./transcriptions/traditional_greek_romanization.tsv

for i in "$liberation_fonts_dir"*.sfd; do
	outfile=$(basename "$i" .sfd | sed 's/^Liberation/Apeleutherosis/')
	outname=$(basename "$i" | sed 's/^Liberation/Apeleutherosis /' | cut -d'-' -f1)
	fontforge -script swap.py -n "$outname" -t "$swap_csv" -o ~/.local/share/fonts/"$outfile".otf "$i"
done

fc-cache -f
