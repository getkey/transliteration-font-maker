#!/bin/sh

fontfile=../liberation-fonts/src/LiberationSerif-Regular.sfd
tmpfile=$(mktemp)
swap_csv=latin_greek_codepoints.csv
outname=LiberationGreekLatinSwap

./swap.py $fontfile $tmpfile $swap_csv
fontforge -script fontforge.py $tmpfile ~/.local/share/fonts/$outname.otf
rm $tmpfile
fc-cache -f
