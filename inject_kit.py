# -*- coding: utf-8 -*-
"""Inject the ImagineMCP navbar + footer (ported to vanilla HTML/CSS/JS) into
the saved Squeeze page. Idempotent: strips any prior injection first."""
import re, io

PAGE = "index.html"

NAV_LINKS = [
    ("Old vs new", "#workflow"),
    ("Features", "#comparison"),
    ("About", "#about"),
    ("FAQ", "#faq"),
]

COLUMNS = [
    ("ImagineArt AI Studios", [
        ("Image Studio", "https://www.imagine.art/image"),
        ("Video Studio", "https://www.imagine.art/video"),
        ("Audio Studio", "https://www.imagine.art/audio-studio"),
        ("Film Studio", "https://www.imagine.art/ai-film-studio"),
        ("Workflow", "https://www.imagine.art/flow"),
        ("Enterprise", "https://www.imagine.art/business/enterprise"),
        ("Teams", "https://www.imagine.art/teams-plan"),
    ]),
    ("Tools", [
        ("AI Image Generator", "https://www.imagine.art/ai-image-generator"),
        ("AI Video Generator", "https://www.imagine.art/ai-video-generator"),
        ("AI Audio Generator", "https://www.imagine.art/audio-studio"),
        ("AI Text-to-Speech", "https://www.imagine.art/audio/text-to-speech"),
        ("AI Music Generator", "https://www.imagine.art/audio/music/elevenlabs-music"),
        ("AI Film Studio", "https://www.imagine.art/ai-film-studio"),
        ("AI Workflows", "https://www.imagine.art/workflow"),
    ]),
    ("Apps", [
        ("Video Translate", "https://www.imagine.art/apps/video-translate"),
        ("HeyGen Avatar", "https://www.imagine.art/apps/heygen-avatar"),
    ]),
    ("Contact Us", [
        ("Contact Sales", "https://www.imagine.art/teams-plan/contact-us"),
        ("Book a Demo", "https://cal.com/team/imagineart/imagineart-customer-assist"),
    ]),
    ("Community", [
        ("Discord", "https://discord.com/invite/z7kjUyvAbv"),
        ("Twitter / X", "https://twitter.com/Imagine_aiart"),
        ("Instagram", "https://www.instagram.com/imagineartofficial"),
    ]),
    ("Pricing", [
        ("See Plans", "https://www.imagine.art/subscription"),
    ]),
]

SOCIALS = [
    ("Facebook", "https://www.facebook.com/groups/imagineai", "M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"),
    ("Twitter / X", "https://twitter.com/Imagine_aiart", "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.741l7.432-8.5L2.25 2.25H8.08l4.253 5.622zm-1.161 17.52h1.833L7.084 4.126H5.117z"),
    ("Discord", "https://discord.com/invite/z7kjUyvAbv", "M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.04.03.05a19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028 14.09 14.09 0 001.226-1.994.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128c.126-.094.252-.192.372-.292a.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.1.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"),
    ("Instagram", "https://www.instagram.com/imagineartofficial", "M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"),
    ("YouTube", "https://www.youtube.com/@imagineartofficial", "M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12z"),
    ("Reddit", "https://www.reddit.com/r/ImagineAiArt/", "M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"),
]

APP_STORE_PATH = "M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"
PLAY_PATH = "M3.18 23.75c.33.18.7.26 1.08.22l13.12-7.57-2.82-2.82-11.38 10.17zM.75 1.13C.28 1.63 0 2.39 0 3.36v17.28c0 .97.28 1.73.76 2.22l.12.11 9.68-9.68v-.23L.87 3.02.75 1.13zM20.9 9.61l-2.8-1.62-3.15 3.14 3.15 3.15 2.81-1.62c.8-.46.8-1.21 0-1.67v.62zM4.26.25L17.38 7.82l-2.82 2.82L3.18.47A1.39 1.39 0 014.26.25z"

FONT = "/Guidelines/fonts/google-sans-flex.ttf"
LOGO = "/Guidelines/assets/imagine-art-wordmark.svg"
F_ICON = "/Guidelines/assets/footer/logo-icon.svg"
F_MARK = "/Guidelines/assets/footer/watermark.svg"

def ext(href): return ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""

# ---------------- CSS ----------------
CSS = """
<style id="imagine-kit-style">
@font-face{font-family:"Google Sans Flex";src:url("__FONT__") format("truetype");font-weight:100 900;font-display:swap;}
.im-nav,.im-nav *,.im-footer,.im-footer *{box-sizing:border-box;font-family:"Google Sans Flex","Inter",ui-sans-serif,system-ui,sans-serif;}

/* ===== NAVBAR ===== */
.im-nav{position:fixed;top:0;left:0;right:0;z-index:9000;padding:16px 0;transition:padding .3s ease;}
.im-nav.is-scrolled{padding:10px 0;}
.im-nav__bar{margin:0 auto;display:flex;align-items:center;justify-content:space-between;max-width:100%;padding:10px clamp(40px,12vw,220px);border-radius:22px;border:1px solid transparent;background:transparent;transition:max-width .48s cubic-bezier(.22,1,.36,1),padding .48s cubic-bezier(.22,1,.36,1),background .48s cubic-bezier(.22,1,.36,1),border-color .48s cubic-bezier(.22,1,.36,1),box-shadow .48s cubic-bezier(.22,1,.36,1);}
.im-nav.is-scrolled .im-nav__bar{max-width:min(1180px,calc(100vw - 32px));padding:8px 12px;background:rgba(10,10,11,.72);-webkit-backdrop-filter:blur(32px) saturate(180%);backdrop-filter:blur(32px) saturate(180%);box-shadow:0 20px 48px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.08),0 0 0 1px rgba(255,255,255,.1);}
.im-nav__logo{display:inline-flex;align-items:center;flex-shrink:0;text-decoration:none;}
/* Default (top) state sits over the dark hero, so the palette is light;
   it morphs into the dark glass pill on scroll (also light). */
.im-nav__logo img{height:22px;width:auto;transition:filter .3s;filter:brightness(0) invert(1);}
.im-nav__links{display:none;align-items:center;gap:2px;}
.im-nav__links a{padding:6px 14px;border-radius:8px;font-size:14px;font-weight:500;letter-spacing:.14px;white-space:nowrap;text-decoration:none;color:rgba(255,255,255,.78);transition:color .15s,background .15s;}
.im-nav__links a:hover{color:#fff;background:rgba(255,255,255,.1);}
.im-nav.is-scrolled .im-nav__links a{color:rgba(255,255,255,.7);}
.im-nav.is-scrolled .im-nav__links a:hover{color:#fff;background:rgba(255,255,255,.08);}
.im-nav__actions{display:none;align-items:center;gap:4px;flex-shrink:0;}
.im-nav__cta{display:inline-flex;align-items:center;justify-content:center;height:34px;padding:0 16px;border-radius:22px;font-size:13.5px;font-weight:500;letter-spacing:.14px;text-decoration:none;background:#fff;color:rgb(10,10,11);box-shadow:0 2px 8px rgba(0,0,0,.18);transition:all .2s;}
.im-nav.is-scrolled .im-nav__cta{background:#fff;color:rgb(10,10,11);box-shadow:0 2px 8px rgba(0,0,0,.2);}
.im-nav__burger{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:10px;border:none;background:transparent;cursor:pointer;color:rgba(255,255,255,.85);transition:color .15s;}
.im-nav.is-scrolled .im-nav__burger{color:rgba(255,255,255,.85);}
.im-nav__burger span{display:flex;flex-direction:column;gap:5px;}
.im-nav__burger span i{display:block;width:18px;height:1.5px;border-radius:2px;background:currentColor;transition:transform .25s;}
@media(min-width:1024px){.im-nav__links{display:flex;}.im-nav__actions{display:flex;}.im-nav__burger{display:none;}}

/* mobile overlay */
.im-menu{position:fixed;inset:0;z-index:9100;background:#fff;display:none;flex-direction:column;}
.im-menu.is-open{display:flex;animation:imMenuIn .22s cubic-bezier(.4,0,.2,1) forwards;}
@keyframes imMenuIn{from{opacity:0;transform:translateY(-10px);}to{opacity:1;transform:translateY(0);}}
.im-menu__top{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;flex-shrink:0;}
.im-menu__top img{height:22px;width:auto;}
.im-menu__close{display:inline-flex;padding:4px;border:none;background:transparent;cursor:pointer;color:rgba(0,0,0,.6);}
.im-menu__body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-bottom:40px;}
.im-menu__links{display:flex;flex-direction:column;align-items:center;gap:4px;}
.im-menu__links a{display:block;text-align:center;padding:10px 32px;border-radius:10px;font-size:22px;font-weight:300;letter-spacing:-.2px;text-decoration:none;color:rgba(0,0,0,.7);transition:color .15s;}
.im-menu__rule{width:calc(100% - 48px);height:1px;background:rgba(0,0,0,.08);margin:16px 0;}
.im-menu__cta{display:inline-flex;align-items:center;justify-content:center;height:44px;padding:0 24px;border-radius:14px;font-size:14px;font-weight:500;text-decoration:none;background:rgb(23,23,23);color:#fff;}

/* ===== FOOTER ===== */
.im-footer{background:#070707;border-top:1px solid rgba(255,255,255,.06);overflow-x:hidden;}
.im-footer__inner{max-width:1240px;margin:0 auto;padding:40px 20px 32px;}
.im-footer__top{display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;gap:32px;flex-wrap:wrap;}
.im-footer__brand{display:flex;flex-direction:row;width:100%;flex-shrink:0;align-items:flex-start;justify-content:space-between;gap:24px;flex-wrap:wrap;}
.im-footer__brand>img{display:block;width:28px;height:28px;}
.im-footer__try{display:flex;flex-direction:column;gap:8px;}
.im-footer__try .h{font-size:11px;font-weight:600;letter-spacing:.5px;color:rgba(255,255,255,.38);margin-bottom:4px;}
.im-store{display:inline-flex;align-items:center;gap:7px;padding:7px 12px;border-radius:9px;border:1px solid rgba(255,255,255,.1);color:rgba(255,255,255,.6);font-size:11.5px;font-weight:600;text-decoration:none;transition:border-color .2s,color .2s;}
.im-store:hover{border-color:rgba(255,255,255,.28);color:#fff;}
.im-store svg{width:14px;height:14px;flex-shrink:0;}
.im-footer__cols{display:grid;grid-template-columns:repeat(2,1fr);gap:32px;flex:1;min-width:0;}
.im-footer__cols .h{display:block;font-size:11px;font-weight:600;letter-spacing:.5px;color:rgba(255,255,255,.38);margin-bottom:20px;}
.im-footer__cols ul{display:flex;flex-direction:column;gap:12px;list-style:none;margin:0;padding:0;}
.im-footer__cols a{font-size:13px;line-height:1.4;color:rgba(255,255,255,.55);text-decoration:none;transition:color .2s;}
.im-footer__cols a:hover{color:rgba(255,255,255,.9);}
.im-footer__mark{max-width:1240px;margin:0 auto;text-align:center;user-select:none;pointer-events:none;padding:16px 20px 0;line-height:0;}
.im-footer__mark img{width:100%;max-width:1240px;height:auto;display:inline-block;}
.im-footer__bottom{max-width:1240px;margin:0 auto;padding:0 20px 24px;}
.im-footer__bottombar{display:flex;flex-direction:column;gap:16px;padding:20px 0 8px;border-top:1px solid rgba(255,255,255,.06);flex-wrap:wrap;}
.im-footer__copy{display:flex;align-items:center;gap:2px;flex-wrap:wrap;}
.im-footer__copy span{font-size:12px;color:rgba(255,255,255,.25);}
.im-footer__copy span strong{font-weight:600;}
.im-cookie{font-size:12px;color:rgba(255,255,255,.25);padding:0 12px;background:transparent;border:none;cursor:pointer;transition:color .2s;}
.im-cookie:hover{color:rgba(255,255,255,.55);}
.im-footer__socials{display:flex;align-items:center;gap:2px;}
.im-footer__socials a{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,.35);transition:color .2s,background .2s;}
.im-footer__socials a:hover{color:rgba(255,255,255,.8);background:rgba(255,255,255,.06);}
.im-footer__socials svg{width:15px;height:15px;}
@media(min-width:640px){.im-footer__cols{grid-template-columns:repeat(3,1fr);}.im-footer__bottombar{flex-direction:row;justify-content:space-between;align-items:center;}}
@media(min-width:768px){.im-footer__inner{padding:56px 40px 32px;}.im-footer__top{flex-direction:row;gap:48px;}.im-footer__brand{flex-direction:column;width:160px;justify-content:flex-start;gap:32px;}.im-footer__mark,.im-footer__bottom{padding-left:40px;padding-right:40px;}}
@media(min-width:1024px){.im-footer__cols{grid-template-columns:repeat(6,1fr);}}

/* ===== TYPOGRAPHY GUIDELINES (kit) ===== */
/* One typeface everywhere: Google Sans Flex. Squeeze drives all type through
   these :root vars (was Geist / PP Mondwest), so overriding them re-fonts the
   whole page. This :root comes later in source order than the stylesheet, so
   it wins without !important. */
:root{
  --font-display:"Google Sans Flex","Inter",ui-sans-serif,system-ui,sans-serif;
  --font-body:"Google Sans Flex","Inter",ui-sans-serif,system-ui,sans-serif;
  --font-sans:"Google Sans Flex","Inter",ui-sans-serif,system-ui,sans-serif;
  --font-mono:ui-monospace,"SF Mono",Menlo,Monaco,Consolas,monospace;
}
/* Hard rule: weight never exceeds 600 (semibold). The page already uses 400/500;
   this caps the base reset's bold and any stray bold. */
body b,body strong{font-weight:600;}

/* ===== BUTTONS: rounded corners (kit primitive), no download icon ===== */
.button[data-astro-cid-vnzlvqnm]{border-radius:10px;padding:10px var(--space-4);gap:0;}
.tocBtn[data-astro-cid-6t6zfk7k]{border-radius:10px;padding:6px 12px;gap:0;}

/* ===== HERO EYEBROW: "Imagine Computer" in Pixelify Sans ===== */
.im-eyebrow{font-family:"Pixelify Sans","Google Sans Flex",monospace;font-weight:600;font-size:clamp(16px,1.8vw,24px);letter-spacing:.5px;color:#fff;margin:0 0 16px;line-height:1;display:block;}

/* ===== Title Case section headings (GUIDELINES §4). FAQ *questions* stay
   sentence case, so .question is intentionally excluded. ===== */
.heading,.headingTop,.headingBottom,.headingWord,.headingAccentBase,.headingAccentText,.faqAccentBase,.headingLine{text-transform:capitalize;}

/* ===== QA pass: no sharp corners, consistent accent, contrast, spacing ===== */
/* Round everything boxy (generous radii; !important to beat scoped cid rules) */
.badge{border-radius:999px !important;padding:6px 14px !important;}
.numBadge{border-radius:999px !important;background:#14141F !important;color:#fff !important;padding:4px 10px !important;}
.cardInner{border-radius:20px !important;}
.cardIcon{border-radius:14px !important;}
.imagePanel{border-radius:16px !important;overflow:hidden !important;}
.ctaBar{border-radius:18px !important;padding:28px 28px !important;}
.accordionItem[data-open=true]{border-radius:14px !important;}
.headingAccent{border-radius:6px !important;}
/* Contrast fix: final-CTA subtext sits on the dark section -> light it up */
.ctaSub{color:rgba(255,255,255,0.66) !important;}

/* Fix "Every Idea, One Studio": the saved HTML baked data-animated=true, so the
   reveal never re-fires -> the dark fill text stayed clipped (invisible) and the
   white highlight slab was only a partial band. Force the final state: full white
   slab + revealed dark text (matches the hero accent). */
.headingAccent[data-astro-cid-s7flme5r]::before{inset:0 !important;border-radius:6px !important;}
.headingAccentBase[data-astro-cid-s7flme5r]{color:#171717 !important;}      /* single dark text layer on the white slab */
.headingAccentFill[data-astro-cid-s7flme5r]{display:none !important;}        /* hide the offset duplicate layer */

/* About section sits on a LIGHT-blue gradient. The monochrome pass turned its
   accent slab + card icons to ink, leaving black boxes/circles with dark content.
   Fix: white highlight + dark text (matches hero), dark heading text, and light
   icon chips with their dark glyphs visible. */
.headingAccent[data-astro-cid-v2cbyr3p]::before{background:#FFFFFF !important;inset:0 !important;border-radius:6px !important;}
.headingAccentBase[data-astro-cid-v2cbyr3p]{color:#171717 !important;}
.headingAccentFill[data-astro-cid-v2cbyr3p]{display:none !important;}
.headingBottom{color:#171717 !important;}
.cardIcon[data-astro-cid-v2cbyr3p]{background:#EDEDED !important;}
.cardIcon[data-astro-cid-v2cbyr3p] img{filter:none !important;}

/* Final CTA ("Start creating") is on the dark section: "Start" was dark-on-dark
   (invisible). Make it light; "creating" stays dark on its white chip. */
.headingWord[data-astro-cid-hxscshf5]{color:#FFFFFF !important;}

/* About section background gradient */
.section[data-astro-cid-v2cbyr3p]{background:linear-gradient(-89.7deg, #9fa1f2 .18%, #7e64a6 99.93%) !important;}
</style>
""".replace("__FONT__", FONT)

# ---------------- NAV HTML ----------------
nav_links_html = "".join(
    '<a href="%s"%s>%s</a>' % (h, ext(h), l) for l, h in NAV_LINKS
)
menu_links_html = "".join(
    '<a href="%s"%s data-im-close>%s</a>' % (h, ext(h), l) for l, h in NAV_LINKS
)
NAV = """
<header class="im-nav" data-im-nav>
  <div class="im-nav__bar">
    <a class="im-nav__logo" href="https://www.imagine.art/"><img src="%(logo)s" alt="ImagineArt" width="144" height="22"></a>
    <nav class="im-nav__links">%(links)s</nav>
    <div class="im-nav__actions"><a class="im-nav__cta" href="#install">Get Started</a></div>
    <button class="im-nav__burger" type="button" aria-label="Open menu" data-im-burger><span><i></i><i></i></span></button>
  </div>
</header>
<div class="im-menu" data-im-menu>
  <div class="im-menu__top">
    <a href="https://www.imagine.art/"><img src="%(logo)s" alt="ImagineArt" width="144" height="22"></a>
    <button class="im-menu__close" type="button" aria-label="Close menu" data-im-close><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 3l12 12M15 3L3 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
  </div>
  <div class="im-menu__body">
    <div class="im-menu__links">%(mlinks)s</div>
    <div class="im-menu__rule"></div>
    <a class="im-menu__cta" href="#install" data-im-close>Get Started</a>
  </div>
</div>
""" % {"logo": LOGO, "links": nav_links_html, "mlinks": menu_links_html}

# ---------------- FOOTER HTML ----------------
cols_html = ""
for heading, links in COLUMNS:
    lis = "".join('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a></li>' % (h, l) for l, h in links)
    cols_html += '<div><span class="h">%s</span><ul>%s</ul></div>' % (heading, lis)

socials_html = "".join(
    '<a href="%s" target="_blank" rel="noopener noreferrer" title="%s" aria-label="%s"><svg viewBox="0 0 24 24" fill="currentColor"><path d="%s"/></svg></a>' % (h, t, t, p)
    for t, h, p in SOCIALS
)

FOOTER = """
<footer class="im-footer">
  <div class="im-footer__inner">
    <div class="im-footer__top">
      <div class="im-footer__brand">
        <img src="%(icon)s" alt="ImagineArt" width="28" height="28">
        <div class="im-footer__try">
          <span class="h">Try Imagine Mobile</span>
          <a class="im-store" href="https://app.adjust.com/1a1xymg6" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" fill="currentColor"><path d="%(apple)s"/></svg>App Store</a>
          <a class="im-store" href="https://app.adjust.com/1rx90a0u" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" fill="currentColor"><path d="%(play)s"/></svg>Google Play</a>
        </div>
      </div>
      <div class="im-footer__cols">%(cols)s</div>
    </div>
  </div>
  <div class="im-footer__mark"><img src="%(mark)s" alt="" aria-hidden="true"></div>
  <div class="im-footer__bottom">
    <div class="im-footer__bottombar">
      <div class="im-footer__copy">
        <span>&copy; %(year)s <strong>Vyro Turkey</strong>. All rights reserved.</span>
        <button type="button" class="im-cookie">Manage Cookie Preferences</button>
      </div>
      <div class="im-footer__socials">%(socials)s</div>
    </div>
  </div>
</footer>
""" % {"icon": F_ICON, "mark": F_MARK, "apple": APP_STORE_PATH, "play": PLAY_PATH,
       "cols": cols_html, "socials": socials_html, "year": 2026}

JS = """
<script id="imagine-kit-script">
(function(){
  var nav=document.querySelector('[data-im-nav]');
  var menu=document.querySelector('[data-im-menu]');
  function onScroll(){ if(window.scrollY>20){nav.classList.add('is-scrolled');}else{nav.classList.remove('is-scrolled');} }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  var burger=document.querySelector('[data-im-burger]');
  if(burger){burger.addEventListener('click',function(){menu.classList.add('is-open');document.body.style.overflow='hidden';});}
  document.querySelectorAll('[data-im-close]').forEach(function(el){el.addEventListener('click',function(){menu.classList.remove('is-open');document.body.style.overflow='';});});
  // Links shouldn't redirect anywhere for now: neutralize anything that would
  // leave the page (external URLs, downloads). In-page "#section" anchors still scroll.
  document.querySelectorAll('a[href]').forEach(function(a){
    var h=a.getAttribute('href')||'';
    var inPage=(h.charAt(0)==='#'&&h.length>1);
    if(!inPage){
      a.addEventListener('click',function(e){e.preventDefault();});
      a.removeAttribute('target');
    }
  });
})();
</script>
"""

START = "<!-- IMAGINE-KIT:START -->"
END = "<!-- IMAGINE-KIT:END -->"

block_top = START + CSS + NAV + END
block_bottom = START + FOOTER + JS + END

html = io.open(PAGE, encoding="utf-8").read()
# strip any previous injection
html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)

# inject nav (+css) right after <body>, footer (+js) right before </body>
html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + block_top, html, count=1)
html = html.replace("</body>", block_bottom + "</body>", 1)

io.open(PAGE, "w", encoding="utf-8").write(html)
print("injected. nav links:", len(NAV_LINKS), "| footer cols:", len(COLUMNS), "| socials:", len(SOCIALS))
