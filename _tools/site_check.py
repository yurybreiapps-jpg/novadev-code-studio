"""Site sanity check: broken internal links/assets, missing #anchors, orphan and
unreachable pages, pages with no way home, sitemap vs files.

    python3 _tools/site_check.py            (run from the site root)
"""
import os, re, sys, urllib.parse
from html.parser import HTMLParser
from collections import defaultdict, deque

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
HOST = "www.novadevcodestudio.com"
SKIP_DIRS = {".git", "node_modules", "_tools", ".claude"}
# Pages that are meant to be unlinked: the Google ownership-check file and old addresses that only redirect.
EXPECTED_UNLINKED = {"googlebabfa33e7c6adb1c.html", "Projects/iOS/a-tennis-ai-coach/index.html"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.links=[]; self.assets=[]; self.ids=set()
    def handle_starttag(self, tag, a):
        a=dict(a)
        for k in ("id","name"):
            if a.get(k): self.ids.add(a[k])
        if tag=="a" and a.get("href"): self.links.append(a["href"])
        if tag in ("img","script","source","video","audio") and a.get("src"): self.assets.append(a["src"])
        if tag=="link" and a.get("href") and a.get("rel") not in ("canonical","alternate","preconnect","dns-prefetch"): self.assets.append(a["href"])
        if tag in ("img","source") and a.get("srcset"):
            for part in a["srcset"].split(","):
                u=part.strip().split(" ")[0]
                if u: self.assets.append(u)
        if tag=="video" and a.get("poster"): self.assets.append(a["poster"])

pages={}
for d,dirs,files in os.walk(ROOT):
    dirs[:]=[x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
    for f in files:
        if f.endswith(".html"):
            p=os.path.relpath(os.path.join(d,f),ROOT); pages[p]=None
for p in pages:
    pr=P(); pr.feed(open(os.path.join(ROOT,p),encoding="utf-8",errors="replace").read()); pages[p]=pr

def resolve(page,url):
    """Return (local_path or None if external, fragment)."""
    u=urllib.parse.urlsplit(url)
    if u.scheme in ("mailto","tel","javascript","data","sms"): return None,None
    if u.scheme in ("http","https"):
        if u.netloc not in (HOST,"novadevcodestudio.com"): return None,None
        path=u.path
        base=""
    else:
        path=u.path; base=os.path.dirname(page)
    if path=="" : target=page
    elif path.startswith("/"): target=path.lstrip("/")
    else: target=os.path.normpath(os.path.join(base,path))
    target=urllib.parse.unquote(target)
    full=os.path.join(ROOT,target)
    if os.path.isdir(full) or path.endswith("/") or target in (".",""):
        target=os.path.normpath(os.path.join(target,"index.html")) if target not in (".","") else "index.html"
    return target,u.fragment

broken=defaultdict(list); badanchor=defaultdict(list); badasset=defaultdict(list)
inbound=defaultdict(set); graph=defaultdict(set)
for p,pr in pages.items():
    for h in pr.links:
        t,frag=resolve(p,h)
        if t is None: continue
        if not os.path.exists(os.path.join(ROOT,t)):
            broken[p].append(h); continue
        if t.endswith(".html"):
            if t!=p: inbound[t].add(p)
            graph[p].add(t)
            if frag and t in pages and frag not in pages[t].ids: badanchor[p].append(h)
    for a in pr.assets:
        t,_=resolve(p,a)
        if t is None: continue
        if not os.path.exists(os.path.join(ROOT,t.split("?")[0])): badasset[p].append(a)

seen={"index.html"}; q=deque(["index.html"])
while q:
    for n in graph[q.popleft()]:
        if n not in seen: seen.add(n); q.append(n)
homeless=[p for p in pages if p!="index.html" and "index.html" not in graph[p]]
# can it get home in any number of clicks?
def reaches_home(p):
    s={p}; q=deque([p])
    while q:
        x=q.popleft()
        if x=="index.html": return True
        for n in graph[x]:
            if n not in s: s.add(n); q.append(n)
    return False
stranded=[p for p in pages if p!="index.html" and not reaches_home(p)]

sm=os.path.join(ROOT,"sitemap.xml"); smurls=re.findall(r"<loc>([^<]+)</loc>",open(sm).read()) if os.path.exists(sm) else []
smfiles=set()
for u in smurls:
    t,_=resolve("index.html",u); smfiles.add(t)
noindex={p for p,pr in pages.items() if re.search(r'name="robots"[^>]*noindex',open(os.path.join(ROOT,p)).read())}

def show(title,items):
    items=[x for x in items if x not in EXPECTED_UNLINKED]
    print(f"\n## {title}: {len(items)}")
    for x in items: print("  -",x)
print(f"Pages scanned: {len(pages)}")
show("Broken internal links",[f"{p} -> {h}" for p,hs in sorted(broken.items()) for h in hs])
show("Links to a missing #anchor",[f"{p} -> {h}" for p,hs in sorted(badanchor.items()) for h in hs])
show("Missing images/assets",[f"{p} -> {a}" for p,as_ in sorted(badasset.items()) for a in sorted(set(as_))])
show("Orphan pages (no other page links to them)",sorted(p for p in pages if p!="index.html" and not inbound[p]))
show("Not reachable by clicking from the home page",sorted(p for p in pages if p not in seen))
show("No direct link to the home page",sorted(homeless))
show("Cannot get back home at all",sorted(stranded))
show("In sitemap but file missing",sorted(t for t in smfiles if not os.path.exists(os.path.join(ROOT,t))))
show("Reachable pages missing from sitemap",sorted(p for p in seen if p not in smfiles and p not in noindex))
