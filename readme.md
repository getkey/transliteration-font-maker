# transliteration-fonts

These fonts allow displaying text in another script than its native script. This is useful to learn to decipher an alphabet you are **not** accustomed to, in a language you **are** accustomed to.

Transliterations fonts can be downloaded from the [releases](https://github.com/getkey/transliteration-font-maker/releases/latest).

## Creating your font

This software modifies fonts in [SFD format](https://fontforge.org/docs/techref/sfdformat.html) with a transliteration table.

```sh
fontforge -script swap.py -t my_transliteration_file.tsv -o ./my_font.otf ./my_font.sfd
```

## Building the provided [transliterations](./transliterations)

```
nix-build
```
