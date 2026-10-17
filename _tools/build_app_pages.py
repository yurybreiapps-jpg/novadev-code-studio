"""Builds the single-page app sites that have no generator of their own:
/tennis-score-tracker/, /zen-tile-flow/ and /eternal-light/ (2026-10-17).

The page shell — CSS, top bar, footer — is lifted from /lustless/ at build
time, so these pages look like the rest of the site and pick up any change
made there. Content is written below; every claim comes from the apps' live
store listings, their release history, or the app's own privacy policy. No
price is stated: prices live in the stores.

    python3 _tools/build_app_pages.py          # dry run: diff against what is live
    python3 _tools/build_app_pages.py --write  # write the pages
"""
import difflib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHELL = (ROOT / "lustless" / "index.html").read_text()

CSS = re.search(r"<style>(.*?)</style>", SHELL, re.S).group(1)
EXTRA_CSS = """
    .shot-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 18px 0 6px; }
    .shot-row.four { grid-template-columns: repeat(4, 1fr); }
    .shot-row figure { margin: 0; }
    .shot-row img { display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid var(--line); }
    .shot-row figcaption { padding: 8px 4px 0; color: var(--muted); font-size: 0.86rem; line-height: 1.45; }
    .shot-row figcaption strong { color: var(--heading); }
    @media (max-width: 640px) { .shot-row, .shot-row.four { grid-template-columns: 1fr 1fr; } }
    .badge-row { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin: 22px 0 0; }
    .badge-row .label { width: 100%; margin: 0; color: var(--muted); font-size: 0.9rem; font-weight: 600; }
    .badge-row img { width: 176px; height: auto; border-radius: 10px; }
"""
BRAND = re.search(r'(<a class="brand" href="\.\./".*?</a>)', SHELL, re.S).group(1)
FOOTER = re.search(r"(<footer class=\"footer\">.*?</footer>)", SHELL, re.S).group(1)
# The AlternativeTo badge belongs to Lustless alone.
FOOTER = re.sub(r'\s*<div class="container footer-badges">.*?</div>\s*(?=</footer>)', "\n  ", FOOTER, flags=re.S)

APPLE_BADGE = '<img src="../assets/store/app-store-badge.png" alt="Download on the App Store">'
PLAY_BADGE = '<img src="../assets/store/google-play-badge.png" alt="Get it on Google Play">'


def store(url, badge, label):
    return f'<a class="store-badge-link" href="{url}" target="_blank" rel="noreferrer" aria-label="{label}">{badge}</a>'


def shots(items, cls="shot-row"):
    figs = []
    for src, alt, cap, w, h in items:
        figs.append(f'''            <figure>
              <img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy">
              <figcaption>{cap}</figcaption>
            </figure>''')
    return f'          <div class="{cls}">\n' + "\n".join(figs) + "\n          </div>"


def page(slug, title, description, og_desc, og_image, app_name, app_icon, os_list, category,
         install_url, nav, nav_store, body):
    links = "\n".join(f'        <a href="{href}">{text}</a>' for href, text in nav)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f7f9ff">
  <link rel="canonical" href="https://www.novadevcodestudio.com/{slug}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="https://www.novadevcodestudio.com/{slug}/">
  <meta property="og:image" content="https://www.novadevcodestudio.com/{og_image}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="NovaDev Code Studio">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="../assets/favicon.png">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{app_name}",
    "operatingSystem": "{os_list}",
    "applicationCategory": "{category}",
    "description": "{og_desc}",
    "url": "https://www.novadevcodestudio.com/{slug}/",
    "installUrl": "{install_url}",
    "author": {{ "@type": "Organization", "name": "NovaDev Code Studio" }}
  }}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>{CSS}{EXTRA_CSS}  </style>
</head>
<body>
  <div class="nav-wrap">
    <header class="topbar">
      <span class="brand-group">
        {BRAND}
        <span class="brand-sep" aria-hidden="true">·</span>
        <span class="brand-app">
          <img class="nav-app-icon" src="{app_icon}" alt="">
          {app_name.split(":")[0]}
        </span>
      </span>
      <nav class="nav" aria-label="Page links">
{links}
        {nav_store}
      </nav>
    </header>
  </div>
  <main>
{body}
  </main>
  {FOOTER}
  <script>document.getElementById("currentYear").textContent = new Date().getFullYear();</script>
</body>
</html>
'''


# ---------------------------------------------------------------- scorer
TST = "../assets/apps/tennis-score-tracker/"
TST_IOS = "https://apps.apple.com/app/id6763812774"
TST_PLAY = "https://play.google.com/store/apps/details?id=space.manus.matchscore.t20260326123000"
TSW_IOS = "https://apps.apple.com/app/id6772611262"
TSW_PLAY = "https://play.google.com/store/apps/details?id=com.novadevcodestudio.matchscoreprowatch"


def all_badges():
    return f'''        <div class="badge-row">
          <p class="label">Phone and tablet</p>
          {store(TST_IOS, APPLE_BADGE, "Tennis Score Tracker Match on the App Store")}
          {store(TST_PLAY, PLAY_BADGE, "Tennis Score Tracker Match on Google Play")}
        </div>
        <div class="badge-row">
          <p class="label">Watch</p>
          {store(TSW_IOS, APPLE_BADGE, "Tennis Score Tracker Watch on the App Store")}
          {store(TSW_PLAY, PLAY_BADGE, "Tennis Score Tracker Watch on Google Play")}
        </div>'''


scorer_body = f'''    <section class="page-head liquid">
      <div class="container">
        <p class="eyebrow">iPhone, iPad &amp; Android &middot; Apple Watch &amp; Wear OS</p>
        <h1 class="display">Tennis Score Tracker</h1>
        <p class="lead"><strong>Never argue about the score again.</strong> 30-15 or 15-30? Who's serving?
        Did we switch sides? A fast scorekeeper for tennis, pickleball and ping-pong, on your phone,
        tablet or watch.</p>
{all_badges()}
      </div>
    </section>
    <section id="what">
      <div class="container">
        <h2 class="display">What it does</h2>
        <div class="card">
          <p>Tap to score; undo and redo any point. The current server is always shown, with a match
          timer. Tennis singles and doubles, standard sets, no-ad, pro sets and Fast4-style presets.
          Pickleball and ping-pong with win-by-two and serving indicators. Large display with a
          high-visibility mode for outdoor courts. Optional voice announcements and haptics.</p>
{shots([
    (TST + "phone-2.webp", "Tennis scoring on iPhone: 15-40, team names, sets and games, server shown", "<strong>Tennis</strong> &middot; Points, games and sets, and who serves next.", 760, 1645),
    (TST + "phone-3.webp", "Pickleball scoring on iPhone with the serving team marked", "<strong>Pickleball</strong> &middot; Win-by-two and the server, on a court view.", 760, 1645),
    (TST + "phone-4.webp", "Ping-pong scoring on iPhone, 7-5", "<strong>Ping-pong</strong> &middot; The same tap-to-score, on a table view.", 760, 1645),
])}
        </div>
      </div>
    </section>
    <section id="phone">
      <div class="container">
        <h2 class="display">On your phone</h2>
        <p class="lead">iPhone, iPad and Android. Saved players with photos, match history and statistics,
        Spectator Mode, rematch in one tap.</p>
        <div class="card">
{shots([
    (TST + "phone-5.webp", "Players list with saved player profiles", "<strong>Players</strong> &middot; Saved profiles, so a rematch takes seconds.", 760, 1645),
    (TST + "phone-7.webp", "Match history across tennis, pickleball and ping-pong", "<strong>History</strong> &middot; Every match, filterable by sport.", 760, 1645),
    (TST + "phone-8.webp", "Statistics overview with a breakdown by sport", "<strong>Stats</strong> &middot; How you play, over time.", 760, 1645),
])}
        </div>
        <div class="card">
          <h3>On Android: score without touching the phone</h3>
          <p>Volume up scores for the top player, volume down for the bottom one. Any Bluetooth media
          remote works too: &#9664;&#9664; undoes, &#9654;&#9654; redoes, and play/pause still controls your music.</p>
          <div class="tip"><p>iPhone doesn't allow apps to use the volume buttons this way.</p></div>
        </div>
      </div>
    </section>
    <section id="watch">
      <div class="container">
        <h2 class="display">On your wrist</h2>
        <p class="lead">Apple Watch and Wear OS. The score on the watch itself, no phone needed. Tap or
        slide to score, with color themes and the time of day.</p>
        <div class="card">
{shots([
    (TST + "watch-1.webp", "Apple Watch showing the score and the serving player", "<strong>Always know who's serving</strong>", 410, 887),
    (TST + "watch-2.webp", "Apple Watch with large score numbers", "<strong>Read it at a glance</strong>", 410, 887),
    (TST + "watch-5.webp", "Apple Watch with a light color theme", "<strong>Any light</strong> &middot; Light and dark themes.", 410, 887),
    (TST + "watch-10.webp", "Apple Watch settings for voice announcements and haptics", "<strong>Hear every point</strong> &middot; Spoken scores and haptics.", 410, 887),
], "shot-row four")}
        </div>
      </div>
    </section>
    <section id="price">
      <div class="container">
        <h2 class="display">Free and Pro</h2>
        <p class="lead">Standard singles scoring is free on every sport. A one-time Pro unlock adds doubles,
        every preset, custom settings, unlimited player profiles, advanced statistics, history filters,
        Spectator Mode and result sharing. No subscription.</p>
      </div>
    </section>
    <section id="private">
      <div class="container">
        <h2 class="display">Private</h2>
        <div class="card">
          <h3>No account, no cloud</h3>
          <p>Matches, players and settings stay on your device.</p>
        </div>
      </div>
    </section>
    <section class="cta liquid">
      <div class="container">
        <h2 class="display">Get Tennis Score Tracker</h2>
        <p class="lead">Free to download. Questions: <a href="mailto:support@novadevcodestudio.com">support@novadevcodestudio.com</a></p>
{all_badges()}
      </div>
    </section>'''

# ---------------------------------------------------------------- ZEN
ZEN = "../assets/apps/zen-tile-flow/"
ZEN_IOS = "https://apps.apple.com/app/id6773094129"
ZEN_PLAY = "https://play.google.com/store/apps/details?id=com.novadevcodestudio.zentileflowwatch"


def zen_badges():
    return f'''        <div class="badge-row">
          {store(ZEN_IOS, APPLE_BADGE, "ZEN Tile Flow on the App Store")}
          {store(ZEN_PLAY, PLAY_BADGE, "ZEN Tile Flow on Google Play")}
        </div>'''


zen_body = f'''    <section class="page-head liquid">
      <div class="container">
        <p class="eyebrow">Apple Watch &amp; Wear OS</p>
        <h1 class="display">ZEN Tile Flow: Pipe Puzzle</h1>
        <p class="lead">A calm pipe-connection puzzle for your watch. Turn and mirror glowing tiles until the
        two ends connect &mdash; quick to start, deep when you want it.</p>
{zen_badges()}
      </div>
    </section>
    <section id="what">
      <div class="container">
        <h2 class="display">How it plays</h2>
        <div class="card">
          <h3>Connect the flow</h3>
          <p>Tap a tile to turn it, long-press to mirror it. Link one end to the other. Early boards are
          quick and relaxing; later ones grow larger, with longer paths to find.</p>
{shots([
    (ZEN + "watch-1.webp", "Apple Watch showing a tile-flow puzzle in progress", "<strong>Connect the flow</strong>", 410, 887),
    (ZEN + "watch-2.webp", "Apple Watch showing a solved puzzle with its move count and time", "<strong>Every win feels good</strong>", 410, 887),
    (ZEN + "watch-3.webp", "Apple Watch scrolling a large deep-flow board", "<strong>Boards that go deep</strong>", 410, 887),
], "shot-row")}
        </div>
        <div class="card">
          <h3>Perfect Flow challenges</h3>
          <p>Special levels where every tile on the board has to be used &mdash; for when a quick solve
          isn't enough.</p>
        </div>
        <div class="card">
          <h3>Never run out</h3>
          <p>New boards are generated as you play, and the difficulty grows with you. Progress is saved,
          and finished flows can be replayed.</p>
{shots([
    (ZEN + "watch-6.webp", "Apple Watch showing the difficulty tiers", "<strong>Grows with you</strong>", 410, 887),
    (ZEN + "watch-8.webp", "Apple Watch settings for music, motion and contrast", "<strong>Tuned to you</strong> &middot; Music, motion, contrast.", 410, 887),
    (ZEN + "watch-10.webp", "Apple Watch offering a fresh random board", "<strong>Endless boards</strong>", 410, 887),
], "shot-row")}
        </div>
      </div>
    </section>
    <section id="watch">
      <div class="container">
        <h2 class="display">Made for the wrist</h2>
        <div class="card">
          <p>Neon visuals, ambient music, sound and haptics, built for short sessions. Plays offline.
          Music, motion and contrast can each be turned down.</p>
        </div>
      </div>
    </section>
    <section id="price">
      <div class="container">
        <h2 class="display">Free to play</h2>
        <p class="lead">No account and no ads. An optional one-time unlock adds endless Zen levels,
        harder puzzles, extra palettes and music.</p>
      </div>
    </section>
    <section class="cta liquid">
      <div class="container">
        <h2 class="display">Get ZEN Tile Flow</h2>
        <p class="lead">Free to download. Questions: <a href="mailto:support@novadevcodestudio.com">support@novadevcodestudio.com</a></p>
{zen_badges()}
      </div>
    </section>'''

# ---------------------------------------------------------------- Eternal Light
EL = "../assets/apps/eternal-light/"
EL_PLAY = "https://play.google.com/store/apps/details?id=com.eternallight.christianprayer"
EL_PRIVACY = "https://yurybreiapps-jpg.github.io/public/Apps/EternalLight/Privacy/"
EL_GUIDE = "https://yurybreiapps-jpg.github.io/public/Apps/EternalLight/HoToUse/"


def el_badges():
    return f'''        <div class="badge-row">
          {store(EL_PLAY, PLAY_BADGE, "Eternal Light on Google Play")}
        </div>'''


el_body = f'''    <section class="page-head liquid">
      <div class="container">
        <p class="eyebrow">Android</p>
        <h1 class="display">Eternal Light: Christian Prayer</h1>
        <p class="lead">A peaceful place to pray, reflect, and begin again. Guided prayers for the moment
        you're in, read or listened to, with a journal and a gentle record of your prayer time.</p>
{el_badges()}
      </div>
    </section>
    <section id="what">
      <div class="container">
        <h2 class="display">What it does</h2>
        <div class="card">
          <h3>A prayer for the moment you're in</h3>
          <p>Choose what you need prayer for &mdash; peace and calm, guidance, gratitude, strength and
          endurance, forgiveness, or a prayer for someone else &mdash; or let the app choose for you.</p>
{shots([
    (EL + "shot-1.webp", "Eternal Light welcome screen with a Begin prayer button", "<strong>Begin</strong> &middot; One button to start.", 760, 1630),
    (EL + "shot-3.webp", "A list of prayer needs: peace and calm, guidance, gratitude, strength, prayer for someone else, forgiveness", "<strong>Choose</strong> &middot; What would you like help praying about?", 760, 1630),
    (EL + "shot-4.webp", "A prayer with its verse, and Listen and Stop buttons", "<strong>Pray</strong> &middot; Each prayer with its verse, to read or hear.", 760, 1630),
])}
        </div>
        <div class="card">
          <h3>Read, listen, or sit in quiet</h3>
          <p>Each prayer opens with a verse and can be read aloud. A focus mode gives you a few
          undistracted minutes of quiet prayer.</p>
        </div>
        <div class="card">
          <h3>A journal and a gentle record</h3>
          <p>Save a short reflection after you pray. Streaks, minutes prayed and goals are shown as
          encouragement, not pressure. Reminders help keep a daily rhythm.</p>
{shots([
    (EL + "shot-5.webp", "Saving a short reflection to the prayer journal", "<strong>Journal</strong> &middot; A reflection, saved after you pray.", 760, 1630),
    (EL + "shot-6.webp", "Progress screen with a streak, minutes of prayer and prayer goals", "<strong>Progress</strong> &middot; Streak, minutes, goals.", 760, 1630),
    (EL + "shot-7.webp", "Home screen with today's verse, Journal and Focus mode", "<strong>Home</strong> &middot; Today's verse, journal and focus mode.", 760, 1630),
])}
        </div>
      </div>
    </section>
    <section id="private">
      <div class="container">
        <h2 class="display">Your prayer life stays yours</h2>
        <div class="card">
          <p>Your journal, progress and settings are kept on your device. The <a href="{EL_PRIVACY}" target="_blank" rel="noreferrer">privacy policy</a>
          explains what is sent when a prayer is written for you.</p>
        </div>
      </div>
    </section>
    <section class="cta liquid">
      <div class="container">
        <h2 class="display">Get Eternal Light</h2>
        <p class="lead">Free to download on Google Play, with optional in-app purchases. Questions: <a href="mailto:support@novadevcodestudio.com">support@novadevcodestudio.com</a></p>
{el_badges()}
        <p style="margin-top:18px"><a class="button-soft" href="{EL_GUIDE}" target="_blank" rel="noreferrer">How to use Eternal Light</a> &nbsp; <a class="button-soft" href="{EL_PRIVACY}" target="_blank" rel="noreferrer">Privacy policy</a></p>
      </div>
    </section>'''

PAGES = {
    "tennis-score-tracker/index.html": page(
        "tennis-score-tracker",
        "Tennis Score Tracker — scorekeeper for tennis, pickleball and ping-pong, on phone and watch",
        "A fast scorekeeper for tennis, pickleball and ping-pong on iPhone, iPad, Android, Apple Watch and Wear OS: tap to score, undo any point, see who is serving. No account.",
        "A fast scorekeeper for tennis, pickleball and ping-pong on your phone, tablet or watch. No account, no cloud.",
        "assets/apps/tennis-score-tracker/phone-1.webp",
        "Tennis Score Tracker", TST + "app-icon.webp", "iOS, iPadOS, watchOS, Android, Wear OS", "SportsApplication",
        TST_IOS,
        [("#what", "What it does"), ("#phone", "Phone"), ("#watch", "Watch"), ("#price", "Free and Pro")],
        f'<a class="store-pill" href="{TST_IOS}" target="_blank" rel="noreferrer">App Store</a>',
        scorer_body),
    "zen-tile-flow/index.html": page(
        "zen-tile-flow",
        "ZEN Tile Flow: Pipe Puzzle — a calm tile-connecting puzzle for Apple Watch and Wear OS",
        "A calm pipe-connection puzzle for Apple Watch and Wear OS: turn and mirror glowing tiles to connect the flow. Endless boards, offline, no account, no ads.",
        "A calm pipe-connection puzzle for your watch. Endless boards, offline, no account and no ads.",
        "assets/apps/zen-tile-flow/watch-1.webp",
        "ZEN Tile Flow: Pipe Puzzle", ZEN + "app-icon.webp", "watchOS, Wear OS", "GameApplication",
        ZEN_IOS,
        [("#what", "How it plays"), ("#watch", "On the wrist"), ("#price", "Free to play")],
        f'<a class="store-pill" href="{ZEN_IOS}" target="_blank" rel="noreferrer">App Store</a>',
        zen_body),
    "eternal-light/index.html": page(
        "eternal-light",
        "Eternal Light: Christian Prayer — guided prayers, a journal and quiet focus, for Android",
        "Eternal Light is a peaceful Christian prayer app for Android: guided prayers for the moment you are in, read or listened to, a prayer journal, focus mode, streaks and reminders.",
        "Guided Christian prayers for the moment you are in, with a journal, quiet focus and a gentle record of your prayer time.",
        "assets/apps/eternal-light/shot-1.webp",
        "Eternal Light: Christian Prayer", EL + "app-icon.webp", "Android", "LifestyleApplication",
        EL_PLAY,
        [("#what", "What it does"), ("#private", "Privacy")],
        f'<a class="store-pill" href="{EL_PLAY}" target="_blank" rel="noreferrer">Google Play</a>',
        el_body),
}

write = "--write" in sys.argv[1:]
for rel, html in PAGES.items():
    path = ROOT / rel
    live = path.read_text() if path.exists() else ""
    if live == html:
        print(f"same         {rel}"); continue
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)
        print(f"wrote        {rel}  {len(html)} bytes")
    else:
        print(f"WOULD {'CHANGE' if live else 'CREATE'} {rel}  {len(html)} bytes")
if not write:
    print("Nothing was written. Run with --write to write the pages.")
