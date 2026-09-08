# sitegen — builds /ai-images/ and its guides

Underscore-prefixed, so GitHub Pages keeps it in the repo and leaves it out of
the published site.

## Rebuild everything

    python3 _tools/sitegen/build_product.py .
    python3 _tools/sitegen/build_guides.py .
    python3 _tools/sitegen/stamp.py .

`stamp.py` runs **last, every time**. Assets are served with
`cache-control: max-age=14400`, so a picture replaced in place leaves anyone
who already loaded the page looking at the old one for four hours. Stamping
appends `?v=<md5[:8]>` to each image url, so changed bytes mean a changed url.
Re-running replaces stamps rather than appending them.

## Where things live

| file | what it holds |
|---|---|
| `gen.py` | the page shell: head, nav, footer, schema, CSS inlining |
| `style.css` | copied verbatim from `/a-tennis/guide/`. Don't rewrite it — copying is why new pages look native |
| `build_product.py` | `/ai-images/` — sections, app screenshots, SoftwareApplication schema |
| `build_guides.py` | `/ai-images/guides/` and the ten guide pages |
| `guides.json` | the guide prose, **extracted, not typed** |
| `extract.py` | regenerates `guides.json` from the reviewed draft HTML |
| `meta.py` | per-guide title, audience label, meta description, index order |
| `figures.py` | which picture goes under which section, keyed by slug + anchor |
| `faq.json` | the 14 FAQ pairs behind the FAQPage schema |

## Rules worth keeping

**Prose is lifted, never retyped.** `extract.py` pulls guide bodies verbatim
out of the drafts. Retyping is how a reviewed sentence quietly becomes a
different sentence. To change a guide, edit the draft and re-extract, or edit
the built HTML directly — but don't paraphrase from memory.

**Screenshots come from `shots-1.1.0/`,** the real-iPad set submitted to the
store. The older `shots/screenshots/` set is 1.0 — three tabs, old prompt box
— and 1.0 was never public. Crop every iPad capture to keep y 62..2680: 62
clears the status bar, 2680 drops the macOS window resize handle.

**Check numbers against the app, not the drafts.** Two were already wrong once:
the free allowance is fifty (`Store.freeAllowance`), not the ten the drafts
said, and the bundled upscaler is a 33 MB package, not the 31 MB of its weight
file alone. The price is not in the repo at all — it lives in App Store
Connect — so no page states a figure.

**`figures.py` fails loudly** if a figure names a section anchor that doesn't
exist, so renaming a heading can't silently drop a picture.

## Still pending

Four places say "coming soon" and change on approval day: the notice on
`/ai-images/`, the notice on `/ai-images/guides/`, the `Coming soon` tag on the
home card, and the App Store links (none exist yet). Re-check the store with
`itunes.apple.com/lookup?id=6805583172` before flipping them.
