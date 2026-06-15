# ImagineMCP Design Kit

Shared design system for the ImagineMCP marketing site, packaged so another
agent can build a **new page** that matches the existing ones.

**Start with [`GUIDELINES.md`](./GUIDELINES.md)** — it contains the do's/don'ts
(no bold fonts, orange-only accent, Title Case headings, etc.). Everything else
here is the source the guidelines describe.

## Contents
```
GUIDELINES.md              ← READ FIRST: rules, do's & don'ts
tokens/
  globals.css              ← colors, type scale, fonts, utilities (@theme tokens)
components/
  SiteNav.tsx              ← navbar (light → dark-glass-pill on scroll)
  SiteFooter.tsx           ← dark footer
  FaqSection.tsx           ← two-column FAQ accordion (+ FAQPage JSON-LD)
  Button.tsx               ← shared button primitive (4 variants)
fonts/
  google-sans-flex.ttf     ← the ONLY typeface (variable, weights 100–900)
  layout-font-setup.tsx    ← how to wire the font in Next.js
assets/
  imagine-art-wordmark.svg ← nav logo
  imagine-logo.svg, imagine-mcp-logo.svg
  footer/logo-icon.svg, footer/watermark.svg
```

## Stack assumptions
- **Next.js (App Router)** + **React** + **TypeScript**
- **Tailwind CSS v4** with `@theme` tokens (see `tokens/globals.css`)
- `motion/react` for reveal animations (components use it lightly)

Adjust import/asset paths to the target project when reusing the components.
