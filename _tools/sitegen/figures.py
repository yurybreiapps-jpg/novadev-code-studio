"""Figures for the guide pages, keyed by guide slug and section anchor.

Kept apart from the prose, which extract.py lifts verbatim from the reviewed
drafts. A figure is layout; putting it in this file means adding one never
edits a sentence.

Captions state what the picture is evidence of. Where a claim cannot be
supported by the image itself it is not made: the offline guide's picture is
captioned as something a phone drew, not as something drawn in airplane mode,
because nobody recorded whether the radio was off when it was made.
"""

A = "../../../assets/apps/ai-images"        # app screenshots, reused
G = f"{A}/guides"                           # images made for the guides

def _fig(cls, items):
    inner = "\n".join(
        f'''            <figure>
              <img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy">
              <figcaption><strong>{lab}</strong>{(" &middot; " + txt) if txt else ""}</figcaption>
            </figure>''' for src, alt, w, h, lab, txt in items)
    return f'          <div class="{cls}">\n{inner}\n          </div>'

def wide(src, alt, w, h, lab, txt):
    return f'''          <figure class="shot-wide">
            <img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy">
            <figcaption><strong>{lab}</strong> &middot; {txt}</figcaption>
          </figure>'''

FIGURES = {
 "ai-image-generation-offline-iphone": {
   "what-on-device-actually-means": wide(
     f"{G}/offline.webp", "A generated image of a greenhouse standing alone in an empty desert landscape",
     1000, 1000, "Drawn on the device",
     "A phone made this, not a server. That is the whole of the difference &mdash; the picture is the same kind of picture either way."),
 },
 "will-my-iphone-run-on-device-ai-images": {
   "the-number-that-decides-it": wide(
     f"{A}/model-hd.webp", "The model picker in the app showing Photoreal HD selected, with a line saying it needs a newer device",
     1100, 1393, "Said before you commit",
     "The larger model announces what it needs at the moment you pick it, rather than failing after a three-gigabyte download."),
 },
 "upscale-photo-4k-iphone": {
   "resizing-versus-upscaling": wide(
     f"{G}/texture.webp", "A close portrait of a snow leopard, fur and whiskers sharply detailed",
     1000, 1000, "Texture is the thing it rebuilds",
     "Fur, whiskers, the grain of snow: this is the kind of detail an upscaling model has learned, which is why its results look sharp rather than smoothed."),
   "doing-it-on-the-phone-offline": wide(
     f"{A}/enhance.webp", "The Enhance tab in the app, showing an image being taken from 1,536 pixels square to 4,096",
     760, 964, "Enhance, in the app",
     "1,536 pixels square taken to 4,096. The multiplier is a choice, and 1&times; cleans up without enlarging at all."),
 },
 "write-better-ai-image-prompts": {
   "order-matters-more-than-length": _fig("shot-trio", [
     (f"{G}/ex-subject.webp", "A bowl of ramen photographed in warm light with steam rising", 600, 600,
      "Subject, setting, light", "Three things, doing three different jobs."),
     (f"{G}/ex-style.webp", "A neon-lit motorcycle on a wet street at night in a vivid synthetic style", 600, 600,
      "A style, doing the work", "The look came from one style word, not from a pile of adjectives."),
     (f"{G}/ex-geometric.webp", "A tiger's head rendered as flat geometric polygons", 600, 600,
      "The same, geometric", "Ask for a style by name and the model commits to it."),
   ]),
   "a-structure-that-works": wide(
     f"{A}/ideas.webp", "The Ideas sheet in the app, listing written prompt suggestions grouped under a People heading",
     1100, 1109, "Or start from one that works",
     "The app carries written prompts built on this structure. Tapping one fills the box, and you can change any of it before generating."),
   "change-one-thing-at-a-time": _fig("shot-quad", [
     (f"{G}/word-night.webp", "A fox on a park bench under a streetlight at night, drawn close and tight", 460, 460,
      "at night", "A tight portrait."),
     (f"{G}/word-dawn.webp", "The same scene at dawn, the camera further back along a street of autumn trees", 460, 460,
      "at dawn", "Pulls back; autumn colour arrives."),
     (f"{G}/word-fog.webp", "The same scene in fog, the fox small in a wide grey frame", 460, 460,
      "in fog", "Goes wide, fox small."),
     (f"{G}/word-snow.webp", "The same scene in heavy snow, now with two foxes by the bench", 460, 460,
      "in heavy snow", "And a second fox nobody asked for."),
   ]),
 },
 "make-ai-wallpaper-iphone": {
   "prompts-that-reliably-work": _fig("shot-trio", [
     (f"{G}/wall-island.webp", "A library building floating on a rock island above waterfalls and clouds", 600, 600,
      "Calm top and bottom", "Room for the clock above, room for the dock below."),
     (f"{G}/wall-forest.webp", "A white stag standing in a misty, softly lit forest", 600, 600,
      "One subject, quiet edges", "Nothing important near the corners."),
     (f"{G}/wall-terrarium.webp", "A glass terrarium holding small plants, on a plain floor by a window", 600, 600,
      "A single object", "Clean separation from its background, which is what Depth effect needs."),
   ]),
 },
 "stable-diffusion-on-iphone-explained": {
   "making-it-fast-enough-to-be": wide(
     f"{G}/engine-comparison.webp",
     "A comparison sheet: three prompts rendered by stock Stable Diffusion XL at 20 steps beside a distilled model at 8 steps, with the test conditions printed underneath",
     1100, 1884, "Eight steps against twenty",
     "Same prompt, same seed, same negative prompt, both 6-bit Core ML on the Neural Engine. The conditions are printed on the sheet so it can be checked rather than taken on trust."),
 },
 "anime-art-from-text-iphone": {
   "what-works-well": wide(
     f"{G}/anime.webp", "An illustrated scene of a figure on a rooftop looking over a coastal town at sunset",
     1000, 1000, "What it does well",
     "Wide, composed scenes with strong colour and clear light. This is the register a general model holds up in."),
 },
}
