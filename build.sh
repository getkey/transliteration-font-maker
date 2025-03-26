#!/bin/sh

transliteration_tsv=./transliterations/traditional_greek_romanization.tsv
out_dir="$HOME/.local/share/fonts"

while getopts "o:t:" opt; do
  case $opt in
    o) out_dir="$OPTARG" ;;
    t) transliteration_tsv="$OPTARG" ;;
    *) echo "Usage: $0 [-o output_directory] [-t transliteration_tsv] sfd_files..." >&2; exit 1 ;;
  esac
done

shift $((OPTIND - 1))

output_name=$(basename "$transliteration_tsv" .tsv)
font_name=$(echo "$output_name" | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')

echo "Output directory: $out_dir"
echo "Swap CSV file: $transliteration_tsv"
echo "Font name: $font_name"

if [ "$#" -eq 0 ]; then
  echo "No .sfd files provided." >&2
  exit 1
fi

for i in "$@"; do
  if [ ! -f "$i" ]; then
    echo "Skipping non-existent file: $i" >&2
    continue
  fi
  outfile=$(basename "$i" .sfd | sed "s/^DejaVu/${output_name}_/")
  outname=$(basename "$i" | sed "s/^DejaVu/$font_name /" | cut -d'-' -f1)
  fontforge -script ./swap.py -n "$outname" -t "$transliteration_tsv" -o "$out_dir/$outfile.otf" "$i"
done
