#!/usr/bin/env python3
"""Builds the Hrid Digital Group website.

Each page lives in src/pages/<name>.html. The first lines are settings:
    <!-- title: Page title -->
    <!-- description: One sentence for Google and link previews -->
    <!-- nav: services -->        (which menu item to highlight, optional)
Everything after them is the page body. This script wraps every page in the
shared header and footer and writes the finished site into site/.

Run:  python3 build.py            -> site/   (the real website)
      python3 build.py --preview  -> preview/ (copy for the Claude preview link)
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ROOT / "src" / "pages"
DOMAIN = "https://hriddigitalgroup.com"

# Settings used across the site. Change contact details here once.
SITE = {
    "name": "Hrid Digital Group",
    "tagline": "Grow · Scale · Succeed",
    "email": "info@hriddigitalgroup.com",
    "phone": "+91 94041 26138",
    "phone_raw": "+919404126138",
    "whatsapp": "https://wa.me/919404126138",
    "year": date.today().year,
}

# Set to False before launch to hide the "draft" bar on every page.
SHOW_DRAFT_BAR = True

NAV = [
    ("services", "services.html", "Services"),
    ("industries", "industries.html", "Industries"),
    ("case-studies", "case-studies.html", "Case Studies"),
    ("pricing", "pricing.html", "Pricing"),
    ("about", "about.html", "About"),
    ("blog", "blog.html", "Blog"),
    ("contact", "contact.html", "Contact"),
]

FONTS = ("https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800"
         "&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap")


def header(active):
    items = "\n".join(
        f'        <li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for key, href, label in NAV)
    draft = ('<div class="draft">Draft website. Sections marked "Sample" are examples '
             'to replace with your real details before launch.</div>\n') if SHOW_DRAFT_BAR else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
{draft}<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Hrid Digital Group home">
      <img src="assets/logo-mark.png" alt="" width="87" height="40">
      <span>Hrid <b>Digital Group</b></span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
{items}
      </ul>
      <a class="btn accent sm" href="free-audit.html">Free Marketing Audit</a>
    </nav>
  </div>
</header>"""


def footer():
    s = SITE
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <img src="assets/logo-600.png" alt="Hrid Digital Group" width="220" height="140" loading="lazy">
        <p>Performance marketing for businesses of every size: paid ads, social media, local search and tracking, run by one accountable team.</p>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="case-studies.html">Case Studies</a></li>
          <li><a href="testimonials.html">Client Reviews</a></li>
          <li><a href="blog.html">Blog &amp; Resources</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="services.html#paid-media">Paid Media</a></li>
          <li><a href="services.html#social">Social Media &amp; YouTube</a></li>
          <li><a href="services.html#local">Google Business Profile</a></li>
          <li><a href="services.html#tracking">Analytics &amp; Tracking</a></li>
          <li><a href="industries.html">Industries We Serve</a></li>
          <li><a href="pricing.html">Pricing &amp; Packages</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul>
          <li><a href="mailto:{s['email']}">{s['email']}</a></li>
          <li><a href="tel:{s['phone_raw']}">{s['phone']}</a></li>
          <li><a href="{s['whatsapp']}" target="_blank" rel="noopener">WhatsApp us</a></li>
          <li><a href="book-consultation.html">Book a Consultation</a></li>
          <li><a href="free-audit.html">Free Marketing Audit</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© {s['year']} Hrid Digital Group. All rights reserved.</span>
      <span>{s['tagline']}</span>
    </div>
  </div>
</footer>"""


def cta_band():
    return """<div class="wrap">
  <div class="cta-band">
    <div>
      <h2>Find out where your ad budget is leaking.</h2>
      <p>Get a free audit of your Google, Meta or Amazon ads and your tracking setup. You get a short list of fixes, whether or not you hire us.</p>
    </div>
    <div class="btns">
      <a class="btn primary" href="free-audit.html">Get my free audit</a>
      <a class="btn ghost" href="book-consultation.html">Book a call</a>
    </div>
  </div>
</div>"""


ORG_JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Hrid Digital Group",
"url":"https://hriddigitalgroup.com","logo":"https://hriddigitalgroup.com/assets/logo-600.png",
"email":"info@hriddigitalgroup.com","telephone":"+919404126138","slogan":"Grow. Scale. Succeed.",
"description":"Digital marketing agency for Google Ads, Meta Ads, Amazon Ads, Local Services Ads, LinkedIn Ads, social media, YouTube, Google Business Profile and conversion tracking."}
</script>"""


def head(meta, page_name):
    path = "" if page_name == "index" else f"{page_name}.html"
    title = meta["title"] if page_name == "index" else f'{meta["title"]} | Hrid Digital Group'
    desc = meta.get("description", "")
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{path}">
<meta property="og:image" content="{DOMAIN}/assets/og-image.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/style.css">
{ORG_JSONLD if page_name == "index" else ""}"""


def parse(text):
    meta = dict(re.findall(r"^<!--\s*(\w+):\s*(.*?)\s*-->\s*$", text, flags=re.M))
    body = re.sub(r"^(<!--\s*\w+:.*?-->\s*\n)+", "", text)
    return meta, body


def render(page_name, text, preview):
    meta, body = parse(text)
    body = body.replace("{{cta}}", cta_band())
    for k, v in SITE.items():
        body = body.replace("{{" + k + "}}", str(v))
    inner = f"""{header(meta.get("nav", ""))}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/main.js" defer></script>"""
    h = head(meta, page_name)
    if page_name == "404" and not preview:
        h = '<base href="/">\n' + h  # so links work from any missing URL
    if preview and page_name == "index":
        # The preview host adds its own <html>/<head>/<body> to the main page.
        return f"{h}\n{inner}\n"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{h}
</head>
<body>
{inner}
</body>
</html>
"""


def main():
    preview = "--preview" in sys.argv
    out = ROOT / ("preview" if preview else "site")
    out.mkdir(exist_ok=True)
    names = []
    for f in sorted(PAGES.glob("*.html")):
        (out / f.name).write_text(render(f.stem, f.read_text(), preview))
        names.append(f.stem)
    if not preview:
        urls = "\n".join(
            f"  <url><loc>{DOMAIN}/{'' if n == 'index' else n + '.html'}</loc></url>"
            for n in names if n != "404")
        (out / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print(f"Built {len(names)} pages into {out.name}/")


if __name__ == "__main__":
    main()
