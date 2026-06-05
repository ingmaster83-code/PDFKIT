# WooaPDF 日本語版 (/ja/) 作成進捗

> **次のClaudeへ:** このファイルのチェックリストを確認し、[ ] の項目から再開してください。
> 完了したら [x] に更新してコミットしてください。
> EN版 (`PDFKIT/en/`) をベースに日本語化します。
> lang属性: `ja`, og:locale: `ja_JP`, パス接頭辞: `../`

---

## 規則 (毎ページ共通)
- `<html lang="ja">`
- canonical: `https://pdfkit.wooahouse.com/ja/{page}`
- hreflang: ko + en + ja + x-default(en)
- `og:locale`: `ja_JP`
- CSS/JS パス: `../` 接頭辞
- サイドバー: `../js/wooa-sidebar-ja.js`
- フッター: `../js/wooa-footer-ja.js`
- Originalsツール: `../js/wooahouse-originals-tool-en.js`
- lang-switcher: KO | EN | JA (JAをactive)
- ld+json `inLanguage`: `"ja"`

---

## Batch 0: インフラ ✅
- [x] `PDFKIT/ja/PROGRESS.md` (このファイル)
- [x] `shared-js/wooa-sidebar-ja.js`
- [x] `shared-js/wooa-footer-ja.js`
- [ ] `PDFKIT/js/wooa-sidebar-ja.js` (deploy_shared_js.py で配布 — 最後にまとめて)
- [ ] `PDFKIT/js/wooa-footer-ja.js` (同上)

## Batch 1: 共通ページ
- [x] `ja/index.html`
- [ ] `ja/about.html`
- [ ] `ja/privacy.html`

## Batch 2: 基本編集ツール ✅
- [x] `ja/merge-pdf.html`
- [x] `ja/split-pdf.html`
- [x] `ja/rotate-pdf.html`
- [x] `ja/delete-pages.html`
- [x] `ja/compress-pdf.html`

## Batch 3: 変換ツール A
- [ ] `ja/pdf-to-jpg.html`
- [ ] `ja/jpg-to-pdf.html`
- [ ] `ja/watermark-pdf.html`
- [ ] `ja/page-number-pdf.html`
- [ ] `ja/unlock-pdf.html`

## Batch 4: 変換ツール B
- [ ] `ja/pdf-to-word.html`
- [ ] `ja/office-to-pdf.html`
- [ ] `ja/pdf-text-extract.html`
- [ ] `ja/pdf-image-extract.html`
- [ ] `ja/pptx-to-pdf.html`

## Batch 5: 高度な編集ツール
- [ ] `ja/pdf-password.html`
- [ ] `ja/pdf-sign.html`
- [ ] `ja/pdf-reorder.html`
- [ ] `ja/pdf-metadata.html`
- [ ] `ja/pdf-header-footer.html`

## Batch 6: その他ツール
- [ ] `ja/pdf-resize.html`
- [ ] `ja/pdf-viewer.html`
- [ ] `ja/pdf-compare.html`
- [ ] `ja/pdf-odd-even.html`
- [ ] `ja/pdf-to-csv.html`

## Batch 7: eBook・特殊
- [ ] `ja/pdf-to-epub.html`
- [ ] `ja/epub-to-pdf.html`
- [ ] `ja/heic-to-pdf.html`

## 最終作業 (全ページ完了後)
- [ ] `deploy_shared_js.py` 実行 → 各サイトの js/ に wooa-sidebar-ja.js・wooa-footer-ja.js を配布
- [ ] `PDFKIT/sitemap.xml` に /ja/ URL追加
- [ ] KO・ENページ全体に `hreflang="ja"` タグ追加
- [ ] `wooa-sites-bar.js` に `/ja/` パス検知追加
- [ ] `PDFKIT/CLAUDE.md` ファイル構造更新
- [ ] git commit & push (ユーザー確認後)

---

## 日本語訳 共通UI文字列
| EN | JA |
|---|---|
| Home | ホーム |
| All Tools | すべてのツール |
| About | About |
| FREE | 無料 |
| NEW | NEW |
| Drop files here | ここにファイルをドロップ |
| Select File | ファイルを選択 |
| Processing... | 処理中... |
| Done! | 完了！ |
| Download | ダウンロード |
| Frequently Asked Questions | よくある質問 |
| Files never leave your browser | ファイルはブラウザ外に出ません |
