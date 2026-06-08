"""
og:description / twitter:description 도 meta description과 동기화
"""
import re, os

BASE = 'C:/개인/wooahouse/PDFKIT'

# meta name="description" 의 새 값을 읽어서
# og:description / twitter:description 에 동일하게 적용
# (og/twitter 는 소셜 공유용이라 검색 CTR에 직접 영향은 적지만 일관성 유지)

PAGES = [
    'index.html', 'merge-pdf.html', 'compress-pdf.html', 'split-pdf.html',
    'pdf-image-extract.html', 'pdf-to-jpg.html', 'jpg-to-pdf.html',
    'watermark-pdf.html', 'rotate-pdf.html', 'delete-pages.html',
    'pdf-to-word.html', 'unlock-pdf.html', 'pdf-password.html',
    'pdf-text-extract.html', 'pdf-sign.html', 'office-to-pdf.html',
    'page-number-pdf.html', 'pdf-reorder.html', 'pdf-metadata.html',
    'pdf-header-footer.html', 'pdf-resize.html', 'pdf-compare.html',
    'pdf-odd-even.html', 'pdf-to-csv.html', 'pdf-to-epub.html',
    'epub-to-pdf.html', 'heic-to-pdf.html', 'pdf-viewer.html', 'pptx-to-pdf.html',
]

ok = 0
for fname in PAGES:
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1) 현재 meta name="description" 값 추출
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    if not m:
        print(f'  SKIP (desc 없음): {fname}')
        continue
    new_desc = m.group(1)

    # 2) og:description 교체
    content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_desc + x.group(2),
        content
    )

    # 3) twitter:description 교체
    content = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_desc + x.group(2),
        content
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK: {fname}')
    ok += 1

print(f'\n완료: {ok}개 og/twitter:description 동기화')
