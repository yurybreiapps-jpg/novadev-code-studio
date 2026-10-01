"""Builds /lustless/compare/ and /ai-images/compare/.

Same shape as /photomuse/compare/ (concede first, then dated facts), and the
same look: the stylesheet and the social row are read from that page rather
than copied here, so the three stay one design.

Why these pages exist: AI assistants answer "which app should I use" from
comparison articles, not from app pages (ChatGPT was the tennis app's largest
referrer). These are written to be quoted, so every number carries its date
and where it was read.

Where the facts came from (re-read them before changing a figure):
  PRICES   - the In-App Purchases list on each app's US App Store page,
             1 October 2026. An app can list several prices for one plan
             (price tests), so ranges are given.
  LABELS   - the App Privacy section of the same pages, same day.
  RATINGS  - Apple's lookup API, same day.
  REVIEWS  - Lustless only: each app's most recent App Store reviews, read
             11 September 2026 (share at 1-2 stars; what happy reviewers name).
Our own apps: Lustless's free/Pro split and the AI Images device requirements
are the wording already on their product pages. AI Images' price is never
printed here (it is set in App Store Connect and is meant to change).

Safe to run: the default is a dry run that says what would change and writes
nothing.  --diff shows how,  --write writes.
"""
import difflib, json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (SITE / "photomuse/compare/index.html").read_text()
STYLE = re.search(r"<style>.*?</style>", TEMPLATE, re.S).group(0)
# These two have one more menu item than the PhotoMuse page the sheet comes
# from, and with the studio wordmark showing they need 914 and 928px on one
# line; the inherited bar stops at 880. Measured in the browser 2026-10-01.
STYLE = STYLE.replace("</style>", "  .topbar { width: min(100%, 960px); }\n  </style>")
SOCIAL_ROW = re.search(r'      <div class="social-row".*?</div>', TEMPLATE, re.S).group(0)
FONTS = re.search(r'<link href="https://fonts.googleapis.com[^>]*>', TEMPLATE).group(0)
BASE = "https://www.novadevcodestudio.com/"


def faq_ld(pairs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q,
                                       "acceptedAnswer": {"@type": "Answer", "text": a}}
                                      for q, a in pairs]}, indent=2, ensure_ascii=False)


def table(head, rows, classes=False):
    th = "".join(f"<th>{h}</th>" for h in head)
    out = []
    for r in rows:
        if classes:
            want, (c1, them), (c2, us) = r
            out.append(f'                <tr><td>{want}</td><td class="{c1}">{them}</td><td class="{c2}">{us}</td></tr>')
        else:
            out.append("                <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return ('          <div class="cmp-wrap">\n            <table class="cmp-table">\n'
            f'              <thead><tr>{th}</tr></thead>\n              <tbody>\n'
            + "\n".join(out) + "\n              </tbody>\n            </table>\n          </div>")


def page(p):
    up = "../../"
    badge = (f'<a class="store-badge-link" href="{p["store"]}" target="_blank" rel="noreferrer" '
             f'aria-label="Download {p["app"]} on the App Store">'
             f'<img src="{up}assets/store/app-store-badge.png" alt="Download on the App Store"></a>')
    nav = "\n".join(f'        <a href="{h}">{t}</a>' for t, h in p["nav"])
    sections = "\n\n".join(p["sections"])
    faq = "\n\n".join(f"          <h3>{q}</h3>\n          <p>{a}</p>" for q, a in p["faq"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p["title"]}</title>
  <meta name="description" content="{p["desc"]}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f7f9ff">
  <link rel="canonical" href="{BASE}{p["path"]}">
  <meta property="og:title" content="{p["og_title"]}">
  <meta property="og:description" content="{p["og_desc"]}">
  <meta property="og:url" content="{BASE}{p["path"]}">
  <meta property="og:image" content="{BASE}{p["og_image"]}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="NovaDev Code Studio">
  <meta name="twitter:card" content="summary">
  <link rel="icon" type="image/png" href="{up}assets/favicon.png">
  <script type="application/ld+json">
{faq_ld(p["faq_ld"])}
  </script>
  {FONTS}
  {STYLE}
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
        <a class="brand-app" href="../">
          <img class="nav-app-icon" src="{up}{p["icon"]}" alt="">
          {p["short"]}
        </a>
      </span>
      <nav class="nav" aria-label="Page links">
{nav}
        <a class="store-pill" href="{p["store"]}" target="_blank" rel="noreferrer">App Store</a>
      </nav>
    </header>
  </div>
  <main>
    <section class="page-head liquid">
      <div class="container">
        <span class="eyebrow">An honest comparison</span>
        <h1 class="display">{p["h1"]}</h1>
        <p class="lead">{p["lead"]}</p>
        <div class="head-actions">
          {badge}
          <a class="button-soft" href="{p["more_href"]}">{p["more_text"]} &rarr;</a>
        </div>
      </div>
    </section>

{sections}

    <section id="faq">
      <div class="container">
        <h2 class="display">Fair <em>questions.</em></h2>
        <div class="card">
{faq}
        </div>
      </div>
    </section>

    <section class="cta liquid">
      <div class="container">
        <span class="eyebrow">Decide for yourself</span>
        <h2 class="display">{p["cta"]}</h2>
        <div class="head-actions">
          {badge}
          <a class="button-soft" href="../">About {p["short"]} &rarr;</a>
        </div>
      </div>
    </section>
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
        <nav class="footer-textlinks" aria-label="Footer links"><a href="{up}support/{p["legal"]}/">Help</a> <a href="{up}privacy/{p["legal"]}/">Privacy</a></nav>
      </div>
{SOCIAL_ROW}    </div>
  </footer>
  <script>document.getElementById("currentYear").textContent = new Date().getFullYear();</script>
</body>
</html>
'''


def section(sid, h2, body, deck=None):
    d = f'\n        <h3 class="deck">{deck}</h3>' if deck else ""
    return (f'    <section id="{sid}">\n      <div class="container">\n'
            f'        <h2 class="display">{h2}</h2>{d}\n        <div class="card">\n{body}\n'
            f'        </div>\n      </div>\n    </section>')


def paras(*ps):
    return "\n".join(f"          <p>{x}</p>" for x in ps)


FINE = ('          <p class="fineprint" style="margin-top:14px">The middle column describes the best-known '
        'apps in this category as we found them in September 2026. Apps change; check the current '
        'App Store pages before deciding.</p>')
PRICE_METHOD = ('Every price below was read from the In-App Purchases list on the app\'s US App Store page on '
                '1 October 2026. Several apps list more than one price for the same plan &mdash; they show '
                'different prices to different people &mdash; so where that happens the range is given. What '
                'you are offered inside an app can differ; check before you subscribe.')
LABEL_METHOD = ('Apple makes every developer declare this, and you can check it yourself: open any App Store '
                'page and scroll to <em>App Privacy</em>. We read these on 1 October 2026.')

# --------------------------------------------------------------------------
# Lustless
# --------------------------------------------------------------------------
LUSTLESS = dict(
    path="lustless/compare/", app="Lustless", short="Lustless", legal="lustless",
    store="https://apps.apple.com/app/id6811104656",
    icon="assets/apps/lustless/app-icon.png", og_image="assets/apps/lustless/app-icon.png",
    title="QUITTR or Unchaind alternative? An honest comparison of quit-lust apps | Lustless",
    desc=("Comparing apps for quitting adult content on iPhone and iPad: what QUITTR, Unchaind, Overcomer, "
          "Rewired and I Am Sober charge, what their privacy labels say, what their recent reviewers say, "
          "and where Lustless fits."),
    og_title="An honest comparison of quit-lust apps",
    og_desc="What the well-known apps charge, what their privacy labels say, and where Lustless fits.",
    h1="Which quit-lust app <em>should you use?</em>",
    lead=("The honest answer first: the well-known apps have far more behind them than we do &mdash; tens of "
          "thousands of ratings, communities, years of lessons. Where they differ most, from each other and "
          "from us, is in <strong>what they cost</strong>, <strong>what they do with your data</strong> and "
          "<strong>what their own recent reviewers say</strong>. Here is each of those, with dates, and where "
          "Lustless is &mdash; and is not &mdash; the right pick."),
    more_href="../", more_text="About Lustless",
    cta="Free to start, <em>nothing collected.</em>",
    nav=[("What they cost", "#cost"), ("Recent reviews", "#reviews"), ("Privacy", "#privacy"),
         ("Side by side", "#table"), ("FAQ", "#faq")],
)
LUSTLESS["sections"] = [
    section("cost", "What they <em>actually cost.</em>",
            paras(PRICE_METHOD) + "\n" + table(
                ["App", "Ratings", "Plans listed on the App Store"],
                [["<strong>I Am Sober</strong>", "188K", "$9.99 a month, $27.49 for six months, $29.99&ndash;$39.99 a year."],
                 ["<strong>Unchaind</strong>", "41K", "$14.99&ndash;$17.99 a month, $39.99&ndash;$49.99 a year. Other plans from $4.99."],
                 ["<strong>QUITTR</strong>", "34K", "$9.99&ndash;$14.99 a month, $19.99&ndash;$29.99 a year, or <strong>$49.99 once</strong>."],
                 ["<strong>Overcomer</strong>", "11K", "$19.99&ndash;$29.99 a year with a 3-day trial. Other plans from $4.99 to $34.99."],
                 ["<strong>Rewired</strong>", "3K", "$3.99 a week, $4.99&ndash;$9.99 a month, $29.99&ndash;$59.99 a year, or <strong>$49.99 once</strong>."],
                 ["<strong>Lustless</strong>", "New", "Free: the counter, the panic button, your reasons, the log and the daily check-in. Pro (the Shield, the 90-day guide, your patterns): $9.99 a month or $29.99 a year, with a 7-day free trial."]])
            + "\n" + paras(
                '<span style="display:block;margin-top:14px"><strong>The price is rarely the whole story here.</strong> '
                "When we read these apps' most recent reviews, price and billing were the most common complaint. "
                "Whatever you pick, start a trial knowing the date it ends, and know that every one of these "
                "&mdash; ours included &mdash; is cancelled in your Apple&nbsp;ID settings, not inside the app.</span>")
            + '\n          <div class="tip"><strong>Where I Am Sober wins, plainly:</strong> 188,000 ratings, a '
              "community of people on the same road, every kind of addiction covered, and the lowest share of "
              "unhappy recent reviews of any app we measured. If community is what keeps you going, it is the "
              "better choice and we would rather say so than pretend otherwise.</div>",
            deck="Read from each App Store page, the one place every plan is written down."),
    section("reviews", "What recent reviewers <em>actually say.</em>",
            paras("A star rating is an average of everything since launch. It moves slowly, so an app can show "
                  "4.7 while the people using it this month are unhappy. On 11 September 2026 we read each "
                  "app's most recent App Store reviews and counted how many gave one or two stars. Every one "
                  "of these apps showed a lifetime rating between 4.6 and 4.9 that day.")
            + "\n" + table(
                ["App", "Most recent reviews giving 1 or 2 stars"],
                [["<strong>QUITTR</strong>", "82% &mdash; 410 of the 500 most recent"],
                 ["<strong>Seed</strong>", "59%"],
                 ["<strong>Brainbuddy</strong>", "56%"],
                 ["<strong>Overcomer</strong>", "46%"],
                 ["<strong>Unchaind</strong>", "38%"],
                 ["<strong>I Am Sober</strong>", "12%"]])
            + "\n" + paras(
                '<span style="display:block;margin-top:14px">People with a complaint write more reviews than people '
                "without one, so none of these is the share of unhappy users. That is what makes I Am Sober "
                "useful as a yardstick: the same count, on a well-run app, comes out at 12%.</span>",
                "The complaints repeat: price and billing first, then a paywall in front of everything, crashes, "
                "and not being able to log in &mdash; which came up in about a quarter of QUITTR's complaints "
                "and a fifth of Brainbuddy's.",
                "<strong>Lustless has no ratings yet.</strong> It was released on 15 September 2026, so there is "
                "nothing of ours to count, and you should weigh that. What we can say is what we built in "
                "response: there is no account to fail to log in to, the counter and the panic button are free "
                "and stay free, and the only things behind the trial are the blocker, the full guide and your "
                "patterns.")),
    section("privacy", "What their labels <em>say about tracking.</em>",
            paras(LABEL_METHOD,
                  "<strong>QUITTR, Unchaind, Overcomer and Rewired all declare &ldquo;Data Used to Track "
                  "You&rdquo;.</strong> So does BlockerX. I Am Sober does not; it declares &ldquo;Data Linked to "
                  "You&rdquo;.",
                  "<strong>Lustless declares &ldquo;Data Not Collected&rdquo;.</strong> There is no account, no "
                  "analytics and no advertising. What you write &mdash; your reasons, your log, your relapses "
                  "&mdash; stays on your device, and there is no server of ours for it to go to. For an app "
                  "about this subject, we think that matters more than any feature.",
                  "This is not a claim you have to take our word for. It is on each App Store page, in the same "
                  "place, written in Apple's words rather than ours.")),
    section("table", "Side by <em>side.</em>",
            table(["What you want", "The well-known apps", "Lustless"],
                  [("Count clean days and see the streak", ("yes", "Yes &mdash; all of them"), ("yes", "Yes, free")),
                   ("A panic button for the hard moment", ("yes", "Most of them"), ("yes", "Yes, free &mdash; your own reasons come first")),
                   ("Block adult sites and apps", ("yes", "Some of them"), ("yes", "Yes &mdash; Apple's own adult filter plus your own list. Part of Pro")),
                   ("A community of other people quitting", ("yes", "Yes &mdash; several of them"), ("no", "No")),
                   ("An AI companion to talk to", ("yes", "Yes &mdash; several lead with it"), ("no", "No, on purpose")),
                   ("An accountability partner", ("yes", "Some of them"), ("no", "Not yet")),
                   ("Pay once and keep it", ("yes", "QUITTR and Rewired: $49.99"), ("no", "No &mdash; monthly or yearly")),
                   ("Thousands of ratings behind it", ("yes", "3K&ndash;188K"), ("no", "No. It is new")),
                   ("Use it without making an account", ("no", "Login trouble is a common complaint"), ("yes", "Yes &mdash; there is no account at all")),
                   ("Privacy label says no data collected", ("no", "No &mdash; none of the six we checked"), ("yes", "Yes")),
                   ("No invented &ldquo;recovery score&rdquo;", ("no", "Some show a score or a predicted quit date"), ("yes", "Yes &mdash; only numbers from your own log"))],
                  classes=True) + "\n" + FINE),
]
LUSTLESS["faq"] = [
    ("Is Lustless a QUITTR alternative?",
     "Partly, and it depends what you wanted. If you want a community, an AI companion or a pay-once price, "
     "QUITTR has all three and we have none of them. If what you wanted was a blocker, a counter and a panic "
     "button that work without an account, with nothing collected and the basics free, then yes."),
    ("Why is there no AI companion?",
     "Because the people who like these apps do not seem to value it. On 11 September 2026 we read the four- "
     "and five-star reviews of the apps that lead with one, and the companion was the least-mentioned feature "
     "&mdash; named by 3% of happy reviewers at most. Lessons, an accountability partner and the blocker itself "
     "came up far more often. So the blocker came first."),
    ("Does the blocker work outside Safari?",
     "Yes. When the Shield is on, Apple's own adult-content filter is on, along with any sites you add and any "
     "apps or categories you pick, and it holds in other browsers as well as Safari. iOS does the blocking, and "
     "the app never sees which sites or apps you chose. Like every blocker on an iPhone, it can be switched off "
     "by the person holding the phone: it is a guard rail, not a lock."),
    ("Is anything I write uploaded?",
     "No. Your reasons, your urge and relapse log and your check-ins stay on your device. There is no account "
     "and no server of ours. You can also lock the app behind Face ID."),
    ("What is free?",
     "The counter and calendar, the panic button and breathing, your reasons, the urge and relapse log, and "
     "the daily check-in &mdash; free, with no time limit. Pro adds the Shield, the full 90-day guide and your "
     "patterns, with a 7-day free trial. Turning the Shield off never needs Pro."),
    ("Is this medical advice?",
     "No. Lustless is a tool, not treatment. If this is affecting your health, your work or your "
     "relationships, a doctor or a licensed therapist can help in ways no app can."),
]
LUSTLESS["faq_ld"] = [
    ("Is Lustless a QUITTR alternative?",
     "If you want a community, an AI companion or a pay-once price, QUITTR has all three and Lustless has none. "
     "Lustless suits you if you want an adult-content blocker, a clean-day counter and a panic button that work "
     "without an account, with the basics free and a privacy label that says no data is collected."),
    ("Do quit-lust apps track you?",
     "Several do. On 1 October 2026 the App Store privacy labels of QUITTR, Unchaind, Overcomer, Rewired and "
     "BlockerX all declared Data Used to Track You. I Am Sober declared Data Linked to You. Lustless declares "
     "Data Not Collected."),
    ("Does the Lustless blocker work outside Safari?",
     "Yes. The Shield turns on Apple's own adult-content filter plus any sites, apps or categories you add, and "
     "it holds in other browsers as well as Safari. It can be switched off by the person holding the phone."),
    ("What is free in Lustless?",
     "The clean-day counter and calendar, the panic button and breathing, your reasons, the urge and relapse "
     "log and the daily check-in are free with no time limit. Pro adds the Shield, the full 90-day guide and "
     "your patterns, at $9.99 a month or $29.99 a year with a 7-day free trial."),
]

# --------------------------------------------------------------------------
# AI Image Generator Anywhere   (our own price is never printed: see the top)
# --------------------------------------------------------------------------
IMAGES = dict(
    path="ai-images/compare/", app="AI Image Generator Anywhere", short="AI Images",
    legal="ai-image-generator", store="https://apps.apple.com/app/id6805583172",
    icon="assets/apps/ai-image-generator/app-icon.png", og_image="assets/ai-image-generator-banner.png",
    title="Draw Things or LocalGen alternative? An honest comparison of AI image apps for iPhone | AI Image Generator Anywhere",
    desc=("Comparing AI image generators for iPhone and iPad: which run on the device and which on a server, "
          "what Draw Things, LocalGen, DaVinci and Leonardo charge, what their privacy labels say, and where "
          "AI Image Generator Anywhere fits."),
    og_title="An honest comparison of AI image apps for iPhone",
    og_desc="Cloud or on-device, what each one charges, what their privacy labels say, and where ours fits.",
    h1="Which AI image app <em>should you use?</em>",
    lead=("The honest answer first: if you want the best picture a machine can make today, use one of the big "
          "cloud services &mdash; their models are far larger than anything a phone can run. And if you want "
          "every model and every dial, on your own device, for free, use Draw Things. This page is about where "
          "the differences really are &mdash; <strong>where the picture is made</strong>, <strong>what it "
          "costs</strong> and <strong>what happens to what you type</strong> &mdash; and the narrower case "
          "where AI Image Generator Anywhere is the right pick."),
    more_href="../guides/", more_text="Read the guides",
    cta="Fifty pictures free, <em>nothing collected.</em>",
    nav=[("Cloud or device", "#where"), ("What they cost", "#cost"), ("Privacy", "#privacy"),
         ("Side by side", "#table"), ("FAQ", "#faq")],
)
IMAGES["sections"] = [
    section("where", "Where the picture <em>is made.</em>",
            paras("This is the difference that decides the rest. A <strong>cloud</strong> app sends your words "
                  "to a server, the server makes the picture, and it comes back. An <strong>on-device</strong> "
                  "app runs the model on your own phone.")
            + "\n" + table(
                ["Kind", "Examples", "What follows from it"],
                [["<strong>Cloud</strong>", "DaVinci, Leonardo.Ai, and the image tools inside ChatGPT, Gemini and Grok",
                  "The largest models and the best results. Needs a connection. What you type goes to their "
                  "servers. Every picture costs them money, which is why they charge by the week, the month or the token."],
                 ["<strong>On your device</strong>", "Draw Things, LocalGen, AI Image Generator Anywhere",
                  "Works with no connection. What you type stays on the phone. Limited by the phone's memory, "
                  "so the models are smaller and older phones are left out."]])
            + "\n" + paras('<span style="display:block;margin-top:14px">Neither is the honest one and the other the '
                           "trick. They are different trades, and the right one depends on what you are making.</span>")),
    section("cost", "What they <em>actually cost.</em>",
            paras(PRICE_METHOD) + "\n" + table(
                ["App", "Ratings", "Plans listed on the App Store"],
                [["<strong>DaVinci</strong> (cloud)", "76K", "$4.99&ndash;$14.99 a week, $19.99&ndash;$39.99 a year, or $29.99 once."],
                 ["<strong>Leonardo.Ai</strong> (cloud)", "11K", "Plans at $15.99, $39.99 and $79.99, or $159.99 to $749.99 a year. Extra tokens from $13."],
                 ["<strong>Draw Things</strong> (on-device)", "733", "<strong>Free to use.</strong> Optional Draw Things+ at $8.99, and Boost bundles from $0.99 to $19.99."],
                 ["<strong>LocalGen</strong> (on-device)", "164", "$4.99 a week, $9.99 a month, or $29.99 once."],
                 ["<strong>PhoneDiffusion</strong> (on-device)", "31", "$7.99&ndash;$11.99 a month, $16.99&ndash;$23.99 a year, or $24.99 once."],
                 ["<strong>AI Image Generator Anywhere</strong> (on-device)", "New", "Fifty pictures free, then <strong>one purchase</strong> unlocks it for good. No subscription. The price is on its App Store page."]])
            + "\n" + paras(
                '<span style="display:block;margin-top:14px"><strong>A weekly plan is the thing to look at twice.</strong> '
                "$4.99 a week is about $260 a year. A cloud app has a real reason to charge that way: it pays "
                "for a server every time you press the button. An on-device app does not, because the work is "
                "done by hardware you already own &mdash; which is the only reason a one-time price is possible.</span>")
            + '\n          <div class="tip"><strong>Where Draw Things wins, plainly:</strong> it is free, it has '
              "been on the App Store since 2022, it offers far more models and settings than we do, and it runs "
              "on a Mac as well. If you enjoy choosing models and tuning them, it is the better choice and we "
              "would rather say so than pretend otherwise.</div>",
            deck="Read from each App Store page, the one place every plan is written down."),
    section("privacy", "What their labels <em>say.</em>",
            paras(LABEL_METHOD,
                  "<strong>DaVinci declares &ldquo;Data Used to Track You&rdquo;.</strong> Leonardo.Ai declares "
                  "&ldquo;Data Linked to You&rdquo;, which is what you would expect of a service you sign in to.",
                  "<strong>The on-device apps do better, and that is no accident.</strong> Draw Things and "
                  "LocalGen declare &ldquo;Data Not Linked to You&rdquo; &mdash; some data is collected, but not "
                  "tied to who you are. Conjure declares &ldquo;Data Not Collected&rdquo;.",
                  "<strong>AI Image Generator Anywhere declares &ldquo;Data Not Collected&rdquo;.</strong> There "
                  "is no account, no analytics and no advertising. Your words and your pictures stay on the device.",
                  "You can test the part that matters yourself: turn on airplane mode and make a picture.")),
    section("table", "Side by <em>side.</em>",
            table(["What you want", "The others", "AI Image Generator Anywhere"],
                  [("The best picture quality there is", ("yes", "The cloud apps &mdash; much larger models"), ("no", "No. A phone cannot run models that size")),
                   ("Many models and every setting", ("yes", "Draw Things"), ("no", "No &mdash; a few chosen models and simple controls")),
                   ("Free with no limit", ("yes", "Draw Things"), ("no", "No &mdash; fifty pictures free, then one purchase")),
                   ("Runs on an older or smaller iPhone", ("yes", "The cloud apps run on anything"), ("no", "No &mdash; it needs 6 GB of memory: an iPhone 14 or later, a 12 Pro or 13 Pro, or an iPad with an M-series chip")),
                   ("Thousands of ratings behind it", ("yes", "DaVinci 76K, Leonardo.Ai 11K"), ("no", "No. It is new")),
                   ("A Mac app", ("yes", "Draw Things"), ("no", "No")),
                   ("Works with no connection", ("no", "The cloud apps: no. The on-device ones: yes"), ("yes", "Yes &mdash; try it in airplane mode")),
                   ("A picture with no second download", ("no", "Draw Things is a 0.3 GB app that fetches its models afterwards"), ("yes", "Yes &mdash; the model is inside the app, which is why it is a 3.1 GB download")),
                   ("No subscription anywhere", ("no", "Most offer weekly or monthly plans"), ("yes", "Yes &mdash; one purchase, nothing renews")),
                   ("Privacy label says no data collected", ("no", "One of the six we checked: Conjure"), ("yes", "Yes")),
                   ("Restyle or enlarge a photo you already have", ("yes", "Most of them"), ("yes", "Yes"))],
                  classes=True) + "\n" + FINE.replace("in September 2026", "on 1 October 2026")),
]
IMAGES["faq"] = [
    ("Is AI Image Generator Anywhere a Draw Things alternative?",
     "Only for some people. Draw Things is free and gives you far more models and control, and if that is what "
     "you want, use it. This app is for someone who wants to type a sentence and get a picture, with a model "
     "that is already installed and nothing to set up &mdash; and who would rather pay once than learn a toolkit."),
    ("Does it really work offline?",
     "Yes. The model runs on your iPhone or iPad's own chip. Turn on airplane mode and make a picture &mdash; "
     "that is the whole test."),
    ("Will it run on my iPhone?",
     "It depends on memory, not on how new the phone is. The standard model needs 6 GB: an iPhone 14 or later, "
     "an iPhone 12 Pro or 13 Pro, or an iPad with an M-series chip. The higher-detail model needs 12 GB. The "
     "app checks first, and tells you if your device cannot run a model."),
    ("Why is the app more than 3 GB?",
     "Because the model that makes the pictures is inside it. A cloud app is small because its model lives on "
     "a server; an on-device app has to bring it along. It is downloaded once, with the app."),
    ("Is there a subscription?",
     "No. Fifty pictures are free. After that, one purchase unlocks the app for good and nothing renews. That "
     "is possible only because making a picture costs us nothing &mdash; your device does the work."),
    ("Is anything uploaded?",
     "No. What you type and what you make stay on the device, and there is no account. The only time the app "
     "goes online is to download an optional larger model, if you ask for one."),
]
IMAGES["faq_ld"] = [
    ("Is AI Image Generator Anywhere a Draw Things alternative?",
     "Draw Things is free and offers far more models and settings, so it is the better choice for people who "
     "like tuning. AI Image Generator Anywhere suits someone who wants to type a sentence and get a picture "
     "with a model already installed, pays once with no subscription, and wants a privacy label that says no "
     "data is collected."),
    ("Which AI image generators for iPhone work offline?",
     "On-device apps do: Draw Things, LocalGen and AI Image Generator Anywhere run the model on the phone and "
     "need no connection. Cloud apps such as DaVinci and Leonardo.Ai send your prompt to a server and need one."),
    ("Will AI Image Generator Anywhere run on my iPhone?",
     "It needs 6 GB of memory for the standard model: an iPhone 14 or later, an iPhone 12 Pro or 13 Pro, or an "
     "iPad with an M-series chip. The higher-detail model needs 12 GB."),
    ("Does AI Image Generator Anywhere have a subscription?",
     "No. Fifty pictures are free, then one purchase unlocks the app for good. Nothing renews."),
]

PAGES = [("lustless/compare/index.html", page(LUSTLESS)), ("ai-images/compare/index.html", page(IMAGES))]

write = "--write" in sys.argv[1:]
show = "--diff" in sys.argv[1:]
drift = 0
for rel, html in PAGES:
    out = SITE / rel
    current = out.read_text() if out.exists() else ""
    same = current == html
    drift += not same
    if write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print(f"{'wrote':8} {rel:36} {len(html):6} bytes{'' if same else '   (CHANGED)'}")
    else:
        print(f"{'same' if same else 'WOULD CHANGE':12} {rel:36} live {len(current):6} -> {len(html):6} bytes")
        if show and not same:
            for line in difflib.unified_diff(current.splitlines(), html.splitlines(), fromfile=f"live/{rel}",
                                             tofile=f"generated/{rel}", lineterm="", n=1):
                print("   " + line)
if not write:
    print(f"\n{drift} of {len(PAGES)} pages would change. Nothing was written." if drift
          else "\nThe generator reproduces both pages exactly. --write is safe.")
    sys.exit(1 if drift else 0)
