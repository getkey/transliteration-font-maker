#!/bin/sh

# A font based on [Liberation](https://github.com/liberationfonts/liberation-fonts) can be built and installed with the following script.

swap_csv=./transliterations/traditional_greek_romanization.tsv

for i in "$LIBERATION_FONTS"/src/*.sfd; do
	outfile=$(basename "$i" .sfd | sed 's/^Liberation/Apeleutherosis/')
	outname=$(basename "$i" | sed 's/^Liberation/Apeleutherosis /' | cut -d'-' -f1)
	fontforge -script swap.py -n "$outname" -t "$swap_csv" -o ~/.local/share/fonts/"$outfile".otf "$i"
done

fc-cache -f
