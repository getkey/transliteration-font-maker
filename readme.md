# transliteration-fonts

These fonts allow displaying text in another script than its native script. This is useful to learn to decipher an alphabet you are **not** accustomed to, in a language you **are** accustomed to.

Transliterations fonts can be downloaded from the [releases](https://github.com/getkey/transliteration-fonts/releases/latest).

## Creating your font

This tool modifies TrueType fonts (`.ttf`) with a transliteration table.

```sh
./swap.py -t transliteration_file.tsv -o input_font.ttf transliteration_font.sfd
```

## Building the provided [transliterations](./transliterations)

```
nix-build
```
