#!/usr/bin/env python3
"""Emits /ai-images/guides/ and the ten guide pages.

The prose is lifted verbatim out of the reviewed drafts by extract.py; nothing
here rewrites a sentence. This file only decides structure: which heading opens
a section, where the cards break, and what schema each page carries.
"""
import os, sys, re, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import page, section, BASE
from meta import META, ORDER
from figures import FIGURES

ROOT = sys.argv[1]
SHELL = os.path.dirname(os.path.abspath(__file__))
GUIDES = {g["slug"].rsplit("/", 1)[-1]: g for g in json.load(open(f"{SHELL}/guides.json"))}
FAQ = json.load(open(f"{SHELL}/faq.json"))

# The drafts use a monospace block for the two device tables and the prompt
# skeletons, where the alignment carries the meaning. Nothing on the site did
# that yet, so the rule comes with the pages that need it.
SPEC_CSS = """
    .spec { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .84rem;
      line-height: 1.7; white-space: pre; overflow-x: auto; -webkit-overflow-scrolling: touch;
      max-width: 100%; margin: 0 0 14px; padding: 14px 16px; border: 1px solid var(--line);
      border-radius: 10px; background: rgba(22, 116, 255, .04); color: var(--muted); }
    .spec strong { color: var(--ink); font-weight: 600; }
    .guide-list { list-style: none; margin: 0; padding: 0; }
    .guide-list li { border-top: 1px solid var(--line); padding: 18px 0; }
    .guide-list li:last-child { border-bottom: 1px solid var(--line); }
    .guide-list .lbl { display: inline-block; font-size: .72rem; letter-spacing: .08em;
      text-transform: uppercase; font-weight: 800; color: var(--accent-1); margin-bottom: 6px; }
    .guide-list h3 { margin: 0 0 4px; font-size: 1.06rem; line-height: 1.35; font-family: var(--sans); }
    .guide-list h3 a { color: var(--heading); text-decoration: none; }
    .guide-list h3 a:hover, .guide-list h3 a:focus-visible { text-decoration: underline; }
    .guide-list p { margin: 0; }
    .faq h3 { margin: 22px 0 4px; font-size: 1.02rem; font-family: var(--sans); color: var(--heading); }
    .faq h3:first-child { margin-top: 0; }
    .faq p { margin: 0 0 4px; }
    .shot-wide { margin: 18px 0 6px; }
    .shot-wide img { display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid var(--line); }
    .shot-wide figcaption { padding: 8px 4px 0; color: var(--muted); font-size: 0.88rem; }
    .shot-wide figcaption strong { color: var(--heading); }
    .shot-quad { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 18px 0 6px; }
    .shot-quad figure { margin: 0; }
    .shot-quad img { display: block; width: 100%; height: auto; border-radius: 12px; border: 1px solid var(--line); }
    .shot-quad figcaption { padding: 6px 2px 0; color: var(--muted); font-size: 0.82rem; line-height: 1.45; }
    .shot-quad figcaption strong { color: var(--heading); display: block; }
    @media (max-width: 700px) { .shot-quad { grid-template-columns: 1fr 1fr; } }
"""

def anchor(text):
    t = re.sub(r"<[^>]+>", "", text).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return "-".join(t.split("-")[:6])

def split_body(body):
    """→ (lead paragraphs, [(heading, chunk)])."""
    parts = re.split(r"<h3>(.*?)</h3>", body, flags=re.S)
    lead = parts[0].strip()
    rest = [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
    return lead, rest

def tidy(chunk):
    """Draft markup → site markup. Only the container changes, never the words."""
    return chunk.replace('<div class="spec">', '<pre class="spec">').replace("</div>", "</pre>")

def lead_text(lead):
    m = re.match(r"<p>(.*?)</p>", lead, re.S)
    return m.group(1).strip() if m else ""

NAV = [("Overview", "../../"), ("All guides", "../"), ("Support", "../../../support/ai-image-generator/")]

def build_guide(slug):
    g, m = GUIDES[slug], META[slug]
    url = f"{BASE}/ai-images/guides/{slug}/"
    lead, secs = split_body(g["body"])
    figs = FIGURES.get(slug, {})
    body = []
    for h, c in secs:
        a = anchor(h)
        fig = figs.get(a, "")
        inner = tidy(c) + (("\n" + fig) if fig else "")
        body.append(section(a, f'        <h2 class="display">{h}</h2>\n        <div class="card">\n{inner}\n        </div>'))
    unplaced = set(figs) - {anchor(h) for h, _ in secs}
    if unplaced:
        raise SystemExit(f"{slug}: figures target sections that do not exist: {sorted(unplaced)}")
    head = f'''        <span class="eyebrow">{html.escape(m["label"])}</span>
        <h1 class="display">{g["title"]}</h1>
        <p class="lead">{lead_text(lead)}</p>
        <div class="head-actions">
          <a class="button-soft" href="../">&larr; All guides</a>
          <a class="button-soft" href="../../">The app</a>
        </div>'''
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "TechArticle" if m["label"] == "For developers" else "Article",
             "@id": url + "#article", "headline": re.sub(r"<[^>]+>", "", g["title"]),
             "description": m["desc"], "inLanguage": "en",
             "mainEntityOfPage": url, "url": url,
             "author": {"@type": "Organization", "name": "NovaDev Code Studio", "url": BASE + "/"},
             "publisher": {"@type": "Organization", "name": "NovaDev Code Studio", "url": BASE + "/"},
             "about": {"@type": "SoftwareApplication", "name": "AI Image Generator Anywhere",
                       "applicationCategory": "PhotoApplication", "operatingSystem": "iOS"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "NovaDev Code Studio", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "AI Image Generator Anywhere", "item": BASE + "/ai-images/"},
                {"@type": "ListItem", "position": 3, "name": "Guides", "item": BASE + "/ai-images/guides/"},
                {"@type": "ListItem", "position": 4, "name": re.sub(r"<[^>]+>", "", g["title"]), "item": url}]},
        ]}, indent=2)
    return page(path=f"ai-images/guides/{slug}/index.html",
                title=f'{re.sub(r"<[^>]+>", "", g["title"])} | NovaDev Code Studio',
                desc=m["desc"], canonical=url, depth=3, head=head, sections=body,
                nav=NAV, schema=schema, extra_css=SPEC_CSS,
                cta={"h": "Made on the device, not on a server.",
                     "p": "AI Image Generator Anywhere runs the model on your iPhone or iPad. No account, no credits, no connection required.",
                     "href": "../../", "label": "About the app"})

def build_index():
    url = f"{BASE}/ai-images/guides/"
    rows = "\n".join(
        f'''          <li>
            <span class="lbl">{html.escape(META[s]["label"])}</span>
            <h3><a href="{s}/">{GUIDES[s]["title"]}</a></h3>
            <p>{META[s]["blurb"]}</p>
          </li>''' for s in ORDER)
    faq = "\n".join(f"          <h3>{q}</h3>\n          <p>{a}</p>" for q, a in FAQ)
    secs = [
        section("guides", f'''        <h2 class="display">Ten guides</h2>
        <h3 class="deck">The label on each row says who it is for. Everything is written in plain language except the one marked <em>For developers</em>, which goes into how the model is converted and run &mdash; useful if you build things, skippable if you just want pictures.</h3>
        <div class="card">
          <ul class="guide-list">
{rows}
          </ul>
        </div>'''),
        section("faq", '''        <h2 class="display">Common questions</h2>
        <div class="card faq">
''' + faq + '''
        </div>'''),
    ]
    head = '''        <span class="eyebrow">Guides</span>
        <h1 class="display">On-device AI image generation, <em>explained.</em></h1>
        <p class="lead">Practical guides to generating and editing images on an iPhone or iPad, with the model running on the device rather than on a server. Written to answer the question you arrived with &mdash; what it costs in storage, which devices can do it, how to write a prompt that works &mdash; whether or not you install anything.</p>
        <div class="head-actions">
          <a class="button-soft" href="../">&larr; About the app</a>
        </div>
        <div class="tip" style="max-width:620px;margin:22px auto 0;text-align:left;">
          <strong>The app is coming to the App Store soon.</strong> These guides are
          written to be useful on their own: almost everything here is about how
          on-device generation works, not about one particular app.
        </div>'''
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                {"@type": "Question", "name": re.sub(r"<[^>]+>", "", q),
                 "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                for q, a in FAQ]},
            {"@type": "ItemList", "name": "Guides to on-device AI image generation",
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1,
                  "name": re.sub(r"<[^>]+>", "", GUIDES[s]["title"]),
                  "url": f"{BASE}/ai-images/guides/{s}/"} for i, s in enumerate(ORDER)]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "NovaDev Code Studio", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "AI Image Generator Anywhere", "item": BASE + "/ai-images/"},
                {"@type": "ListItem", "position": 3, "name": "Guides", "item": url}]},
        ]}, indent=2)
    return page(path="ai-images/guides/index.html",
                title="Guides — on-device AI image generation on iPhone and iPad | NovaDev Code Studio",
                desc="Practical guides to generating and editing images on an iPhone or iPad with the model running on the device: which devices qualify, what it costs in storage, how to write prompts that work, and how it compares with cloud tools.",
                canonical=url, depth=2, head=head, sections=secs,
                nav=[("Overview", "../"), ("Support", "../../support/ai-image-generator/")],
                schema=schema, extra_css=SPEC_CSS)

if __name__ == "__main__":
    n = build_index()
    print(f"{'ai-images/guides/index.html':58} {n:6}b")
    for s in ORDER:
        print(f"{'ai-images/guides/' + s + '/index.html':58} {build_guide(s):6}b")
