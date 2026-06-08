"""
JA 페이지 originals 스크립트 교체
- index.html: tool-en.js → ja.js (리치 카드 버전)
- 도구 페이지: tool-en.js → tool-ja.js (일본어 헤딩)
"""
import os, glob

BASE = 'C:/개인/wooahouse/PDFKIT/ja'

# index.html: wooahouse-originals-tool-en.js → wooahouse-originals-ja.js
index_path = os.path.join(BASE, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()
new_content = content.replace(
    '../js/wooahouse-originals-tool-en.js',
    '../js/wooahouse-originals-ja.js'
)
if new_content != content:
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK index.html → originals-ja.js')
else:
    print(f'SKIP index.html (no change)')

# 도구 페이지: wooahouse-originals-tool-en.js → wooahouse-originals-tool-ja.js
skip = {'index.html', 'about.html', 'privacy.html'}
changed = 0
for fpath in glob.glob(os.path.join(BASE, '*.html')):
    fname = os.path.basename(fpath)
    if fname in skip:
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content.replace(
        '../js/wooahouse-originals-tool-en.js',
        '../js/wooahouse-originals-tool-ja.js'
    )
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed += 1
        print(f'OK {fname}')

print(f'\n총 {changed}개 도구 페이지 → originals-tool-ja.js')
