"""Builds the PhotoMuse pages for novadevcodestudio.com.

The look is not redesigned here: each page takes the <style> of the page it is
modelled on (the tennis guide for the app pages, the Lustless policy pages for
privacy and support), so the site stays one site.

Everything said about the app was checked against its source on 2026-09-21.
The free allowance (5 groups, 5 enhanced photos, 2 compressed videos) comes
from FreeAllowance in Core/Store.swift — change it there, change it here.

FLIP-ON-LAUNCH marks the places that say "coming soon". When the app is
approved, set LIVE = True and run this again.
"""
import difflib, pathlib, re, sys

# Safe to run: the default is a dry run that diffs what this script would
# produce against what is live and writes nothing. --diff shows how, --write
# writes. It earned that guard - the pictures, the install link, the tour clip
# and the two-part header and footer were all added to the live pages by hand
# after this script was written, and running it would have deleted every one.
# They are all in here now (FIGURES, TOUR, topbar, footer), and a plain run
# reports "reproduces every live page exactly". If it ever stops saying that,
# something was hand-edited again: port it in here before writing.
SITE = pathlib.Path("/Volumes/ExternalDrive/Source/novadev-code-studio")
LIVE = True  # launched 2026-09-24
STORE = "https://apps.apple.com/app/id6814026340"
UPDATED = "21 September 2026"

def style_of(path):
    html = (SITE / path).read_text()
    return re.search(r"<style>.*?</style>", html, re.S).group(0)

APP_STYLE = style_of("a-tennis/guide/index.html")
DOC_STYLE = style_of("privacy/lustless/index.html")
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">'

def head(title, desc, path, up, og_desc=None, ld=None, style=APP_STYLE):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f7f9ff">
  <link rel="canonical" href="https://www.novadevcodestudio.com/{path}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc or desc}">
  <meta property="og:url" content="https://www.novadevcodestudio.com/{path}">
  <meta property="og:image" content="https://www.novadevcodestudio.com/assets/apps/photomuse/app-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="NovaDev Code Studio">
  <meta name="twitter:card" content="summary">
  <link rel="icon" type="image/png" href="{up}assets/favicon.png">
{('  <script type="application/ld+json">' + ld + '</script>') if ld else ''}
  {FONTS}
  {style}
</head>
'''

def store_pill():
    if LIVE: return f'<a class="store-pill" href="{STORE}" target="_blank" rel="noreferrer">App Store</a>'
    return '<!-- FLIP-ON-LAUNCH --><span class="store-pill" style="opacity:.78">Coming soon</span>'

def store_badge(up):
    if LIVE:
        return f'<a class="store-badge-link" href="{STORE}" target="_blank" rel="noreferrer" aria-label="Download PhotoMuse on the App Store"><img src="{up}assets/store/app-store-badge.png" alt="Download on the App Store"></a>'
    return '<!-- FLIP-ON-LAUNCH --><span class="button-dark" style="cursor:default">Coming soon to the App Store</span>'

def topbar(up, home, links):
    """The two-part header the tennis pages have: the studio mark, which is
    the way back to the home page, then the app. `home` is the app's own page,
    so on the sub-pages the app half links back to it; on the app's own page
    it is not a link at all."""
    nav = "\n".join(f'        <a href="{h}">{t}</a>' for t, h in links)
    on_app_page = home in ("./", "")
    app_open = '<span class="brand-app">' if on_app_page else f'<a class="brand-app" href="{home}">'
    app_close = "</span>" if on_app_page else "</a>"
    return f'''  <div class="nav-wrap">
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
          <img class="nav-app-icon" src="{up}assets/apps/photomuse/app-icon.webp" alt="">
          PhotoMuse
        {app_close}
      </span>
      <nav class="nav" aria-label="Page links">
{nav}
        {store_pill()}
      </nav>
    </header>
  </div>
'''

SOCIAL_ROW = re.search(r'      <div class="social-row".*?</div>\n',
                       (SITE / "a-tennis/index.html").read_text(), re.S).group(0)

def footer(up):
    """The tennis footer: the studio mark (a second way home), the legal line
    with this app's own links, and the social row — which is read from the
    tennis home page rather than copied here, so one edit changes them all."""
    return f'''  <footer class="footer">
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
        <nav class="footer-textlinks" aria-label="Footer links"><a href="{up}support/photomuse/">Help</a> <a href="{up}privacy/photomuse/">Privacy</a> <a href="mailto:support@novadevcodestudio.com">Support</a></nav>
      </div>
{SOCIAL_ROW}    </div>
  </footer>
  <script>document.getElementById("currentYear").textContent = new Date().getFullYear();</script>
</body>
</html>
'''

# The figure and clip styles the tennis guide's stylesheet does not carry.
# APP_STYLE brings the header, footer and .shot-pair/.shot-trio/.shot-solo
# rules with it; these are the ones added for these pages alone.
OVERVIEW_STYLE = """    .shot-wide { margin: 18px 0 6px; }
    .shot-wide img { display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid var(--line); }
    .shot-wide figcaption { padding: 8px 4px 0; color: var(--muted); font-size: 0.88rem; }
    .shot-wide figcaption strong { color: var(--heading); }
"""

GUIDE_STYLE = """    .shot-half { max-width: 460px; margin: 18px auto 6px; }
    .shot-half img, .shot-strip img { display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid var(--line); }
    .shot-half figcaption, .shot-strip figcaption { padding: 8px 4px 0; color: var(--muted); font-size: 0.9rem; text-align: center; }
    .shot-half figcaption strong, .shot-strip figcaption strong { color: var(--heading); }
    .shot-strip { max-width: 560px; margin: 18px auto 6px; }
"""

TOUR_STYLE = """    /* The tour clip under the hero. Portrait, so it is capped to about a
       phone's width rather than stretched across a desktop page. */
    .tour { display: flex; justify-content: center; margin: 2px 0 34px; }
    .tour video { width: 100%; max-width: 300px; height: auto; display: block;
                  border-radius: 26px; border: 1px solid var(--line);
                  box-shadow: 0 20px 52px rgba(0,0,0,.16); background: #14110F; }
"""

# With the studio wordmark showing, this app's seven menu items need up to
# 948px on one line and the inherited bar stops at 880, which left the last of
# them on a second line. Measured in the browser 2026-10-01: overview 948,
# guide 927. Below 1,100 the inherited sheet drops the wordmark, and it fits.
HEADER_STYLE = """    .topbar { width: min(100%, 960px); }
"""

def with_style(html, *blocks):
    """Puts extra rules at the end of the page's <style>, so they win over the
    inherited sheet rather than being overridden by it."""
    i = html.rindex("</style>")
    return html[:i].rstrip(" ") + "".join(blocks) + "  " + html[i:]

TOUR = """
    <section class="tour-clip">
      <div class="container">
        <div class="tour">
          <video controls playsinline muted autoplay loop preload="metadata"
            poster="../assets/apps/photomuse/tour-poster.jpg"
            src="../assets/apps/photomuse/tour.mp4"
            aria-label="PhotoMuse counting a photo library into piles, grouping the same moment twice, and a month sorted by swiping left to delete and right to keep"></video>
        </div>
      </div>
    </section>
"""

# The pictures on the app pages, keyed by the card or step they follow.
# Extracted from the live pages on 2026-09-28, when this script was brought
# back into line with them; before that it would have deleted every one.
FIGURES = {
    'Sorts the clutter into piles':
        '          <div class="shot-pair">\n            <figure>\n              <img src="../assets/apps/photomuse/piles.webp" alt="The home screen: nine piles, each with how many items it holds and how much room they take" width="880" height="1173" loading="lazy">\n              <figcaption><strong>Nine piles</strong> &middot; Counted and measured, never estimated.</figcaption>\n            </figure>\n            <figure>\n              <img src="../assets/apps/photomuse/badshots.webp" alt="The bad shots pile, each photo labelled blurry or too dark with its size" width="880" height="1173" loading="lazy">\n              <figcaption><strong>Bad shots</strong> &middot; Each one says what is wrong with it.</figcaption>\n            </figure>\n          </div>',
    'Picks a keeper, and lets you overrule it':
        '          <div class="shot-pair">\n            <figure>\n              <img src="../assets/apps/photomuse/similar.webp" alt="Similar shots grouped, with the suggested keeper marked in each group" width="880" height="1173" loading="lazy">\n              <figcaption><strong>Similar shots</strong> &middot; The suggested keeper is marked; tap any photo to change its mind.</figcaption>\n            </figure>\n            <figure>\n              <img src="../assets/apps/photomuse/duplicates.webp" alt="Exact duplicates grouped, showing how much each group frees" width="880" height="1173" loading="lazy">\n              <figcaption><strong>Duplicates</strong> &middot; The same picture saved twice, with what each group frees.</figcaption>\n            </figure>\n          </div>',
    'Review a month by swiping':
        '          <figure class="shot-wide">\n            <img src="../assets/apps/photomuse/review.webp" alt="The swipe review: a photo mid-swipe marked for deletion, with the month\'s progress above" width="1040" height="1387" loading="lazy">\n            <figcaption><strong>Review a month</strong> &middot; Nothing goes until you finish and confirm.</figcaption>\n          </figure>',
    'Search by what is in the photo':
        '          <figure class="shot-wide">\n            <img src="../assets/apps/photomuse/search.webp" alt="Everything else, month by month, with a search field reading what is in each picture" width="1040" height="1387" loading="lazy">\n            <figcaption><strong>Everything else</strong> &middot; Month by month, searchable by what is in the picture.</figcaption>\n          </figure>',
    'Enhance, not just delete':
        '          <figure class="shot-wide">\n            <img src="../assets/apps/photomuse/enhance.webp" alt="Enhance with a before and after slider across a photo, Auto applied, and the dials below" width="1040" height="1387" loading="lazy">\n            <figcaption><strong>Enhance</strong> &middot; Auto sets light and colour; every dial still moves by hand.</figcaption>\n          </figure>',
    'Compress videos &mdash; only when it helps':
        '          <div class="shot-pair">\n            <figure>\n              <img src="../assets/apps/photomuse/compress.webp" alt="The compress list: each video with its own estimated saving" width="880" height="1173" loading="lazy">\n              <figcaption><strong>Compress</strong> &middot; Only the videos that really shrink, each with its own estimate.</figcaption>\n            </figure>\n            <figure>\n              <img src="../assets/apps/photomuse/bigvideos.webp" alt="Large videos grouped by size, biggest first" width="880" height="1173" loading="lazy">\n              <figcaption><strong>Large videos</strong> &middot; Grouped by size, the biggest first.</figcaption>\n            </figure>\n          </div>',
    'A real iPad app.':
        '        <figure class="shot-solo">\n          <img src="../assets/apps/photomuse/iphone-home.webp" alt="The same piles on iPhone" width="520" height="1125" loading="lazy">\n          <figcaption><strong>On iPhone too</strong> &middot; Every screen above is the iPad; this is the same app on a phone.</figcaption>\n        </figure>',
    'Photo access, the first scan, and what the numbers mean.':
        '          <figure class="shot-half"><img src="../../assets/apps/photomuse/piles.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>The first screen.</strong> Every pile, with its real size.</figcaption></figure>',
    'Screenshots, screen recordings, bad shots, large videos and Live Photos.':
        '          <div class="shot-trio"><figure><img src="../../assets/apps/photomuse/screenshots.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>Screenshots.</strong> Nothing is picked for you.</figcaption></figure><figure><img src="../../assets/apps/photomuse/badshots.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>Bad shots.</strong> Each one says what was measured.</figcaption></figure><figure><img src="../../assets/apps/photomuse/bigvideos.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>Large videos.</strong> Grouped by size, biggest first.</figcaption></figure></div>',
    'Groups of near-identical photos, with a suggested keeper.':
        '          <div class="shot-pair"><figure><img src="../../assets/apps/photomuse/similar.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>Similar shots.</strong> A suggested keeper in every group.</figcaption></figure><figure><img src="../../assets/apps/photomuse/duplicates.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>Duplicates.</strong> The same picture more than once.</figcaption></figure></div>',
    'The fastest way through everything that is not in a pile.':
        '          <div class="shot-pair"><figure><img src="../../assets/apps/photomuse/review.webp" alt="" width="1040" height="1387" loading="lazy"><figcaption><strong>Swipe left</strong> to delete.</figcaption></figure><figure><img src="../../assets/apps/photomuse/review-keep.webp" alt="" width="1040" height="1387" loading="lazy"><figcaption><strong>Swipe right</strong> to keep.</figcaption></figure></div>',
    'Find the cat, the beach or the tennis match without scrolling.':
        '          <figure class="shot-half"><img src="../../assets/apps/photomuse/search.webp" alt="" width="1040" height="1387" loading="lazy"><figcaption><strong>Type a plain word.</strong> The matches come up, read on your device.</figcaption></figure>',
    'Auto, the dials, Rebuild detail, and the two ways to save.':
        '          <div class="shot-pair"><figure><img src="../../assets/apps/photomuse/enhance.webp" alt="" width="1040" height="1387" loading="lazy"><figcaption><strong>Before and after</strong>, with the slider in between.</figcaption></figure><figure><img src="../../assets/apps/photomuse/enhance-portrait.webp" alt="" width="1040" height="1387" loading="lazy"><figcaption><strong>Auto</strong> first, then any dial by hand.</figcaption></figure></div>',
    'Smaller files for the videos you want to keep.':
        '          <figure class="shot-half"><img src="../../assets/apps/photomuse/compress.webp" alt="" width="880" height="1173" loading="lazy"><figcaption><strong>An estimate first</strong>, the real saving at the end.</figcaption></figure>',
    'The step every cleaner app skips telling you about.':
        '          <figure class="shot-strip"><img src="../../assets/apps/photomuse/freeing-space.webp" alt="" width="900" height="342" loading="lazy"><figcaption>The app says it before you delete: the space comes back <strong>once Recently Deleted is emptied</strong>.</figcaption></figure>',
}


def card(title, *paras):
    body = "\n".join(f"          <p>{p}</p>" for p in paras)
    shot = FIGURES.get(title, "")
    if shot:
        body += "\n" + shot
    return f'        <div class="card">\n          <h3>{title}</h3>\n{body}\n        </div>\n'

# ------------------------------------------------------------------ overview
LD = '''
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "PhotoMuse: Photo Cleaner",
    "operatingSystem": "iOS, iPadOS",
    "applicationCategory": "UtilitiesApplication",
    "description": "Finds similar shots, duplicates, bad photos and oversized videos, lets you review a month by swiping, enhances photos and compresses videos. Everything happens on the device; nothing is collected.",
    "url": "https://www.novadevcodestudio.com/photomuse/",
    "installUrl": "https://apps.apple.com/app/id6814026340",
    "author": { "@type": "Organization", "name": "NovaDev Code Studio" }
  }
  '''
overview = head(
    "PhotoMuse: Photo Cleaner — clear duplicates, swipe to sort, enhance, free up space",
    "PhotoMuse finds similar shots, duplicates, bad photos and oversized videos, lets you sort a month by swiping, enhances photos and compresses videos. All on your device. No account, no tracking.",
    "photomuse/", "../", og_desc="Clear duplicates and bad shots, sort by swiping, enhance photos, shrink videos. Nothing leaves your device.", ld=LD)
overview += "<body>\n" + topbar("../", "./", [("What it does", "#what"), ("iPad", "#ipad"), ("Private", "#private"), ("Free and Plus", "#price"), ("Guide", "guide/"), ("Compare", "compare/")])
overview += f'''  <main>
    <section class="page-head liquid">
      <div class="container">
        <span class="eyebrow">iPhone &amp; iPad</span>
        <h1 class="display">A photo library you can <em>find things in.</em></h1>
        <p class="lead">PhotoMuse finds the similar shots, duplicates, bad photos and oversized videos,
        lets you sort a whole month by swiping, makes the keepers look better, and shrinks the videos
        you want to keep &mdash; all on your device, with no account and no tracking.</p>
        <div class="head-actions">
          {store_badge("../")}
          <a class="button-soft" href="guide/">Read the guide →</a>
        </div>
      </div>
    </section>
{TOUR}
    <section id="what">
      <div class="container">
        <h2 class="display">What it <em>does.</em></h2>
        <h3 class="deck">Nine piles, a swipe review, search, Enhance and video compression.</h3>
{card("Sorts the clutter into piles",
      "Similar shots, duplicates, bad shots (blurred, too dark, a thumb in the way), screenshots, screen recordings, large videos, Live Photos &mdash; and everything else, month by month.",
      "Every pile shows how many items it holds and how much room they take. The sizes are read from your library, byte for byte, not estimated.")}
{card("Picks a keeper, and lets you overrule it",
      "Nearly identical photos are grouped and PhotoMuse suggests the one worth keeping. Take its pick, keep them all, or switch any photo yourself.")}
{card("Review a month by swiping",
      "Left to delete, right to keep. Swiping only marks &mdash; nothing is deleted until you finish and confirm. Undo goes back as far as you like, and your place is saved, so a long month can be done over several days.")}
{card("Search by what is in the photo",
      "Type <em>cat</em>, <em>beach</em> or <em>tennis</em> and see the photos and videos that contain it. The reading is done on your device.")}
{card("Enhance, not just delete",
      "Auto sets light and colour for the photo in front of you; every dial can be moved by hand. Rebuild detail sharpens fine detail and clears compression noise. Save a copy, or replace the original &mdash; Photos keeps the untouched one, so Revert always works.",
      "Enhanced photos stay in the format they came in. An HEIC is not quietly turned into a JPEG twice the size.")}
{card("Compress videos &mdash; only when it helps",
      "Re-encoding an already efficient video makes it <strong>bigger</strong>. PhotoMuse asks Apple's encoder first and lists only the videos that will really shrink, each with its own estimate, then shows the real saving afterwards. HDR video stays HDR.")}
{card("Honest about what frees space",
      "Deleting in any app only moves photos to Recently Deleted, where they sit for 30 days and still take up room. PhotoMuse says so, and takes you to Photos to finish the job.")}
      </div>
    </section>

    <section id="ipad">
      <div class="container">
        <h2 class="display">A real <em>iPad app.</em></h2>
        <p class="lead">Laid out for the big screen in every orientation, not a stretched phone app.
        One purchase covers iPhone and iPad on the same Apple&nbsp;ID.</p>
{FIGURES["A real iPad app."]}
      </div>
    </section>

    <section id="private">
      <div class="container">
        <h2 class="display">Private <em>by design.</em></h2>
{card("Your photos never leave your device",
      "Finding duplicates, judging bad shots, search, Enhance and compression all run on your iPhone or iPad. There is no server on our side to send a photo to.")}
{card("No account, no analytics, no tracking",
      "No sign-in, no advertising, no analytics library, no tracking prompt. We could not identify you from anything we hold, because we hold nothing. The <a href='../privacy/photomuse/'>privacy policy</a> is short because there is little to say.")}
{card("You choose what it can see",
      "Give access to the whole library, or only to the photos you pick. PhotoMuse works with whatever you allow and tells you which it is counting.")}
      </div>
    </section>

    <section id="price">
      <div class="container">
        <h2 class="display">Free and <em>Plus.</em></h2>
        <p class="lead"><strong>Free, with no time limit:</strong> scanning, every pile, search, the swipe
        review, and deleting photos you pick by hand &mdash; as many as you like. Also free to try: cleaning
        5 similar or duplicate groups, enhancing 5 photos and compressing 2 videos.</p>
        <p class="lead" style="margin-top:14px"><strong>Plus</strong> is for doing it in bulk: select a whole pile
        or month at once, clean every group, and enhance and compress without a limit. Weekly, yearly with a
        7-day free trial, or a one-time lifetime purchase. Prices are shown in the app and on the App Store.</p>
        <p class="lead" style="margin-top:16px"><a href="compare/" style="font-weight:700; color: var(--accent-1);">See how that compares with the other photo cleaners &rarr;</a> &mdash; what they charge, and what their privacy labels say.</p>
        <div class="tip">Subscriptions are billed by Apple and can be cancelled at any time in your Apple&nbsp;ID settings. Lifetime is paid once; there is nothing to renew.</div>
      </div>
    </section>

    <section class="cta liquid">
      <div class="container">
        <span class="eyebrow">Ready when you are</span>
        <h2 class="display">Get your library <em>back.</em></h2>
        <div class="head-actions">
          {store_badge("../")}
          <a class="button-soft" href="guide/">The guide</a>
          <a class="button-soft" href="../support/photomuse/">Help</a>
        </div>
      </div>
    </section>
  </main>
''' + footer("../")
overview = with_style(overview, TOUR_STYLE, OVERVIEW_STYLE, HEADER_STYLE)

# --------------------------------------------------------------------- guide
def step(num, sid, title, deck, body):
    return f'''    <section id="{sid}">
      <div class="container">
        <div class="step-head"><span class="step-num">{num}</span><h2 class="display">{title}</h2></div>
        <h3 class="deck">{deck}</h3>
        <div class="card">
{body}{FIGURES.get(deck, "") and chr(10) + FIGURES[deck]}
        </div>
      </div>
    </section>

'''
def ul(*items): return "          <ul>\n" + "\n".join(f"            <li>{i}</li>" for i in items) + "\n          </ul>"
def ol(*items): return "          <ol>\n" + "\n".join(f"            <li>{i}</li>" for i in items) + "\n          </ol>"
def p(text): return f"          <p>{text}</p>"
def tip(text): return f'          <div class="tip">{text}</div>'

guide = head(
    "How to use PhotoMuse — the complete guide to cleaning your photo library",
    "Step by step: clear similar shots and duplicates, review a month by swiping, search your photos, enhance them, compress videos, and actually free the space on your iPhone or iPad.",
    "photomuse/guide/", "../../")
guide += "<body>\n" + topbar("../../", "../", [("Piles", "#piles"), ("Swipe review", "#review"), ("Enhance", "#enhance"), ("Videos", "#compress"), ("Free space", "#finish"), ("Help", "#troubleshooting")])
guide += f'''  <main>
    <section class="page-head liquid">
      <div class="container">
        <span class="eyebrow">The complete guide</span>
        <h1 class="display">From a full phone to a <em>tidy library.</em></h1>
        <p class="lead">Everything in one place: the piles, similar shots and duplicates, the swipe review,
        search, Enhance, video compression &mdash; and the last step most people miss, which is the one that
        actually frees the space.</p>
        <div class="head-actions">
          <a class="button-soft" href="../">← App overview</a>
          <a class="button-soft" href="../../support/photomuse/">Common questions</a>
        </div>
      </div>
    </section>

''' + step("01", "start", "Let it <em>look.</em>", "Photo access, the first scan, and what the numbers mean.", "\n".join([
    p("<strong>Allow photo access.</strong> Choose <em>Full Access</em> to have the whole library sorted, or pick only some photos &mdash; PhotoMuse works with whatever you allow, and says which it is counting. You can change this later in Settings → Privacy &amp; Security → Photos."),
    p("<strong>The first scan</strong> runs on your device and nothing is uploaded. A large library takes a few minutes; you can start using the piles that are ready while the rest are still being counted."),
    p("<strong>The numbers are real.</strong> Sizes are read from your library byte for byte. Where a figure is an estimate, the app says so."),
    tip("<strong>Nothing is ever deleted on its own.</strong> Every delete is confirmed by you in Apple's own sheet, and can be undone in Photos for 30 days."),
])) + step("02", "piles", "Clear the <em>piles.</em>", "Screenshots, screen recordings, bad shots, large videos and Live Photos.", "\n".join([
    ol("Open a pile from the first screen.",
       "Tap the items you do not want. Tap a preview to see it full size first &mdash; videos and Live Photos play there.",
       "Use <strong>Sort</strong> to order by date, size or name. <strong>Large videos</strong> are grouped by size &mdash; over 1&nbsp;GB, over 500&nbsp;MB and so on &mdash; because a handful of files is usually most of the space.",
       "Delete, and confirm in Apple's sheet."),
    p("<strong>Bad shots</strong> are photos that are blurred, too dark, or have a finger over the lens. Glance through before deleting &mdash; a dark photo can still be one you love."),
    tip("Picking photos by hand and deleting them is free and unlimited. <strong>Select all</strong> &mdash; for a whole pile, month or size group at once &mdash; is part of Plus."),
])) + step("03", "similar", "Similar shots &amp; <em>duplicates.</em>", "Groups of near-identical photos, with a suggested keeper.", "\n".join([
    p("<strong>Duplicates</strong> are the same picture more than once. <strong>Similar shots</strong> are the six tries at one group photo. Each group shows how much room the extras take."),
    ul("<strong>Keep only our pick</strong> keeps the photo PhotoMuse judges best and marks the rest.",
       "<strong>Keep all</strong> leaves the group alone.",
       "To decide yourself, tap the badge on any photo to switch it between keep and delete. Tap the photo to see it large."),
    p("An enhanced copy you saved earlier will show up next to its original here &mdash; that is correct, they are the same picture. Keep whichever you prefer."),
])) + step("04", "review", "Review a month by <em>swiping.</em>", "The fastest way through everything that is not in a pile.", "\n".join([
    ol("Open <strong>Everything else</strong> and choose a month.",
       "<strong>Swipe left to delete, right to keep.</strong> The two buttons underneath do the same.",
       "Made a mistake? <strong>Undo</strong> goes back one step at a time, as far as you like &mdash; even after closing the app.",
       "Tap <strong>Done</strong> whenever you like. Your place is saved; the month shows how many are sorted.",
       "At the end, review what you marked and confirm. Only then is anything deleted."),
    p("<strong>Start this month over</strong>, under More, clears the month's marks if you want a fresh run."),
    tip("The swipe review is free, all of it."),
])) + step("05", "search", "Search by what is <em>in the photo.</em>", "Find the cat, the beach or the tennis match without scrolling.", "\n".join([
    p("In <strong>Everything else</strong>, type a plain word: <em>cat</em>, <em>dog</em>, <em>beach</em>, <em>food</em>, <em>tennis</em>, <em>car</em>. Photos and videos that contain it are shown."),
    p("This works by reading your photos <strong>on your device</strong>. The first read of a large library takes a while; after that, search is instant. If a word finds nothing, <strong>Search Photos instead</strong> hands the same word to Apple's Photos app."),
])) + step("06", "enhance", "Enhance a <em>photo.</em>", "Auto, the dials, Rebuild detail, and the two ways to save.", "\n".join([
    ol("Open any photo and tap <strong>Enhance</strong> &mdash; or use <strong>Enhance a photo</strong> on the first screen.",
       "<strong>Auto</strong> sets light and colour for that particular photo. Every dial can then be moved by hand, and <strong>Reset</strong> puts them back.",
       "<strong>Rebuild detail</strong> sharpens fine detail and clears compression noise. It runs on your device and takes a little while on a large photo.",
       "Save as a <strong>new photo</strong>, or <strong>Replace original</strong>."),
    p("<strong>Replacing is not destructive.</strong> Photos keeps the untouched original alongside the edit, exactly as it does for its own edits. To put it back: open the photo in Photos → Edit → Revert."),
    p("<strong>Live Photos</strong> can only be saved as a copy, because replacing one would drop the movement."),
    tip("<strong>File format:</strong> Settings → <em>Save enhanced photos as</em>. <em>Match the Original</em> keeps each photo in the format it already has. <em>High Efficiency</em> always saves HEIC (about half the size of a JPEG); <em>Most Compatible</em> always saves JPEG."),
])) + step("07", "compress", "Compress <em>videos.</em>", "Smaller files for the videos you want to keep.", "\n".join([
    p("Re-encoding a video that is already efficient makes it <strong>bigger</strong>, so <strong>Compress videos</strong> first asks Apple's encoder about each one and lists only those that will really shrink. Each shows its own estimate; slow-motion clips and videos that are not on the device are left alone, and the app says why."),
    ol("Pick a video and a size: the same resolution, or 1080p for anything larger.",
       "Wait for it to finish. You can stop at any time and nothing changes.",
       "See the <strong>real</strong> saving, then choose <strong>Keep both</strong> or <strong>Delete the original</strong>."),
    p("HDR video stays HDR. If the finished file is not meaningfully smaller, PhotoMuse throws it away and keeps your original."),
])) + step("08", "finish", "Actually free <em>the space.</em>", "The step every cleaner app skips telling you about.", "\n".join([
    p("Deleting a photo &mdash; in any app, including Photos &mdash; moves it to <strong>Recently Deleted</strong>, where it stays for 30 days and <strong>still takes up room</strong>. Your storage does not change until that album is emptied."),
    ol("In PhotoMuse, open <strong>Settings → Finish freeing space in Photos</strong>. Apple gives apps no way to open that album directly, so this opens Photos with it searched for.",
       "In Photos, open <strong>Recently Deleted</strong> (it asks for Face&nbsp;ID or your passcode).",
       "Tap <strong>Select → Delete All</strong>."),
    tip("<strong>Changed your mind?</strong> Until you empty it, anything you deleted can be recovered from that same album."),
])) + step("09", "troubleshooting", "If something's <em>not working.</em>", "The usual causes, and what to do.", "\n".join([
    ul("<strong>&ldquo;I deleted thousands of photos and my storage did not change&rdquo;</strong> &mdash; they are in Recently Deleted. See step 08.",
       "<strong>The piles look too small</strong> &mdash; PhotoMuse may only have access to some photos. The first screen says so; tap <strong>Change</strong>, or allow Full Access in Settings → Privacy &amp; Security → Photos.",
       "<strong>&ldquo;Your library has changed&rdquo;</strong> &mdash; you took or deleted photos since the last scan. Tap <strong>Check again</strong>, or turn on <em>Check again automatically</em> in Settings.",
       "<strong>Enhance or Compress is slow to start</strong> &mdash; with iCloud Photos and <em>Optimise iPhone Storage</em> on, the full-size original is fetched from your iCloud first. Wi-Fi helps.",
       "<strong>A video is not offered for compression</strong> &mdash; it is already efficient, it is slow-motion, or the original is only in iCloud. The screen lists how many were left alone for each reason.",
       "<strong>Plans will not load on the Plus screen</strong> &mdash; that needs a connection to the App Store. Try again on Wi-Fi.",
       "Still stuck? Email <a href='mailto:support@novadevcodestudio.com'>support@novadevcodestudio.com</a> &mdash; it reaches a person."),
])) + f'''    <section class="cta liquid">
      <div class="container">
        <span class="eyebrow">That is all of it</span>
        <h2 class="display">Go and <em>clear some space.</em></h2>
        <div class="head-actions">
          {store_badge("../../")}
          <a class="button-soft" href="../">About the app →</a>
        </div>
      </div>
    </section>
  </main>
''' + footer("../../")
guide = with_style(guide, GUIDE_STYLE, HEADER_STYLE)

# ------------------------------------------------------- privacy and support
def doc_page(kind, h1, intro_html, sections, stamp=None):
    title = {"privacy": "Privacy Policy — PhotoMuse | NovaDev Code Studio", "support": "Help — PhotoMuse | NovaDev Code Studio"}[kind]
    desc = {"privacy": "PhotoMuse collects nothing. Your photos are analysed on your device and never uploaded; there is no account, no analytics and no tracking.",
            "support": "Answers about PhotoMuse: storage that did not change, getting a photo back, iCloud photos, Enhance, video compression, and PhotoMuse Plus."}[kind]
    out = head(title, desc, f"{kind}/photomuse/", "../../", style=DOC_STYLE).replace(FONTS, '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  ' + FONTS)
    out += f'''<body>
  <div class="wrap">
    <header>
      <a class="brand-home" href="../../" aria-label="NovaDev Code Studio home">
        <img class="logo" src="../../assets/novadev-logo.png" alt="NovaDev Code Studio logo">
        <span>
          <span class="brand-title">Nova<span>Dev</span></span><br>
          <span class="brand-subtitle">Code Studio</span>
        </span>
      </a>
      <h1>{h1}</h1>
{intro_html}
    </header>
'''
    if stamp: out += f'\n    <p class="stamp">Last updated {stamp}</p>\n'
    for h2, paras in sections:
        out += '\n    <section class="card">\n      <h2>' + h2 + '</h2>\n'
        for para in paras:
            out += (f'      <p class="lede">{para[1:]}</p>\n' if para.startswith("!") else f'      <p>{para}</p>\n')
        out += '    </section>\n'
    return out

LUSTLESS_DOC_TAIL = re.search(r"(\n    <footer.*?</html>\n?)", (SITE / "privacy/lustless/index.html").read_text(), re.S)
assert LUSTLESS_DOC_TAIL, "could not find the policy pages' footer"
DOC_TAIL = LUSTLESS_DOC_TAIL.group(1)

privacy = doc_page("privacy", "Privacy for <em>PhotoMuse.</em>",
    "      <p>The short version: we collect nothing, and your photos never leave your device.</p>",
    [("What we collect", ["!Nothing.",
        "PhotoMuse has no account, no sign-in, no advertising and no analytics. We do not collect your name, your email address, your location, an advertising identifier, your photos, or any record of how you use the app. There is no server involved in using the app at all, so there is nowhere for your data to go.",
        "We built it that way on purpose. A photo library is about the most personal thing on a phone. We could not identify you, or see a single picture of yours, from anything we hold &mdash; because we hold nothing."]),
     ("Your photos", [
        "PhotoMuse asks for access to your photo library so that it can find similar shots, duplicates, bad photos and large videos, let you search, enhance and compress, and delete what you choose. You can give it the whole library or only the photos you pick, and change that at any time in Settings → Privacy &amp; Security → Photos.",
        "All of that work happens on your iPhone or iPad, using Apple's own on-device frameworks and a detail model that ships inside the app. <strong>No photo, video, thumbnail or description of one is ever uploaded, to us or to anybody else.</strong>",
        "We use this access for one purpose only: to do what you asked, on your device."]),
     ("What stays on your device", [
        "To avoid re-reading your library every time it opens, the app keeps its working notes in its own space on your device: which photos belong to which pile, their sizes, the words it found for search, your swipe-review decisions and your place in each month, your settings, and how much of the free allowance you have used. None of this is uploaded, and deleting the app deletes all of it.",
        "Enhanced photos and compressed videos are saved into your own photo library, where they are yours like any other picture."]),
     ("Deleting", [
        "PhotoMuse never deletes anything on its own. Every delete is confirmed by you in Apple's own confirmation sheet. Deleted items go to Recently Deleted in the Photos app, where Apple keeps them for 30 days before removing them, and from where you can recover them."]),
     ("iCloud Photos", [
        "If you use iCloud Photos with storage optimisation, the full-size original of a photo or video may be in your iCloud rather than on your device. When you enhance or compress such an item, Apple's Photos system downloads that original from <em>your</em> iCloud to <em>your</em> device so the work can be done. That transfer is between your device and Apple under your Apple&nbsp;ID. We are not part of it and never see the file. Scanning and search never trigger it."]),
     ("Purchases", [
        "PhotoMuse Plus is sold through Apple as a weekly or yearly auto-renewable subscription, or as a one-time lifetime purchase. Payment is handled entirely by the App Store: we never see your card, your Apple&nbsp;ID or your billing details. The app only learns whether Plus is currently active, which it reads from Apple on your device. Manage or cancel a subscription in your App Store account settings."]),
     ("When the app uses the internet", [
        "The app contacts Apple's App Store services to show prices and to complete or restore a purchase. Apart from that, the iCloud download described above, and any link you deliberately tap (this page, the guide, Apple's terms), PhotoMuse does not contact the internet. Scanning, the piles, search, the swipe review, Enhance and compression all work with no connection at all."]),
     ("No third parties", [
        "The app contains no advertising, no analytics library, no crash reporter and no social media kit, and it never shows the tracking permission prompt because it does not track. We do not sell or share data, because there is none to sell or share."]),
     ("Children", ["PhotoMuse is a general-audience utility and is not directed at children. It collects no personal information from anyone, of any age."]),
     ("Your rights", ["Rules such as the GDPR and the CCPA give you the right to see, correct, export or delete the personal data a company holds about you. We hold none, so there is nothing for us to show you or delete. Everything the app records is on your device, and deleting the app removes all of it."]),
     ("Changes", ["If this policy ever changes, the new version will appear on this page with a new date at the top. If a change ever meant the app started collecting something, we would say so plainly rather than quietly rewording a paragraph."]),
     ("Contact", ['Questions about this policy, or about the app: <a href="mailto:support@novadevcodestudio.com">support@novadevcodestudio.com</a>',
                  'Terms of use are <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" target="_blank" rel="noreferrer">Apple\'s standard licence agreement</a> for App Store apps.'])],
    stamp=UPDATED) + DOC_TAIL

store_line = (f'<a href="{STORE}" target="_blank" rel="noreferrer">PhotoMuse on the App Store</a> &middot; ' if LIVE else "<!-- FLIP-ON-LAUNCH -->")
support = doc_page("support", "Help with <em>PhotoMuse.</em>",
    f'      <p>{store_line}<a href="../../photomuse/">About the app</a> &middot; <a href="../../photomuse/guide/">The complete guide</a></p>\n      <p>Straight answers. If yours is not here, write to us at the bottom.</p>',
    [("I deleted a lot of photos and my storage did not change", [
        "That is how iOS works, in every app: deleted photos move to <strong>Recently Deleted</strong> in the Photos app, where they stay for 30 days and still take up room. To free the space now, open PhotoMuse → Settings → <strong>Finish freeing space in Photos</strong>, then in Photos open Recently Deleted and choose Select → Delete All.",
        "Apple gives apps no way to open that album directly, so the button opens Photos with it searched for."]),
     ("I deleted something by mistake. Can I get it back?", [
        "Yes, for 30 days. Open the Photos app → Albums → Recently Deleted, select the photo, and tap Recover. In the swipe review you can also <strong>Undo</strong> any mark before you confirm &mdash; swiping never deletes anything by itself."]),
     ("Does anything leave my phone?", [
        "No. Scanning, the piles, search, Enhance and compression all run on your device. There is no account, no server and no analytics. The details are on the <a href=\"../../privacy/photomuse/\">privacy page</a>."]),
     ("The piles look too small, or it says it is counting only the photos I picked", [
        "PhotoMuse has been given access to some photos rather than all of them. Tap <strong>Change</strong> on the first screen, or open Settings → Privacy &amp; Security → Photos → PhotoMuse and choose Full Access."]),
     ("It says my library has changed", [
        "You have taken or deleted photos since the last scan, so the numbers on screen are from before. Tap <strong>Check again</strong>. If you would rather it did this by itself, turn on <em>Check again automatically</em> in Settings &mdash; it is off by default because looking at every photo is real work on a large library."]),
     ("Why did an enhanced photo appear under Duplicates or Similar shots?", [
        "Because it is the same picture as its original, and PhotoMuse is right to notice. Keep whichever you prefer. If you would rather not have two, use <strong>Replace original</strong> when saving from Enhance."]),
     ("Is Replace original safe?", [
        "Yes. Photos keeps the untouched original alongside the edit, as it does for its own edits. To go back, open the photo in Photos → Edit → Revert. Live Photos can only be saved as a copy, because replacing one would drop the movement."]),
     ("Enhance or Compress takes a while to start", [
        "With iCloud Photos and Optimise Storage on, the full-size original may be in your iCloud, and Apple's Photos system has to fetch it first. Wi-Fi helps. Rebuild detail is also real work on a large photo, and says so while it runs."]),
     ("Why are some videos not offered for compression?", [
        "Re-encoding an efficient video makes it bigger, so PhotoMuse lists only videos that Apple's encoder says will shrink. Slow-motion clips and videos whose original is only in iCloud are left alone too. The screen shows how many were skipped for each reason."]),
     ("Search did not find my photo", [
        "Search reads what is visibly in a picture &mdash; <em>cat</em>, <em>beach</em>, <em>car</em> &mdash; on your device, and it does not know names, places or text. The first read of a big library takes a while. When a word finds nothing, <strong>Search Photos instead</strong> passes it to Apple's Photos app."]),
     ("What is free, and what is Plus?", [
        "Free, with no time limit: scanning, every pile, search, the whole swipe review, and deleting photos you pick by hand. Also free to try: cleaning 5 similar or duplicate groups, enhancing 5 photos, and compressing 2 videos.",
        "Plus is for doing it in bulk: selecting a whole pile, month or size group at once, cleaning every group, and enhancing and compressing without a limit. Prices are shown in the app and on the App Store."]),
     ("Subscriptions, the free trial, lifetime, restoring and cancelling", [
        "Plus is sold and billed by Apple: weekly, yearly with a 7-day free trial, or a one-time lifetime purchase. If you cancel during the trial you are not charged. To restore a purchase on a new device, open Settings in PhotoMuse → <strong>Restore a purchase</strong>. To change or cancel a subscription, use Settings → your name → Subscriptions on your device, or <strong>Manage or cancel</strong> in PhotoMuse once a plan is active. Cancelling stops renewal; Plus stays on until the end of the period you paid for. Lifetime has nothing to renew or cancel."]),
     ("Contact", ['Anything else &mdash; a bug, a question, a suggestion: <a href="mailto:support@novadevcodestudio.com">support@novadevcodestudio.com</a>. It reaches a person, not a form.'])]) + DOC_TAIL

PAGES = [("photomuse/index.html", overview), ("photomuse/guide/index.html", guide),
         ("privacy/photomuse/index.html", privacy), ("support/photomuse/index.html", support)]

# Writing is something you ask for. The default is a dry run that diffs what
# this script would produce against what is live, because it has quietly
# deleted hand-made work before and a warning in a comment did not stop it.
write = "--write" in sys.argv[1:]
show = "--diff" in sys.argv[1:]
drift = 0
for rel, html in PAGES:
    out = SITE / rel
    current = out.read_text() if out.exists() else ""
    same = current == html
    if not same:
        drift += 1
    if write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print(f"{'wrote':8} {rel:36} {len(html):6} bytes{'' if same else '   (CHANGED)'}")
    else:
        mark = "same" if same else "WOULD CHANGE"
        print(f"{mark:12} {rel:36} live {len(current):6} -> {len(html):6} bytes")
        if show and not same:
            for line in difflib.unified_diff(current.splitlines(), html.splitlines(),
                                             fromfile=f"live/{rel}", tofile=f"generated/{rel}",
                                             lineterm="", n=1):
                print("   " + line)

if not write:
    print()
    if drift:
        print(f"{drift} of {len(PAGES)} pages would change. Nothing was written.")
        print("Run with --diff to see how, and --write once the difference is only what you intend.")
    else:
        print("The generator reproduces every live page exactly. --write is safe.")
    sys.exit(1 if drift else 0)
