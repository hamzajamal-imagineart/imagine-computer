#!/usr/bin/env python3
"""Recolor Squeeze's green accent system to the brand purple #8A3FFC.

Squeeze used a lime accent (#d2ff28 = --color-accent) with dark-olive text on
top of it, plus a green success gradient. #8A3FFC is darker than the lime, so:
  - lime/green fills + standalone green text -> #8A3FFC
  - dark-olive text that sat ON the lime      -> #FFFFFF (stays legible on purple)
  - success gradient green -> purple base + a darker shade
Idempotent: re-running is a no-op once greens are gone.
"""
CSS = "assets/index.D8XJp5Hw.css"

# base #8A3FFC = rgb(138,63,252); darker shade #6E2FCC
MAP = {
    "#d2ff28": "#8A3FFC",  # --color-accent + all lime fills (badge, icons, toc circle, heading bars)
    "#6da300": "#8A3FFC",  # standalone "compressed size" label text
    "#668f07": "#FFFFFF",  # text on lime (badgeAfter, open accordion) -> white on purple
    "#3a6300": "#FFFFFF",  # checkmark glyph on lime -> white on purple
    "#16a34a": "#8A3FFC",  # success overlay gradient (top)
    "#15803d": "#6E2FCC",  # success overlay gradient (bottom) -> darker purple shade
}

css = open(CSS, encoding="utf-8").read()
total = 0
for green, purple in MAP.items():
    n = css.lower().count(green.lower())
    if n:
        # replace case-insensitively (source hexes are lowercase)
        css = css.replace(green, purple).replace(green.upper(), purple)
        total += n
    print(f"{green} -> {purple}: {n}")
open(CSS, "w", encoding="utf-8").write(css)
print("total replacements:", total)
