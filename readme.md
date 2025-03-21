# transliteration-font-maker

This software modifies fonts in [SFD format](https://fontforge.org/docs/techref/sfdformat.html) with a transliteration table. This allows displaying text in another script than its native script.

This is a useful tool to learn to decipher an alphabet you are **not** accustomed to, in a language you **are** accustomed to.

```sh
fontforge -script swap.py -t my_transliteration_file.tsv -o ./my_font.otf ./my_font.sfd
```

## For convenience

This repository contains a few transliteration files in [this directory](https://github.com/getkey/cross-alphabetizer/tree/main/transliterations) for various scripts.

This repository provides [a script](https://github.com/getkey/cross-alphabetizer/tree/main/apeleutherosis) to modify the Liberation Fonts to transliterate latin to greek.
