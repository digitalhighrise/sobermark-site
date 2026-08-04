"""Generate guides/index.html and sitemap.xml from the article files. Run from repo root."""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
GUIDES = os.path.join(ROOT, 'guides')

SECTIONS = [
    ('Best of 2026', lambda s: s.startswith('best-')),
    ('Head to head', lambda s: '-vs-' in s),
    ('Alternatives', lambda s: s.endswith('-alternatives')),
]

arts = []
for fn in sorted(os.listdir(GUIDES)):
    if not fn.endswith('.html') or fn == 'index.html':
        continue
    src = open(os.path.join(GUIDES, fn), encoding='utf-8').read()
    slug = fn[:-5]
    h1 = re.search(r'<h1>(.*?)</h1>', src, re.S)
    md = re.search(r'name="description" content="(.*?)"', src)
    arts.append((slug, h1.group(1).strip() if h1 else slug, md.group(1) if md else ''))

cards = []
for label, pred in SECTIONS:
    items = [a for a in arts if pred(a[0])]
    if not items:
        continue
    lis = '\n'.join(
        f'      <li><a href="/guides/{s}.html">{html.escape(re.sub("<.*?>", "", t))}</a><br /><span class="g-desc">{d}</span></li>'
        for s, t, d in items)
    cards.append(f'  <section class="art-card">\n    <h2>{label}</h2>\n    <ul class="g-list">\n{lis}\n    </ul>\n  </section>')

page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Guides | Sobermark</title>
  <meta name="description" content="Honest guides from the Sobermark team: the best sobriety, quit smoking and habit tracking apps in 2026, head to head comparisons and alternatives." />
  <link rel="canonical" href="https://sobermark.app/guides/" />
  <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
  <link rel="stylesheet" href="/css/styles.css" />
  <style>
    .art-wrap {{ max-width: 760px; margin: 0 auto; padding: 140px 24px 80px; }}
    .art-wrap h1 {{ font-size: clamp(2rem, 5vw, 2.6rem); letter-spacing: -0.03em; margin: 0 0 8px; }}
    .art-meta {{ color: #5E6E9C; font-size: 0.95rem; margin: 0 0 28px; }}
    .art-card {{ background: #fff; border: 1px solid #D3DEF4; border-radius: 18px; padding: 24px 26px; margin-bottom: 18px; box-shadow: 0 4px 12px rgba(23,51,123,0.05); }}
    .art-card h2 {{ margin: 0 0 10px; font-size: 1.3rem; }}
    .g-list {{ margin: 0; padding-left: 0; list-style: none; }}
    .g-list li {{ margin: 0 0 14px; line-height: 1.5; }}
    .g-list a {{ color: #2F6BFF; font-weight: 600; text-decoration: none; }}
    .g-list a:hover {{ text-decoration: underline; }}
    .g-desc {{ color: #5E6E9C; font-size: 0.92rem; }}
  </style>
  <script defer src="/analytics.js"></script>
</head>
<body>
<header class="nav-wrap">
  <nav class="nav" aria-label="Main">
    <a href="/" class="brand">
      <span class="brand-mark"><img src="/assets/bern-front.webp" alt="" width="46" height="46" /></span>
      <span class="brand-word">sobermark</span>
    </a>
    <div class="nav-links">
      <a href="/#features">Features</a>
      <a href="/#faq">Pricing</a>
      <a href="/#bern">About</a>
    </div>
  </nav>
</header>
<main class="art-wrap">
  <h1>Guides</h1>
  <p class="art-meta">Honest write-ups from the Sobermark team. We make one of the apps covered here, and we say so every time.</p>
{chr(10).join(cards)}
</main>
<footer class="footer">
  <div class="footer-bottom">
    <span>&copy; 2026 Sobermark. One day at a time.</span>
    <span><a href="/">Home</a> &middot; <a href="/privacy.html">Privacy</a></span>
  </div>
</footer>
</body>
</html>
'''
open(os.path.join(GUIDES, 'index.html'), 'w', encoding='utf-8').write(page)

urls = ['<url><loc>https://sobermark.app/</loc><lastmod>2026-08-04</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>',
        '<url><loc>https://sobermark.app/privacy.html</loc><lastmod>2026-08-04</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>',
        '<url><loc>https://sobermark.app/guides/</loc><lastmod>2026-08-04</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>']
for s, t, d in arts:
    urls.append(f'<url><loc>https://sobermark.app/guides/{s}.html</loc><lastmod>2026-08-04</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>')
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  ' + '\n  '.join(urls) + '\n</urlset>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
print(f'index + sitemap written for {len(arts)} articles')
