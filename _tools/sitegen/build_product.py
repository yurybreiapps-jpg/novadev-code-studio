import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import page, section, BASE

ROOT = sys.argv[1]
NAV = [("What it does","#what"),("On your device","#device"),
       ("Will it run?","#requires"),("Price","#price"),("Guides","guides/")]

head = '''        <p class="eyebrow">iPhone &amp; iPad</p>
        <h1 class="display">AI Image Generator Anywhere</h1>
        <p class="lead">An image generator that runs on your phone instead of somebody's server.
        No account, no credits, no queue &mdash; and it works with no signal at all.</p>
        <p class="deck">One purchase. No subscription. Fifty images free first.</p>
        <div class="tip" style="max-width:620px;margin:20px auto 0;text-align:left;">
          <strong>Coming to the App Store soon.</strong> These pages are up ahead of the
          listing on purpose &mdash; so you can check whether your device qualifies, and
          what it actually does, before deciding to download three gigabytes.
        </div>'''

s_what = section("what", '''        <h2 class="display">What it does</h2>
        <div class="card">
          <h3>Turn words into pictures</h3>
          <p>Describe what you want and it draws it, in any of seventeen styles &mdash;
          photographic, cinematic, anime, painting, line art, low poly and more.</p>
          <div class="shot-pair">
            <figure>
              <img src="../assets/apps/ai-images/create.webp" alt="The Create tab: a generated photograph of a couple on a park bench, with the prompt that made it below" width="760" height="964" loading="lazy">
              <figcaption><strong>Create</strong> &middot; Type what you want and tap Generate. The row under the picture saves it, tries again, or sends it to Enhance.</figcaption>
            </figure>
            <figure>
              <img src="../assets/apps/ai-images/styles.webp" alt="The model picker showing Photoreal and Photoreal HD, above a grid of style chips" width="760" height="964" loading="lazy">
              <figcaption><strong>Models and styles</strong> &middot; Photoreal for speed, Photoreal HD for detail &mdash; then a style, and one, three or five images in a run.</figcaption>
            </figure>
          </div>
        </div>
        <div class="card">
          <h3>Work from a photo you already have</h3>
          <p>Restyle a picture from your library or camera, and keep the original untouched.</p>
        </div>
        <div class="card">
          <h3>Make a picture larger and sharper</h3>
          <p>Enlarge up to 4096 pixels on the longest side. It rebuilds texture rather than
          stretching pixels, and there are colour and exposure dials with an Auto that
          moves them for you.</p>
          <div class="shot-pair">
            <figure>
              <img src="../assets/apps/ai-images/enhance.webp" alt="The Enhance tab showing an image being taken from 1,536 pixels square to 4,096" width="760" height="964" loading="lazy">
              <figcaption><strong>Enhance</strong> &middot; 1,536 pixels square taken to 4,096. Size is a choice, not a maximum &mdash; 1&times; cleans up without enlarging.</figcaption>
            </figure>
            <figure>
              <img src="../assets/apps/ai-images/adjust.webp" alt="The Adjust panel with exposure, brightness, contrast, highlights, shadows, black point and gamma sliders" width="760" height="964" loading="lazy">
              <figcaption><strong>Adjust</strong> &middot; Light, colour, detail and vignette, with an Auto that sets a starting point. Undo, redo, reset all.</figcaption>
            </figure>
          </div>
        </div>
        <div class="card">
          <h3>Ideas, when the box is blank</h3>
          <p>An empty prompt box is the hardest part of any image generator. The app
          carries a bank of written prompts grouped by subject &mdash; people, wallpapers
          and more &mdash; and tapping one fills the box for you.</p>
          <figure class="shot-wide">
            <img src="../assets/apps/ai-images/ideas.webp" alt="The Ideas sheet open over the Create tab, listing suggested prompts under a People heading, with the style grid visible beneath it" width="1100" height="1109" loading="lazy">
            <figcaption><strong>Ideas</strong> &middot; Suggested prompts, grouped by subject. Tapping one fills the box, and you can change any of it before you generate.</figcaption>
          </figure>
        </div>''')

s_device = section("device", '''        <h2 class="display">It runs on your device</h2>
        <p class="lead">Most image apps are a text box wired to somebody else's computer.
        This one puts the model on your phone and runs it on the Neural Engine.</p>
        <div class="card">
          <h3>Nothing is uploaded</h3>
          <p>Your prompts and your pictures stay on the device. There is no account
          because there is no server to sign in to.</p>
          <div class="shot-pair">
            <figure>
              <img src="../assets/apps/ai-images/gallery.webp" alt="The Gallery tab showing a grid of many generated images" width="760" height="843" loading="lazy">
              <figcaption><strong>Gallery</strong> &middot; Everything you have made, held on the device. None of it was uploaded to make it.</figcaption>
            </figure>
            <figure>
              <img src="../assets/apps/ai-images/viewer.webp" alt="A generated image open full screen with Save and Share buttons beneath it" width="760" height="895" loading="lazy">
              <figcaption><strong>Save and share</strong> &middot; Straight into Photos, or out to anywhere you like.</figcaption>
            </figure>
          </div>
        </div>
        <div class="card">
          <h3>It works offline</h3>
          <p>After the one-time model download, generation needs no connection at all.
          You can check that yourself: turn on airplane mode and make a picture.</p>
        </div>
        <div class="card">
          <h3>No counter, no queue</h3>
          <p>Generating costs nothing to run, because it runs on hardware you already own.
          That is the only reason a one-time price is possible.</p>
        </div>''')

s_req = section("requires", '''        <h2 class="display">Will it run on your device?</h2>
        <p class="lead">This is decided by memory rather than by how new the phone is,
        and the app checks before it downloads anything.</p>
        <div class="card">
          <h3>Standard model &mdash; 6 GB of memory</h3>
          <p>An iPhone 14 or later, an iPhone 12 Pro or 13 Pro, or an iPad with an
          M-series chip.</p>
        </div>
        <div class="card">
          <h3>Higher-detail model &mdash; 12 GB of memory</h3>
          <p>Draws at 1024 across, with cleaner detail and far less grain.</p>
          <figure class="shot-wide">
            <img src="../assets/apps/ai-images/model-hd.webp" alt="The Create tab with a generated photograph of a bowl of lemons, and the model picker below showing Photoreal HD selected" width="1100" height="1393" loading="lazy">
            <figcaption><strong>Photoreal HD</strong> &middot; Draws at 1024, with cleaner detail and far less grain. The app says it needs a newer device at the moment you pick it &mdash; not after a three-gigabyte download.</figcaption>
          </figure>
        </div>
        <div class="card">
          <h3>Storage and first launch</h3>
          <p>The model is about 3 GB, downloaded once over Wi-Fi. The first launch spends
          roughly two minutes letting iOS compile it for the Neural Engine. That happens
          once per install.</p>
        </div>
        <p><a class="button-soft" href="guides/will-my-iphone-run-on-device-ai-images/">Read the full compatibility guide</a></p>''')

s_price = section("price", '''        <h2 class="display">One purchase</h2>
        <p class="lead">Fifty images free, then one purchase unlocks the app for good.
        There is no subscription and
        nothing renews.</p>
        <div class="tip">
          <p>Because generation happens on your own device, each image costs us nothing to
          produce. Apps that charge monthly are usually paying a server every time you press
          the button &mdash; which is a perfectly honest reason to charge monthly, and the
          reason we do not have to.</p>
        </div>''')

n = page(path="ai-images/index.html",
     title="AI Image Generator Anywhere — on-device AI images for iPhone and iPad",
     desc="An AI image generator that runs entirely on your iPhone or iPad. No account, no credits, no subscription, and it works with no signal. One purchase, unlimited images.",
     canonical=f"{BASE}/ai-images/", depth=1, head=head, nav=NAV,
     extra_css="""
    .shot-wide { margin: 18px 0 6px; }
    .shot-wide img { display: block; width: 100%; height: auto; border-radius: 16px; border: 1px solid var(--line); }
    .shot-wide figcaption { padding: 8px 4px 0; color: var(--muted); font-size: 0.88rem; }
    .shot-wide figcaption strong { color: var(--heading); }
""",
     sections=[s_what, s_device, s_req, s_price],
     cta={"h":"Guides","p":"How it works, which devices can run it, and how to get better pictures out of it.","href":"guides/","label":"Read the guides"},
     schema='''  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "AI Image Generator Anywhere",
    "operatingSystem": "iOS, iPadOS",
    "applicationCategory": "GraphicsApplication",
    "description": "An AI image generator that runs entirely on the device. No account, no credits, no subscription, and it works offline.",
    "url": "https://www.novadevcodestudio.com/ai-images/",
    "author": { "@type": "Organization", "name": "NovaDev Code Studio" }
  }''')
print(f"  ai-images/index.html  {n:,} bytes")
