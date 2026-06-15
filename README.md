# ImagineArt — Landing Page

A landing page restyled and rewritten for **ImagineArt**, the AI creative studio
(image, video, audio and film generation in one place).

## What's here

- `Squeeze – Video & Image Compression for macOS.html` — the page (filename is a
  leftover from the original capture; the content is now ImagineArt).
- `Squeeze – … _files/` — page CSS / JS / image assets.
- `hero-frames/`, `footer-cta/frames/` — scroll-scrubbed WebGL frame sequences.
- `Guidelines/` — the ImagineArt design kit (tokens, fonts, components, assets)
  used to drive the navbar, footer, typography and color.
- Helper scripts used to build the page:
  - `inject_kit.py` — injects the ImagineArt navbar + footer + typography/button rules.
  - `recolor_accent.py` — maps the original accent palette to the brand accent.
  - `rewrite_copy.py` — rewrites the page copy to ImagineArt messaging.

## Run locally

```bash
python3 -m http.server 8000
# then open:
# http://127.0.0.1:8000/Squeeze%20%E2%80%93%20Video%20%26%20Image%20Compression%20for%20macOS.html
```

> The `site/` folder (a Next.js preview of the design-kit components) is intentionally
> not tracked.
