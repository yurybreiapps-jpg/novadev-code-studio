#!/usr/bin/env python3
"""Generates the AI Image Generator product page and its guides.

The site is hand-written static HTML with the CSS inlined per page, so pages
are emitted from the same shell the existing /a-tennis/guide/ page uses. The
CSS is copied verbatim from that page rather than rewritten, which is the only
way new pages look native without touching the ones that already work.
"""
import os, re, sys, html

ROOT = sys.argv[1]                      # site repo root
SHELL = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(SHELL, "style.css")).read()
FONTS = open(os.path.join(SHELL, "fonts.html")).read().strip()
BASE = "https://www.novadevcodestudio.com"
APP = "AI Image Generator Anywhere"
APP_ICON = "assets/apps/ai-image-generator/app-icon.png"
STORE = "https://apps.apple.com/app/id6805583172"
SOCIAL_ROW = re.search(r'      <div class="social-row".*?</div>\n',
                       open(os.path.join(ROOT, "a-tennis/index.html")).read(), re.S).group(0)

def page(*, path, title, desc, canonical, depth, head, sections, cta=None,
         schema=None, nav=None, og_image="assets/ai-image-generator-banner.png",
         extra_css=""):
    up = "../" * depth
    on_app_page = path == "ai-images/index.html"
    app_open = '<span class="brand-app">' if on_app_page else f'<a class="brand-app" href="{up}ai-images/">'
    app_close = "</span>" if on_app_page else "</a>"
    nav = nav or []
    navhtml = "\n".join(
        f'        <a href="{h}">{html.escape(t)}</a>' for t, h in nav)
    secs = "\n".join(sections)
    ctahtml = f'''
    <section class="cta liquid">
      <div class="container">
        <h2 class="display">{cta['h']}</h2>
        <p class="lead">{cta['p']}</p>
        <p><a class="button-soft" href="{cta['href']}">{cta['label']}</a></p>
      </div>
    </section>''' if cta else ""
    schemahtml = f'''  <script type="application/ld+json">
{schema}
  </script>
''' if schema else ""
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f7f9ff">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE}/{og_image}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="NovaDev Code Studio">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="{up}assets/favicon.png">
{schemahtml}  {FONTS}
  <style>{CSS}{extra_css}</style>
</head>
<body>
  <div class="nav-wrap">
    <header class="topbar">
      <span class="brand-group">
        <a class="brand" href="{up}" aria-label="NovaDev Code Studio home">
          <img src="{up}assets/novadev-logo.png" alt="NovaDev Code Studio logo">
          <span class="brand-text">
            <span class="brand-title">Nova<span>Dev</span></span>
            <span class="brand-subtitle">Code Studio</span>
          </span>
        </a>
        <span class="brand-sep" aria-hidden="true">·</span>
        {app_open}
          <img class="nav-app-icon" src="{up}{APP_ICON}" alt="">
          {APP}
        {app_close}
      </span>
      <nav class="nav" aria-label="Page links">
{navhtml}
        <a class="store-pill" href="{STORE}" target="_blank" rel="noreferrer">App Store</a>
      </nav>
    </header>
  </div>
  <main>
    <section class="page-head liquid">
      <div class="container">
{head}
      </div>
    </section>
{secs}{ctahtml}
  </main>
  <footer class="footer">
    <div class="container footer-grid">
      <a class="footer-brand" href="{up}" aria-label="NovaDev Code Studio home">
        <img src="{up}assets/novadev-logo.png" alt="NovaDev Code Studio logo">
        <span class="brand-text">
          <span class="brand-title">Nova<span>Dev</span></span>
          <span class="brand-subtitle">Code Studio</span>
        </span>
      </a>
      <div class="footer-legal">
        <p>Copyright <span id="currentYear"></span> NovaDev Code Studio &middot; novadevcodestudio.com. All rights reserved.</p>
        <nav class="footer-textlinks" aria-label="Footer links"><a href="mailto:support@novadevcodestudio.com">Support</a></nav>
      </div>
{SOCIAL_ROW}    </div>
  </footer>
  <script>document.getElementById("currentYear").textContent = new Date().getFullYear();</script>
</body>
</html>
'''
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(out)
    return len(out)

def section(sid, inner):
    return f'    <section id="{sid}">\n      <div class="container">\n{inner}\n      </div>\n    </section>'
