#!/usr/bin/env python3
"""Stamps every local image URL with a hash of the file it points at.

Assets are served with `cache-control: max-age=14400`, so replacing a picture
in place leaves anyone who already loaded the page looking at the old one for
four hours — which is exactly what happened when the couple with their eyes
shut was swapped out. A URL that changes when the bytes change makes that
impossible, and costs nothing: the query is ignored by the file system and
treated as a distinct URL by the cache.

Run after building. Re-running is safe: existing stamps are replaced, not
appended, so the hash always describes the file as it is now.
"""
import sys, os, re, glob, hashlib

ROOT = sys.argv[1]
pat = re.compile(r'(<img[^>]+src=")([^"]+?)(?:\?v=[0-9a-f]+)?(")')
stamped = skipped = 0

for page in glob.glob(os.path.join(ROOT, "ai-images", "**", "*.html"), recursive=True):
    src = open(page, encoding="utf-8").read()
    base = os.path.dirname(page)

    def repl(m):
        global stamped, skipped
        url = m.group(2)
        if url.startswith(("http", "data:")):
            skipped += 1
            return m.group(0)
        path = os.path.normpath(os.path.join(base, url))
        if not os.path.exists(path):
            skipped += 1
            return m.group(0)
        h = hashlib.md5(open(path, "rb").read()).hexdigest()[:8]
        stamped += 1
        return f"{m.group(1)}{url}?v={h}{m.group(3)}"

    out = pat.sub(repl, src)
    if out != src:
        open(page, "w", encoding="utf-8").write(out)

print(f"stamped {stamped} image urls, skipped {skipped}")
