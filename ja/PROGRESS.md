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

## Batch 1: 共通ページ ✅
- [x] `ja/index.html`
- [x] `ja/about.html`
- [x] `ja/privacy.html`

## Batch 2: 基本編集ツール ✅
- [x] `ja/merge-pdf.html`
- [x] `ja/split-pdf.html`
- [x] `ja/rotate-pdf.html`
- [x] `ja/delete-pages.html`
- [x] `ja/compress-pdf.html`

## Batch 3: 変換ツール A ✅
- [x] `ja/pdf-to-jpg.html`
- [x] `ja/jpg-to-pdf.html`
- [x] `ja/watermark-pdf.html`
- [x] `ja/page-number-pdf.html`
- [x] `ja/unlock-pdf.html`

## Batch 4: 変換ツール B ✅
- [x] `ja/pdf-to-word.html`
- [x] `ja/office-to-pdf.html`
- [x] `ja/pdf-text-extract.html`
- [x] `ja/pdf-image-extract.html`
- [x] `ja/pptx-to-pdf.html`

## Batch 5: 高度な編集ツール ✅
- [x] `ja/pdf-password.html`
- [x] `ja/pdf-sign.html`
- [x] `ja/pdf-reorder.html`
- [x] `ja/pdf-metadata.html`
- [x] `ja/pdf-header-footer.html`

## Batch 6: その他ツール ✅
- [x] `ja/pdf-resize.html`
- [x] `ja/pdf-viewer.html`
- [x] `ja/pdf-compare.html`
- [x] `ja/pdf-odd-even.html`
- [x] `ja/pdf-to-csv.html`

## Batch 7: eBook・特殊 ✅
- [x] `ja/pdf-to-epub.html`
- [x] `ja/epub-to-pdf.html`
- [x] `ja/heic-to-pdf.html`

## 最終作業 ✅
- [x] `js/wooa-sidebar-ja.js` / `js/wooa-footer-ja.js` を PDFKIT/js/ に配備
- [x] `deploy_shared_js.py` に JA ファイル追加（将来の一括配布用）
- [x] `PDFKIT/sitemap.xml` に /ja/ URL 31件追加
- [x] KO・ENページ全体 (31ページ×2) に `hreflang="ja"` タグ追加
- [x] `wooa-sites-bar.js` に `/ja/` パス検知追加（日本語ラベル対応）
- [ ] `PDFKIT/CLAUDE.md` ファイル構造更新
- [ ] git push (ユーザー確認後)

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
