#!/usr/bin/env python3

import sys
import fontforge

font = fontforge.open(sys.argv[1])
font.fontname = sys.argv[2]
font.familyname = sys.argv[2]
font.fullname = sys.argv[2]
font.generate(f'{sys.argv[2]}.otf')
