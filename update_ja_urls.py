import re, os

BASE = 'C:/개인/wooahouse/PDFKIT/js'
files = [
    'wooahouse-originals-ja.js',
    'wooahouse-originals-tool-ja.js',
]

def replace_url(m):
    full = m.group(0)
    url = m.group(1)
    if 'pdfkit' in url:
        new_url = url.rstrip('/') + '/ja/'
    else:
        new_url = url.rstrip('/') + '/en/'
    return full.replace(url, new_url)

for fname in files:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(r"url: '(https://[a-z.]+wooahouse\.com)'", replace_url, content)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    count = len(re.findall(r"url: '(https://[a-z.]+wooahouse\.com)'", content))
    print(f'OK {fname}: {count}개 URL 교체')

print('완료!')
