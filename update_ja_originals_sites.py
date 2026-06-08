"""
wooahouse-originals-ja.js / wooahouse-originals-tool-ja.js
SITES 배열의 title/desc를 일본어로 교체
"""
import os, re

BASE_JS = 'C:/개인/wooahouse/PDFKIT/js'

# ── tool 버전 title 교체 맵 ────────────────────────────────────────────
TOOL_TITLES = {
    "'Free Online PDF Tools'":           "'無料オンラインPDFツール'",
    "'Free Online Image Tools'":          "'無料オンライン画像ツール'",
    "'Color Picker & Palette'":           "'カラーピッカー＆パレット'",
    "'Text Transform Tools'":             "'テキスト変換・編集ツール'",
    "'QR Code Generator'":                "'QRコード生成・スキャン'",
    "'Unit Converter & Calculator'":      "'単位変換・計算機'",
    "'Free Commercial Fonts'":            "'無料商用フォント集'",
    "'Essential Mac Apps'":               "'Mac必須アプリ集'",
    "'Essential Windows Programs'":       "'Windows必須ソフト集'",
    "'VS Code Extensions'":               "'VS Code拡張機能集'",
    "'Online Audio Tools'":               "'オンライン音声ツール'",
    "'Online Video Tools'":               "'オンライン動画ツール'",
    "'File Viewer Collection'":           "'ファイルビューア集'",
    "'Developer Tools'":                  "'開発者ツール'",
    "'OCR — Extract Text from Images'":  "'OCR — 画像からテキスト抽出'",
    "'Online Spreadsheet Tools'":         "'オンライン表計算ツール'",
    "'SEO Analysis Tools'":               "'SEO分析ツール'",
    "'Free License Mock Tests'":          "'無料資格模擬試験'",
}

# ── originals 버전 title+desc 교체 맵 ────────────────────────────────
ORIG_REPLACEMENTS = [
    ("'Free Online PDF Tools'",
     "'無料オンラインPDFツール'"),
    ("'Convert, merge, split, compress, rotate & watermark PDFs. Files never leave your browser — 100% safe and free.'",
     "'PDF変換・結合・分割・圧縮・回転・透かし追加。ファイルはブラウザ外に出ず100%安全で無料。'"),
    ("'Free Online Image Tools'",
     "'無料オンライン画像ツール'"),
    ("'Compress, resize, convert & remove backgrounds — all in your browser, no upload needed.'",
     "'圧縮・リサイズ・変換・背景削除をブラウザで直接。アップロード不要。'"),
    ("'Color Picker & Palette Generator'",
     "'カラーピッカー＆パレット生成'"),
    ("'Extract colors from images, convert HEX/RGB, and generate beautiful palettes instantly.'",
     "'画像から色を抽出、HEX/RGB変換、美しいパレットを瞬時に生成。'"),
    ("'Text Transform & Edit Tools'",
     "'テキスト変換・編集ツール'"),
    ("'Convert, sort, number lines, and edit text — all your text tasks in one place.'",
     "'テキスト変換・整列・行番号追加など多様なテキスト作業を一箇所で。'"),
    ("'QR Code Generator & Scanner'",
     "'QRコード生成・スキャン'"),
    ("'Generate QR codes for URLs, text, contacts and more — free, fast, no limits.'",
     "'URL・テキスト・連絡先など多様なQRコードを無料で制限なく生成。'"),
    ("'Unit Converter & Calculator'",
     "'単位変換・計算機'"),
    ("'Convert length, weight, temperature and more. Calculate formulas in one place.'",
     "'長さ・重さ・温度などの単位変換と数式計算を一箇所で。'"),
    ("'Free Commercial Fonts'",
     "'無料商用フォント集'"),
    ("'Handpicked free fonts for commercial use — official download links, no copyright worries.'",
     "'著作権の心配なく使える無料商用フォントの公式ダウンロードリンク集。'"),
    ("'Essential Mac Apps'",
     "'Mac必須アプリ集'"),
    ("'Must-have apps after buying or reformatting a Mac — all official download links.'",
     "'Mac購入・再フォーマット後に入れるべき必須アプリの公式リンク集。'"),
    ("'Essential Windows Programs'",
     "'Windows必須ソフト集'"),
    ("'Must-have programs after a Windows reformat — all official download links.'",
     "'Windowsフォーマット後に必要な必須プログラムの公式リンク集。'"),
    ("'VS Code Extensions Collection'",
     "'VS Code拡張機能集'"),
    ("'Curated VS Code extensions to boost your development productivity.'",
     "'開発生産性を上げるVS Code拡張機能のおすすめ厳選集。'"),
    ("'Online Audio Tools'",
     "'オンライン音声ツール'"),
    ("'Convert, edit, trim, and record audio — all free, directly in your browser.'",
     "'変換・編集・トリミング・録音など音声作業を無料でブラウザから。'"),
    ("'Online Video Tools'",
     "'オンライン動画ツール'"),
    ("'Convert, compress, and edit videos — free, no upload to server required.'",
     "'変換・圧縮・編集などの動画作業を無料で。サーバーへのアップロード不要。'"),
    ("'File Viewer Collection'",
     "'ファイルビューア集'"),
    ("'Open and view various file formats directly in your browser — no software needed.'",
     "'様々なファイル形式をブラウザで直接表示。ソフトウェアのインストール不要。'"),
    ("'Developer Tools'",
     "'開発者ツール'"),
    ("'JSON formatter, Base64, URL encoder and more dev tools — all in one place.'",
     "'JSONフォーマッター・Base64・URLエンコーダーなど開発ツールを一箇所に。'"),
    ("'OCR — Extract Text from Images'",
     "'OCR — 画像からテキスト抽出'"),
    ("'Automatically recognize and extract text from images and scanned documents.'",
     "'画像やスキャン文書からテキストを自動認識して抽出。'"),
    ("'Online Spreadsheet Tools'",
     "'オンライン表計算ツール'"),
    ("'Open, edit, and convert CSV & Excel files directly in your browser.'",
     "'CSV・Excelファイルをブラウザで直接開いて編集・変換。'"),
    ("'SEO Analysis Tools'",
     "'SEO分析ツール'"),
    ("'Analyze SEO scores, research keywords, and generate meta tags for your website.'",
     "'SEOスコア分析・キーワードリサーチ・メタタグ生成であなたのサイトを最適化。'"),
    ("'Free License Mock Tests'",
     "'無料資格模擬試験'"),
    ("'Practice for driving licenses and certification exams — 49 exam types, free.'",
     "'免許・資格試験の練習を49種のジャンルで無料実施。'"),
]


def apply_replacements(path, replacements):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# ── tool 버전 ─────────────────────────────────────────────────────────
tool_ja = os.path.join(BASE_JS, 'wooahouse-originals-tool-ja.js')
apply_replacements(tool_ja, list(TOOL_TITLES.items()))
print(f'OK: wooahouse-originals-tool-ja.js ({len(TOOL_TITLES)}개 제목 교체)')

# ── originals 버전 ────────────────────────────────────────────────────
orig_ja = os.path.join(BASE_JS, 'wooahouse-originals-ja.js')
apply_replacements(orig_ja, ORIG_REPLACEMENTS)
print(f'OK: wooahouse-originals-ja.js ({len(ORIG_REPLACEMENTS)}개 title/desc 교체)')

print('\n완료!')
