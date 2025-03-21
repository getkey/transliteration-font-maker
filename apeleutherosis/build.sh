#!/bin/sh

here=$(dirname "$0")
swap_csv="$here"/../transliterations/traditional_greek_romanization.tsv
out_dir="$HOME/.local/share/fonts"

while getopts "o:" opt; do
  case $opt in
    o) out_dir="$OPTARG" ;;
    *) echo "Usage: $0 [-o output_directory] sfd_files..." >&2; exit 1 ;;
  esac
done

shift $((OPTIND - 1))

echo "Output directory: $out_dir"

if [ "$#" -eq 0 ]; then
  echo "No .sfd files provided." >&2
  exit 1
fi

for i in "$@"; do
  if [ ! -f "$i" ]; then
    echo "Skipping non-existent file: $i" >&2
    continue
  fi
  outfile=$(basename "$i" .sfd | sed 's/^Liberation/Apeleutherosis/')
  outname=$(basename "$i" | sed 's/^Liberation/Apeleutherosis /' | cut -d'-' -f1)
  fontforge -script "$here"/../swap.py -n "$outname" -t "$swap_csv" -o "$out_dir/$outfile.otf" "$i"
done
