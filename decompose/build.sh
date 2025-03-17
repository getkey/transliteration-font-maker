#!/bin/sh

script_dir=$(dirname "$0")

cp "$script_dir"/traditional_greek_romanization_base.tsv "$script_dir"/../transliterations/traditional_greek_romanization.tsv
"$script_dir"/decompose.py -b "$script_dir"/traditional_greek_romanization_base.tsv -c "$script_dir"/tonos_dialytika.tsv -c "$script_dir"/extended.tsv >> "$script_dir"/../transliterations/traditional_greek_romanization.tsv
