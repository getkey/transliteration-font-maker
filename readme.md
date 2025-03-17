# transliteration-font-maker

This software modifies fonts in [SFD format](https://fontforge.org/docs/techref/sfdformat.html) with a transliteration table. This allows displaying text in another script than its native script.

This is a useful tool to learn to decipher an alphabet you are **not** accustomed to, in a language you **are** accustomed to.

```sh
fontforge -script swap.py -t my_transliteration_file.tsv -o ./my_font.otf ./my_font.sfd
```

This repository contains a few transliteration files in [this directory](https://github.com/getkey/cross-alphabetizer/tree/main/transliterations) for Ancient and Modern Greek as well as Cyrillic.
If you don't know where to start, the Liberation font family is an excellent starting point. You can run and tweak [build_and_install_liberation.sh](https://github.com/getkey/cross-alphabetizer/blob/main/build_and_install_liberation.sh) with a transliteration file of your choosing.
