"""
1. hreflang="ja" 들여쓰기 수정 (4칸→2칸, x-default 0칸→2칸)
2. about.html / privacy.html (KO/EN)에 hreflang 블록 추가
"""
import os, re

BASE = 'C:/개인/wooahouse/PDFKIT'
BASE_URL = 'https://pdfkit.wooahouse.com'

# ── 1. 들여쓰기 수정 ──────────────────────────────────────────────────────────
# 이전 스크립트가 만든 잘못된 패턴:
#   "    <link rel=\"alternate\" hreflang=\"ja\" ..." (4칸)
# + "<link rel=\"alternate\" hreflang=\"x-default\" ..." (0칸)
# → 둘 다 2칸으로 정규화

PAGES_WITH_HREFLANG = [
    'index.html','merge-pdf.html','split-pdf.html','rotate-pdf.html',
    'delete-pages.html','compress-pdf.html','watermark-pdf.html',
    'page-number-pdf.html','unlock-pdf.html','pdf-viewer.html',
    'pdf-to-jpg.html','jpg-to-pdf.html','pdf-to-word.html',
    'office-to-pdf.html','pdf-text-extract.html','pdf-image-extract.html',
    'pptx-to-pdf.html','pdf-password.html','pdf-sign.html',
    'pdf-reorder.html','pdf-metadata.html','pdf-header-footer.html',
    'pdf-resize.html','pdf-compare.html','pdf-odd-even.html',
    'pdf-to-csv.html','pdf-to-epub.html','epub-to-pdf.html',
    'heic-to-pdf.html',
]

def fix_indent(path, fname):
    if not os.path.isfile(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 4칸 ja 태그 → 2칸
    content = re.sub(
        r'    (<link rel="alternate" hreflang="ja")',
        r'  \1',
        content
    )
    # 0칸 x-default 태그 → 2칸 (이미 2칸인 경우 제외)
    content = re.sub(
        r'\n(<link rel="alternate" hreflang="x-default")',
        r'\n  \1',
        content
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'FIX indent: {fname}')

print('=== 들여쓰기 수정 ===')
for fname in PAGES_WITH_HREFLANG:
    fix_indent(os.path.join(BASE, fname), fname)
    fix_indent(os.path.join(BASE, 'en', fname), f'en/{fname}')

# ── 2. about.html / privacy.html에 hreflang 추가 ─────────────────────────────
def add_hreflang_to_page(path, fname, ko_url, en_url, ja_url):
    if not os.path.isfile(path):
        print(f'SKIP: {path}')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'hreflang' in content:
        print(f'SKIP (already has hreflang): {fname}')
        return
    hreflang_block = (
        f'  <link rel="alternate" hreflang="ko" href="{ko_url}">\n'
        f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'  <link rel="alternate" hreflang="ja" href="{ja_url}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{en_url}">\n'
    )
    # <link rel="canonical" 앞 또는 <meta name="description" 앞에 삽입
    if '<link rel="canonical"' in content:
        new_content = content.replace(
            '<link rel="canonical"',
            hreflang_block + '<link rel="canonical"',
            1
        )
    elif '<meta name="description"' in content:
        new_content = content.replace(
            '<meta name="description"',
            hreflang_block + '<meta name="description"',
            1
        )
    else:
        # <title> 앞에 삽입
        new_content = content.replace('<title>', hreflang_block + '<title>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK hreflang: {fname}')

print('\n=== about/privacy hreflang 추가 ===')
for fname in ['about.html', 'privacy.html']:
    ko_url = f'{BASE_URL}/{fname}'
    en_url = f'{BASE_URL}/en/{fname}'
    ja_url = f'{BASE_URL}/ja/{fname}'
    add_hreflang_to_page(os.path.join(BASE, fname), fname, ko_url, en_url, ja_url)
    add_hreflang_to_page(os.path.join(BASE, 'en', fname), f'en/{fname}', ko_url, en_url, ja_url)

print('\n완료!')
