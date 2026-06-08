"""
JA 페이지 SEO 작업 스크립트
1. KO/EN 페이지에 hreflang="ja" 추가
2. sitemap.xml에 JA URLs 추가
"""
import os, re

BASE = 'C:/개인/wooahouse/PDFKIT'
BASE_URL = 'https://pdfkit.wooahouse.com'

# JA 버전이 있는 페이지 목록 (파일명만)
JA_PAGES = [
    ('index.html',          '1.0', 'weekly'),
    ('merge-pdf.html',      '0.9', 'monthly'),
    ('split-pdf.html',      '0.9', 'monthly'),
    ('rotate-pdf.html',     '0.8', 'monthly'),
    ('delete-pages.html',   '0.8', 'monthly'),
    ('compress-pdf.html',   '0.9', 'monthly'),
    ('watermark-pdf.html',  '0.8', 'monthly'),
    ('page-number-pdf.html','0.8', 'monthly'),
    ('unlock-pdf.html',     '0.8', 'monthly'),
    ('pdf-viewer.html',     '0.7', 'monthly'),
    ('pdf-to-jpg.html',     '0.9', 'monthly'),
    ('jpg-to-pdf.html',     '0.9', 'monthly'),
    ('pdf-to-word.html',    '0.9', 'monthly'),
    ('office-to-pdf.html',  '0.9', 'monthly'),
    ('pdf-text-extract.html','0.9','monthly'),
    ('pdf-image-extract.html','0.9','monthly'),
    ('pptx-to-pdf.html',    '0.9', 'monthly'),
    ('pdf-password.html',   '0.8', 'monthly'),
    ('pdf-sign.html',       '0.8', 'monthly'),
    ('pdf-reorder.html',    '0.8', 'monthly'),
    ('pdf-metadata.html',   '0.8', 'monthly'),
    ('pdf-header-footer.html','0.8','monthly'),
    ('pdf-resize.html',     '0.8', 'monthly'),
    ('pdf-compare.html',    '0.8', 'monthly'),
    ('pdf-odd-even.html',   '0.8', 'monthly'),
    ('pdf-to-csv.html',     '0.8', 'monthly'),
    ('pdf-to-epub.html',    '0.8', 'monthly'),
    ('epub-to-pdf.html',    '0.8', 'monthly'),
    ('heic-to-pdf.html',    '0.8', 'monthly'),
    ('about.html',          '0.5', 'monthly'),
    ('privacy.html',        '0.4', 'yearly'),
]

JA_FILENAMES = [p[0] for p in JA_PAGES]


# ── 1. KO 페이지에 hreflang="ja" 추가 ──────────────────────────────────────
def add_hreflang_ko(fname):
    path = os.path.join(BASE, fname)
    if not os.path.isfile(path):
        print(f'SKIP (not found): {fname}')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 이미 추가돼 있으면 스킵
    if f'hreflang="ja"' in content:
        print(f'SKIP (already has ja hreflang): {fname}')
        return
    # <link rel="alternate" hreflang="en" ...> 뒤에 삽입
    ja_tag = f'  <link rel="alternate" hreflang="ja" href="{BASE_URL}/ja/{fname}">\n'
    # x-default 앞에 삽입
    new_content = re.sub(
        r'(<link rel="alternate" hreflang="x-default")',
        ja_tag + r'\1',
        content,
        count=1
    )
    if new_content == content:
        print(f'WARN (pattern not found): {fname}')
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK KO: {fname}')


# ── 2. EN 페이지에 hreflang="ja" 추가 ──────────────────────────────────────
def add_hreflang_en(fname):
    path = os.path.join(BASE, 'en', fname)
    if not os.path.isfile(path):
        print(f'SKIP EN (not found): en/{fname}')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if f'hreflang="ja"' in content:
        print(f'SKIP EN (already has ja hreflang): en/{fname}')
        return
    ja_tag = f'  <link rel="alternate" hreflang="ja" href="{BASE_URL}/ja/{fname}">\n'
    # x-default 앞에 삽입. x-default가 없으면 마지막 hreflang 태그 뒤에
    if 'hreflang="x-default"' in content:
        new_content = re.sub(
            r'(<link rel="alternate" hreflang="x-default")',
            ja_tag + r'\1',
            content,
            count=1
        )
    else:
        # hreflang="en" 뒤에 삽입
        new_content = re.sub(
            r'(<link rel="alternate" hreflang="en"[^>]+>)',
            r'\1\n' + ja_tag.rstrip('\n'),
            content,
            count=1
        )
    if new_content == content:
        print(f'WARN EN (pattern not found): en/{fname}')
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK EN: en/{fname}')


# ── 3. sitemap.xml에 JA section 추가 ────────────────────────────────────────
def add_ja_sitemap():
    sitemap_path = os.path.join(BASE, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '/ja/' in content:
        print('SKIP sitemap (already has /ja/)')
        return

    ja_entries = '\n  <!-- Japanese versions -->\n'
    for fname, priority, changefreq in JA_PAGES:
        ja_entries += f'''  <url>
    <loc>{BASE_URL}/ja/{fname}</loc>
    <lastmod>2026-06-05</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>\n'''

    # </urlset> 바로 앞에 삽입
    new_content = content.replace('</urlset>', ja_entries + '</urlset>')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK sitemap: {len(JA_PAGES)}개 JA URL 추가')


# ── 실행 ─────────────────────────────────────────────────────────────────────
print('=== KO 페이지 hreflang 추가 ===')
for fname in JA_FILENAMES:
    add_hreflang_ko(fname)

print('\n=== EN 페이지 hreflang 추가 ===')
for fname in JA_FILENAMES:
    add_hreflang_en(fname)

print('\n=== sitemap.xml JA 추가 ===')
add_ja_sitemap()

print('\n완료!')
