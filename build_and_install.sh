#!/bin/sh

fontfile=../liberation-fonts/src/LiberationSerif-Regular.sfd
swap_csv=./traditional_greek_romanization.tsv
outname='Apeleutherosis Serif Regular'

fontforge -script swap.py -n "$outname" -t "$swap_csv" -o ~/.local/share/fonts/"$outname".otf "$fontfile"
fc-cache -f
