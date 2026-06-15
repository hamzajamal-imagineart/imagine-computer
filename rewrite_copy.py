# -*- coding: utf-8 -*-
"""Rewrite the Squeeze (Mac compression app) page copy into ImagineArt
(AI creative studio) copy. Whitespace-tolerant: each `old` is matched with
flexible whitespace so multiline HTML still matches. Reports any miss."""
import re, io

PAGE = "Squeeze – Video & Image Compression for macOS.html"
s = io.open(PAGE, encoding="utf-8").read()

# (old, new). For short/ambiguous strings the old is wrapped in >...< so it only
# matches a text node, not an attribute or a substring of a longer phrase.
PAIRS = [
    # ---------- Hero ----------
    (">Stop compressing<", ">Create anything<"),
    (">like it's<", ">you can imagine<"),
    (">1996<", ">with AI<"),
    ("Video and image compression with side-by-side preview, file size stats, and one-click upload to Webflow. Free and macOS native.",
     "Generate stunning images, video, audio and film from a single prompt — every leading AI model in one creative studio. Free to start, no skills required."),

    # ---------- Workflow / settings section ----------
    ("Your workflow is broken,", "Every idea,"),
    (">so we fixed it<", ">one studio<"),
    (">Video Codec<", ">Model<"),
    (">H.264 — MP4<", ">GPT Image<"),
    (">H.265 — MP4<", ">Flux Pro<"),
    (">VP9 — WebM<", ">Imagen<"),
    (">ProRes 422 — MOV<", ">Veo Video<"),
    (">ProRes 4444 — MOV<", ">Kling Video<"),
    (">GIF<", ">Stable Diffusion<"),
    (">Frame rate<", ">Aspect ratio<"),
    (">60fps (Original)<", ">16:9 (Landscape)<"),
    (">Video quality<", ">Quality<"),
    (">Advanced compression settings<", ">Advanced generation settings<"),
    (">Speed<", ">Style<"),
    (">Sound<", ">Upscale<"),
    (">Source<", ">4K Ultra<"),

    ("Full control over every setting.", "Full control over every output."),
    ("Codec, quality, frame rate, file size — adjust everything with a simple UI. No command line required.",
     "Model, style, aspect ratio, resolution — fine-tune everything with a simple UI. No prompt engineering required."),
    ("Convert and compress. Any format.", "Create in any medium."),
    ("PNG, JPEG, WebP, AVIF, MOV, WebM — drop any file and get it web-ready in seconds.",
     "Images, video, audio, speech and music — describe an idea and get a finished result in seconds."),
    ("Preview before/after", "Preview and refine"),
    ("Compare original vs. compressed side-by-side. Save only when you're happy.",
     "Compare variations side-by-side, then inpaint, upscale or edit until it's exactly right."),
    ("Upload straight to Webflow", "Bring it into your workflow"),
    ("One click to your project's Assets panel. No extra tools, no extra costs.",
     "Chain models into automated workflows, then export anywhere in one click. No extra tools."),
    (">bg-pattern.png<", ">portrait-4k.png<"),
    (">hero-animation.mov<", ">cinematic-clip.mp4<"),
    (">12MB (-99%)<", ">4K · 8s<"),
    (">Before<", ">Prompt<"),
    (">After<", ">Result<"),

    # ---------- Comparison ----------
    ("You shouldn't need a CS degree", "You shouldn't need a studio"),
    ("to compress a file", "to create anything"),
    (">With Squeeze<", ">With ImagineArt<"),
    ("Without squeeze – multiple apps", "Without ImagineArt – juggling tools"),
    ("With squeeze – 1 app", "With ImagineArt – one studio"),
    # without column
    ("Open Handbrake for video, ImageOptim for images", "A separate AI tool for every medium"),
    ("Two apps before you even start", "A new subscription for each task"),
    ("Guess the right settings without preview", "Re-roll prompts with no way to compare"),
    ("10+ tries to get it right", "10+ generations to get it right"),
    ("Too big? Try again", "Wrong style? Start over"),
    ("Clean up leftover files", "Stitch results together by hand"),
    ("Your Desktop is a graveyard", "Your downloads folder is a mess"),
    ("Manually upload image to Webflow dashboard", "Re-upload assets between apps"),
    ("One by one, through the dashboard", "One by one, by hand"),
    ("Embed manually in Webflow", "No way to automate anything"),
    ("Custom HTML embed, copy-paste the URL", "Repeat every step manually"),
    # with column
    ("Drop your file into Squeeze", "Type a prompt into ImagineArt"),
    (">Video or image<", ">Image, video, audio or film<"),
    ("Pick format and quality", "Pick a model and a style"),
    ("MP4, WebM, JPG – you choose", "GPT Image, Flux, Veo – you choose"),
    ("Compress and preview side-by-side", "Generate and compare side-by-side"),
    ("See the result before you save", "See variations before you commit"),
    ("Save locally or upload to Webflow", "Edit, upscale or inpaint in place"),
    (">One click, done<", ">One click, done<"),  # (kept; harmless)
    ("Upload directly to Webflow", "Chain it into a workflow"),
    ("Straight to your project's Assets panel", "Automate every step end to end"),
    ("Copy ready-to-use embed code", "Export anywhere, ready to use"),
    ("No more writing embed code by hand", "No more switching between tools"),

    # ---------- About ----------
    (">We compress<", ">We create<"),
    (">media every day<", ">with AI every day<"),
    ("We're GRAFIT – a digital agency that ships Webflow sites for tech companies.",
     "We're ImagineArt — an AI creative platform trusted by millions of creators worldwide."),
    ("We compress videos and images for client projects every single day.",
     "We generate images, video, audio and film for creators every single day."),
    ("We know exactly how painful the current tools are because we've been using them for years.",
     "We know how scattered creative tools are — so we built one studio that does it all."),
    ("Squeeze is the tool we built for ourselves and decided to share. It's free and native macOS.",
     "ImagineArt brings every generative model into one place. Free to start, no credit card required."),

    # ---------- FAQ ----------
    ("Why not just Handbrake?", "What can I create with ImagineArt?"),
    ("Handbrake is great for video — but it's video only, and there's no side-by-side preview. You guess settings, export, check, repeat. Squeeze handles video and images in one app, with a preview before you save.",
     "ImagineArt generates images, video, audio, speech, music and full films from text prompts — all in one studio. You can also edit, inpaint and upscale existing media without switching tools."),
    ("Why not Squoosh or ImageOptim?", "Which AI models does it support?"),
    ("Squoosh and ImageOptim are images-only. If your project includes video — which most Webflow sites do — you'd still need a separate tool. Squeeze covers both in one place, and connects directly to Webflow so you never leave the app.",
     "ImagineArt brings the best models together — GPT Image, Flux, Imagen, Veo, Kling and more — so you can pick the right one for each task without juggling multiple subscriptions."),
    ("How does the Webflow upload work?", "What are Workflows?"),
    ("Connect once with your Webflow API key. After that, every compressed file uploads straight to your project's Assets panel with a single click — no browser tab switching, no copy-paste, no dashboard.",
     "Workflows let you link models and steps into an automated pipeline — generate an image, animate it into video, add a voiceover, and export — all in one chain you control."),
    ("Is it really free?", "Is it really free to start?"),
    ("Yes, completely free. No trial period, no feature limits, no account required. We built it for our own workflow at GRAFIT and decided to share it.",
     "Yes — you can start creating for free with no credit card required. Paid plans unlock higher resolution, faster generation and full commercial usage when you need it."),
    ("Why native macOS?", "Can I use my creations commercially?"),
    ("Native apps use system codecs and hardware acceleration, which makes encoding significantly faster than Electron or browser-based tools. Tighter OS integration means drag-and-drop, Finder support, and no background processes eating your RAM.",
     "Yes. On a paid plan you get full commercial rights to everything you generate, so you can use ImagineArt for ads, content, products and client work."),
    ("What formats are supported?", "What can I export?"),
    ("Video: MP4 (H.264, H.265), WebM (VP9), MOV. Images: JPEG, PNG, WebP, AVIF. More formats are added with each release — check the changelog for the latest.",
     "Export images, video and audio in high resolution. Upscale to 4K, download in standard formats, or push results straight into your next workflow."),
    ("Will it support Windows / Linux?", "Is there a mobile app?"),
    ("macOS first while we refine the core experience. Windows is next on the roadmap. Leave your email on the site and we'll let you know when it launches.",
     "Yes — Imagine is on iOS and Android, so you can generate and edit on the go with everything synced to your account across web and mobile."),

    # ---------- Final CTA + misc labels ----------
    (">Get<", ">Start<"),
    (">Squeeze<", ">creating<"),
    ("Download the macOS app – free forever, native compression.",
     "Join millions of creators turning ideas into images, video and audio — free to start."),
    (">Download for macOS<", ">Start creating free<"),
    (">Start compression<", ">Start creating<"),
    ("[BY GRAFIT]", "[BY IMAGINE]"),
    (">Get the app<", ">Start creating<"),
]

def flex(old):
    # build a regex that tolerates any whitespace run where old has whitespace
    parts = re.split(r"\s+", old)
    return r"\s+".join(re.escape(p) for p in parts)

misses = []
for old, new in PAIRS:
    pat = re.compile(flex(old))
    n = len(pat.findall(s))
    if n == 0:
        misses.append(old)
        continue
    s = pat.sub(lambda m: new, s)

# Page <title> + key social meta
s = re.sub(r"<title>.*?</title>",
           "<title>ImagineArt — Create Images, Video & Audio with AI</title>", s, flags=re.S)
s = re.sub(r'("og:image:alt"\s+content=")[^"]*(")',
           r"\1Create anything you can imagine with AI\2", s)
s = re.sub(r'("twitter:image:alt"\s+content=")[^"]*(")',
           r"\1Create anything you can imagine with AI\2", s)

io.open(PAGE, "w", encoding="utf-8").write(s)
print("applied:", len(PAIRS) - len(misses), "/", len(PAIRS))
if misses:
    print("MISSES (matched 0):")
    for m in misses:
        print("  ", m)
