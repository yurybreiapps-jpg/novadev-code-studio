"""Pull the reviewed prose out of the draft batches.

The drafts hold three things per guide: the headline, an internal .intent note
that is planning and must never ship, and the .draft body that is the guide.
Retyping the bodies by hand is how a reviewed sentence quietly becomes a
different sentence, so they are lifted verbatim instead.
"""
import re, json, sys, html

SP = "/private/tmp/claude-501/-Volumes-ExternalDrive-Source-Apple-iOS-a-tennis-ai-coach-ios/658acf6e-d621-4207-9fb8-8b64f828f954/scratchpad"
BATCHES = ["guides-batch-1.html", "guides-batch-2.html", "guides-batch-3.html"]

guide_re = re.compile(r'<section class="guide">(.*?)</section>', re.S)
h2_re    = re.compile(r'<h2>(.*?)</h2>', re.S)
slug_re  = re.compile(r'<span class="slug">(.*?)</span>', re.S)
draft_re = re.compile(r'<div class="draft">(.*?)\n  </div>', re.S)

out = []
for b in BATCHES:
    src = open(f"{SP}/{b}", encoding="utf-8").read()
    for block in guide_re.findall(src):
        h2 = h2_re.search(block); sl = slug_re.search(block); dr = draft_re.search(block)
        if not (h2 and dr):
            print(f"!! could not parse a guide in {b}", file=sys.stderr); continue
        out.append({
            "title": h2.group(1).strip(),
            "slug":  (sl.group(1).strip() if sl else ""),
            "body":  dr.group(1).strip(),
        })

print(f"parsed {len(out)} guides")
for g in out:
    heads = re.findall(r'<h3>(.*?)</h3>', g["body"])
    print(f'  {g["slug"]:58} {len(g["body"]):6}b  {len(heads)} sections')
json.dump(out, open(f"{SP}/sitegen/guides.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
