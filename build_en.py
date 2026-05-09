"""
PDFKit 영어 버전 자동 생성 스크립트
실행: python build_en.py
결과: en/ 폴더에 영어 버전 HTML 파일 생성
"""

import os, re, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(BASE, 'en')
os.makedirs(EN_DIR, exist_ok=True)

# ── 1. 페이지별 메타 번역 ─────────────────────────────────────────────────────
PAGE_META = {
    'pdf-to-jpg.html': {
        'title': 'PDF to JPG Converter Free Online – Convert PDF to Image | WooaPDF',
        'desc':  'Convert PDF to JPG or PNG images for free. High-quality output, select page range. Files never leave your browser — 100% private.',
        'kw':    'PDF to JPG, PDF to image, convert PDF to JPG free, PDF to PNG, PDF image extractor, online PDF converter',
        'og_title': 'PDF to JPG Converter – Free Online | WooaPDF',
        'og_desc':  'Convert PDF pages to high-quality JPG or PNG images. No upload, no signup. Runs entirely in your browser.',
        'app_name': 'PDF to JPG Converter',
        'faq': [
            ('Does converting PDF to JPG reduce quality?',
             'Quality depends on DPI setting. The default 150 DPI provides sufficient quality for most uses.'),
            ('How many pages can I convert at once?',
             'All pages in a PDF can be converted to JPG at once. Custom page range selection is also supported.'),
            ('Are converted images stored on a server?',
             'No. All conversion happens locally in your browser and nothing is stored on any server.'),
        ],
        'h1': 'PDF to JPG Converter – Free Online',
        'tool_desc': 'Upload a PDF and each page will be converted to an image. Files are processed in your browser only — never sent to a server.',
        'breadcrumb': 'PDF → JPG',
        'cross_banner_text': 'Want to compress or edit the converted JPG images?',
        'cross_banner_link_text': '🖼️ WooaImage – Image Compress →',
        'cross_banner_href': 'https://imagekit.wooahouse.com/compress-image.html',
    },
    'jpg-to-pdf.html': {
        'title': 'Image to PDF Converter Free Online – JPG PNG to PDF | WooaPDF',
        'desc':  'Convert JPG, PNG and other images to PDF for free. Drag & drop multiple images, set page size and margin. 100% browser-based, no upload.',
        'kw':    'image to PDF, JPG to PDF, PNG to PDF, convert image to PDF free, photo to PDF, online image PDF converter',
        'og_title': 'Image to PDF – Free Online Converter | WooaPDF',
        'og_desc':  'Convert JPG, PNG images to PDF instantly. Drag & drop, set page size, download. No signup, no upload.',
        'app_name': 'Image to PDF Converter',
        'faq': [
            ('What image formats are supported?',
             'JPG, PNG, WebP, GIF, and BMP are all supported.'),
            ('Can I combine multiple images into one PDF?',
             'Yes. Add multiple images and they will be combined into a single PDF in the order you arrange them.'),
            ('Are my images uploaded to a server?',
             'No. All processing is done locally in your browser. Your files are never sent anywhere.'),
        ],
        'h1': 'Image to PDF Converter – Free Online',
        'tool_desc': 'Upload JPG, PNG or other images to convert them into a PDF document. Reorder pages before converting. Everything runs in your browser.',
        'breadcrumb': 'Image → PDF',
        'cross_banner_text': 'Need to edit or compress images before converting?',
        'cross_banner_link_text': '🖼️ WooaImage – Image Tools →',
        'cross_banner_href': 'https://imagekit.wooahouse.com/',
    },
    'merge-pdf.html': {
        'title': 'Merge PDF Free Online – Combine PDF Files | WooaPDF',
        'desc':  'Merge multiple PDF files into one for free. Drag & drop to reorder, then click to combine. No signup, files never leave your browser.',
        'kw':    'merge PDF, combine PDF, join PDF files, merge PDF free, PDF merger online, combine multiple PDF',
        'og_title': 'Merge PDF Free – Combine PDF Files Online | WooaPDF',
        'og_desc':  'Combine multiple PDFs into one. Drag & drop to reorder pages, merge with one click. Free, no signup.',
        'app_name': 'PDF Merger',
        'faq': [
            ('How many PDF files can I merge?',
             'There is no limit on the number of files you can merge.'),
            ('Can I reorder the files before merging?',
             'Yes. Drag and drop the files to arrange them in any order before merging.'),
            ('Can password-protected PDFs be merged?',
             'Remove the password first using the Unlock PDF tool, then merge.'),
        ],
        'h1': 'Merge PDF – Free Online',
        'tool_desc': 'Upload multiple PDF files and combine them into one. Drag to reorder, then click Merge. All processing happens in your browser.',
        'breadcrumb': 'Merge PDF',
        'cross_banner_text': 'Want to compress the merged PDF to reduce file size?',
        'cross_banner_link_text': '🗜️ Compress PDF →',
        'cross_banner_href': 'compress-pdf.html',
    },
    'split-pdf.html': {
        'title': 'Split PDF Free Online – Split PDF by Page | WooaPDF',
        'desc':  'Split a PDF into individual pages or custom page ranges for free. No signup required. Files processed entirely in your browser.',
        'kw':    'split PDF, split PDF by page, PDF splitter online, extract PDF pages, divide PDF, PDF page extractor free',
        'og_title': 'Split PDF Free – Online PDF Splitter | WooaPDF',
        'og_desc':  'Split PDF into separate pages or page ranges. Free, no signup. All processing in your browser.',
        'app_name': 'PDF Splitter',
        'faq': [
            ('Can I split by specific page ranges?',
             'Yes. You can specify custom page ranges like 1-3, 5, 7-10 to extract exactly the pages you need.'),
            ('Will the split PDFs be downloaded individually?',
             'Yes. Each split section is downloaded as a separate PDF file.'),
            ('Is there a page limit?',
             'No. You can split PDFs of any length.'),
        ],
        'h1': 'Split PDF – Free Online',
        'tool_desc': 'Upload a PDF and split it into separate pages or custom ranges. Download individual pages or groups. Runs entirely in your browser.',
        'breadcrumb': 'Split PDF',
        'cross_banner_text': 'Want to merge PDFs instead?',
        'cross_banner_link_text': '🔗 Merge PDF →',
        'cross_banner_href': 'merge-pdf.html',
    },
    'compress-pdf.html': {
        'title': 'Compress PDF Free Online – Reduce PDF File Size | WooaPDF',
        'desc':  'Compress PDF files to reduce size for free. No quality loss. Files processed in browser — never uploaded to a server.',
        'kw':    'compress PDF, reduce PDF size, PDF compressor online, shrink PDF, PDF file size reducer, compress PDF free',
        'og_title': 'Compress PDF Free – Reduce PDF Size Online | WooaPDF',
        'og_desc':  'Reduce PDF file size without losing quality. Free, no signup. Browser-based — no server upload.',
        'app_name': 'PDF Compressor',
        'faq': [
            ('How much can PDF size be reduced?',
             'Compression ratio varies by content. Image-heavy PDFs typically see 30–70% size reduction.'),
            ('Will compression reduce quality?',
             'Text quality is maintained. Image quality may be slightly reduced depending on compression level.'),
            ('Is there a file size limit?',
             'No strict limit, though very large PDFs may take longer to process.'),
        ],
        'h1': 'Compress PDF – Free Online',
        'tool_desc': 'Upload a PDF to reduce its file size. Great for email attachments and easy sharing. All processing happens locally in your browser.',
        'breadcrumb': 'Compress PDF',
        'cross_banner_text': 'Need to merge PDFs after compressing?',
        'cross_banner_link_text': '🔗 Merge PDF →',
        'cross_banner_href': 'merge-pdf.html',
    },
    'rotate-pdf.html': {
        'title': 'Rotate PDF Free Online – Rotate PDF Pages | WooaPDF',
        'desc':  'Rotate PDF pages 90°, 180°, or 270° for free. Rotate all pages or individual pages. No signup. Files stay in your browser.',
        'kw':    'rotate PDF, rotate PDF pages, PDF rotation online, fix PDF orientation, rotate PDF 90 degrees free',
        'og_title': 'Rotate PDF Pages Free Online | WooaPDF',
        'og_desc':  'Rotate PDF pages 90°, 180°, or 270°. Rotate all or specific pages. Free, no upload to server.',
        'app_name': 'PDF Page Rotator',
        'faq': [
            ('Can I rotate only specific pages?',
             'Yes. You can choose to rotate all pages or select individual pages to rotate.'),
            ('What rotation angles are supported?',
             '90°, 180°, and 270° rotations are supported.'),
            ('Is the rotated PDF re-uploaded to a server?',
             'No. Everything runs in your browser. No files are sent to any server.'),
        ],
        'h1': 'Rotate PDF Pages – Free Online',
        'tool_desc': 'Upload a PDF and rotate pages to the correct orientation. Choose 90°, 180°, or 270°. All processing is done in your browser.',
        'breadcrumb': 'Rotate PDF',
        'cross_banner_text': 'Need to delete unwanted pages from your PDF?',
        'cross_banner_link_text': '🗑️ Delete PDF Pages →',
        'cross_banner_href': 'delete-pages.html',
    },
    'delete-pages.html': {
        'title': 'Delete PDF Pages Free Online – Remove Pages from PDF | WooaPDF',
        'desc':  'Delete specific pages from a PDF for free. Select pages to remove and download the result. No signup. 100% browser-based.',
        'kw':    'delete PDF pages, remove pages from PDF, PDF page remover, delete pages from PDF free, extract remove PDF pages',
        'og_title': 'Delete PDF Pages Free Online | WooaPDF',
        'og_desc':  'Select and remove unwanted pages from your PDF. Free, no signup. Files processed in browser only.',
        'app_name': 'PDF Page Deleter',
        'faq': [
            ('Can I delete multiple pages at once?',
             'Yes. Select all the pages you want to delete and they will all be removed at once.'),
            ('Will the remaining pages be renumbered?',
             'Yes. The remaining pages will be in order after deletion.'),
            ('Can I preview pages before deleting?',
             'Yes. Page thumbnails are shown so you can select the exact pages to delete.'),
        ],
        'h1': 'Delete PDF Pages – Free Online',
        'tool_desc': 'Upload a PDF and select pages to delete. Preview thumbnails help you choose the right pages. Processed entirely in your browser.',
        'breadcrumb': 'Delete Pages',
        'cross_banner_text': 'Want to reorder pages instead of deleting?',
        'cross_banner_link_text': '🔀 Reorder PDF Pages →',
        'cross_banner_href': 'pdf-reorder.html',
    },
    'watermark-pdf.html': {
        'title': 'Add Watermark to PDF Free Online – Text Watermark | WooaPDF',
        'desc':  'Add a text watermark to PDF pages for free. Customize font, size, color, and opacity. No signup. Files never leave your browser.',
        'kw':    'watermark PDF, add watermark to PDF, PDF watermark online, text watermark PDF free, stamp PDF',
        'og_title': 'Add Watermark to PDF Free Online | WooaPDF',
        'og_desc':  'Add custom text watermarks to your PDF. Set font, color, opacity and position. Free, no upload to server.',
        'app_name': 'PDF Watermark Tool',
        'faq': [
            ('Can I customize the watermark appearance?',
             'Yes. You can set the text, font size, color, opacity, angle, and position of the watermark.'),
            ('Can I add watermark to specific pages only?',
             'Yes. You can apply the watermark to all pages or selected pages only.'),
            ('Is the watermark permanent?',
             'Yes. The watermark is embedded into the PDF and cannot be easily removed.'),
        ],
        'h1': 'Add Watermark to PDF – Free Online',
        'tool_desc': 'Upload a PDF and add a custom text watermark. Adjust font, size, color, opacity, and angle. Everything runs in your browser.',
        'breadcrumb': 'Add Watermark',
        'cross_banner_text': 'Need to protect your PDF with a password?',
        'cross_banner_link_text': '🔐 Protect PDF →',
        'cross_banner_href': 'pdf-password.html',
    },
    'page-number-pdf.html': {
        'title': 'Add Page Numbers to PDF Free Online | WooaPDF',
        'desc':  'Automatically add page numbers to PDF pages for free. Choose position, font size, and starting number. No signup. Browser-based.',
        'kw':    'add page numbers to PDF, PDF page numbering, number PDF pages, PDF pagination online free',
        'og_title': 'Add Page Numbers to PDF Free Online | WooaPDF',
        'og_desc':  'Add page numbers to your PDF automatically. Set position, font, and start number. Free, no server upload.',
        'app_name': 'PDF Page Numbering Tool',
        'faq': [
            ('Can I choose where page numbers appear?',
             'Yes. You can place page numbers at the top or bottom, and left, center, or right.'),
            ('Can I set a custom starting number?',
             'Yes. You can start page numbering from any number you choose.'),
            ('Are my files sent to a server?',
             'No. All processing happens locally in your browser.'),
        ],
        'h1': 'Add Page Numbers to PDF – Free Online',
        'tool_desc': 'Upload a PDF and add page numbers automatically. Choose position, font size, and starting number. All done in your browser.',
        'breadcrumb': 'Page Numbers',
        'cross_banner_text': 'Want to add a watermark to your PDF?',
        'cross_banner_link_text': '💧 Add Watermark →',
        'cross_banner_href': 'watermark-pdf.html',
    },
    'unlock-pdf.html': {
        'title': 'Unlock PDF Free Online – Remove PDF Password | WooaPDF',
        'desc':  'Remove password protection from PDF files for free. Unlock PDF instantly in your browser. No signup. Files never leave your device.',
        'kw':    'unlock PDF, remove PDF password, PDF password remover, unlock PDF free, decrypt PDF online',
        'og_title': 'Unlock PDF Free – Remove Password Online | WooaPDF',
        'og_desc':  'Remove password protection from your PDF. Enter the password and unlock instantly. Free, no server upload.',
        'app_name': 'PDF Unlock Tool',
        'faq': [
            ('Do I need to know the PDF password?',
             'Yes. You must enter the correct password to unlock the PDF.'),
            ('What types of PDF protection can be removed?',
             'Open password protection can be removed. Some permission restrictions may also be lifted.'),
            ('Is unlocking secure?',
             'Yes. All processing happens in your browser. The password is never sent to any server.'),
        ],
        'h1': 'Unlock PDF – Remove Password Free Online',
        'tool_desc': 'Enter the PDF password to unlock and remove protection. Download the unlocked PDF. All processing is local — files never leave your browser.',
        'breadcrumb': 'Unlock PDF',
        'cross_banner_text': 'Want to protect a PDF with a password?',
        'cross_banner_link_text': '🔐 Protect PDF →',
        'cross_banner_href': 'pdf-password.html',
    },
    'pdf-password.html': {
        'title': 'Protect PDF with Password Free Online | WooaPDF',
        'desc':  'Add password protection to your PDF for free. Set an open password and restrict permissions. No signup. 100% browser-based.',
        'kw':    'protect PDF, PDF password, add password to PDF, encrypt PDF online free, secure PDF with password',
        'og_title': 'Protect PDF with Password Free Online | WooaPDF',
        'og_desc':  'Set a password on your PDF to restrict access. Customize permissions. Free, no upload to server.',
        'app_name': 'PDF Password Protect Tool',
        'faq': [
            ('What types of protection can I set?',
             'You can set an open password to prevent unauthorized viewing, and restrict printing or copying.'),
            ('Can I remove the password later?',
             'Yes, use the Unlock PDF tool to remove the password when needed.'),
            ('Is my PDF sent to a server?',
             'No. All encryption happens locally in your browser.'),
        ],
        'h1': 'Protect PDF with Password – Free Online',
        'tool_desc': 'Upload a PDF and set a password to restrict access. Customize permissions like printing and copying. All done locally in your browser.',
        'breadcrumb': 'Protect PDF',
        'cross_banner_text': 'Need to remove a PDF password instead?',
        'cross_banner_link_text': '🔓 Unlock PDF →',
        'cross_banner_href': 'unlock-pdf.html',
    },
    'pdf-sign.html': {
        'title': 'Sign PDF Free Online – Add Signature to PDF | WooaPDF',
        'desc':  'Draw or type your signature and insert it into a PDF for free. No signup required. Files processed entirely in your browser.',
        'kw':    'sign PDF, add signature to PDF, PDF signature online free, e-sign PDF, electronic signature PDF',
        'og_title': 'Sign PDF Free Online – Add Signature | WooaPDF',
        'og_desc':  'Draw your signature on a canvas and add it to your PDF. Free, no signup, no server upload.',
        'app_name': 'PDF Signature Tool',
        'faq': [
            ('Can I draw my own signature?',
             'Yes. Use the canvas to draw your signature with a mouse or touch.'),
            ('Can I place the signature anywhere on the page?',
             'Yes. You can position the signature at any location on any page.'),
            ('Is my signature data stored?',
             'No. Your signature and PDF are processed only in your browser and never stored.'),
        ],
        'h1': 'Sign PDF – Free Online Signature Tool',
        'tool_desc': 'Draw your signature on the canvas and insert it into your PDF. Position it anywhere on any page. All runs locally in your browser.',
        'breadcrumb': 'Sign PDF',
        'cross_banner_text': 'Need to protect your signed PDF with a password?',
        'cross_banner_link_text': '🔐 Protect PDF →',
        'cross_banner_href': 'pdf-password.html',
    },
    'pdf-reorder.html': {
        'title': 'Reorder PDF Pages Free Online – Drag & Drop | WooaPDF',
        'desc':  'Rearrange PDF pages by drag & drop for free. Preview thumbnails, drag to reorder, then download. No signup. Browser-based.',
        'kw':    'reorder PDF pages, rearrange PDF, PDF page reorder online, drag drop PDF pages, reorganize PDF free',
        'og_title': 'Reorder PDF Pages Free – Drag & Drop | WooaPDF',
        'og_desc':  'Drag and drop to rearrange PDF pages in any order. Preview and download instantly. Free, no server upload.',
        'app_name': 'PDF Page Reorder Tool',
        'faq': [
            ('How do I reorder pages?',
             'Page thumbnails are displayed. Drag and drop them into the order you want, then download.'),
            ('Can I preview all pages before reordering?',
             'Yes. All pages are shown as thumbnails so you can see exactly what you are moving.'),
            ('Is there a page limit?',
             'No strict limit. Large PDFs may take a moment to load thumbnails.'),
        ],
        'h1': 'Reorder PDF Pages – Free Online',
        'tool_desc': 'Upload a PDF to see page thumbnails. Drag and drop to rearrange pages in any order, then download the reordered PDF. Fully browser-based.',
        'breadcrumb': 'Reorder Pages',
        'cross_banner_text': 'Need to delete some pages after reordering?',
        'cross_banner_link_text': '🗑️ Delete PDF Pages →',
        'cross_banner_href': 'delete-pages.html',
    },
    'pdf-to-word.html': {
        'title': 'PDF to Word Converter Free Online – PDF to DOCX | WooaPDF',
        'desc':  'Convert PDF to editable Word document (DOCX) for free. Extract text and formatting. No signup. Browser-based PDF to Word converter.',
        'kw':    'PDF to Word, PDF to DOCX, convert PDF to Word free, PDF Word converter online, editable Word from PDF',
        'og_title': 'PDF to Word Converter Free Online | WooaPDF',
        'og_desc':  'Convert PDF to editable Word DOCX. Extract text and structure. Free, no signup, no server upload.',
        'app_name': 'PDF to Word Converter',
        'faq': [
            ('Will the formatting be preserved?',
             'Basic text and paragraph structure is preserved. Complex layouts may differ slightly.'),
            ('What Word format is the output?',
             'The output is a .docx file compatible with Microsoft Word and Google Docs.'),
            ('Are my files sent to a server?',
             'No. All conversion runs locally in your browser.'),
        ],
        'h1': 'PDF to Word Converter – Free Online',
        'tool_desc': 'Upload a PDF to convert it to an editable Word document. Text and basic formatting are extracted. All processing runs in your browser.',
        'breadcrumb': 'PDF → Word',
        'cross_banner_text': 'Want to convert Word back to PDF?',
        'cross_banner_link_text': '📝 Word/Excel → PDF →',
        'cross_banner_href': 'office-to-pdf.html',
    },
    'office-to-pdf.html': {
        'title': 'Word Excel to PDF Converter Free Online | WooaPDF',
        'desc':  'Convert Word (.docx) and Excel (.xlsx) files to PDF for free. No signup required. Files processed in your browser.',
        'kw':    'Word to PDF, Excel to PDF, DOCX to PDF, XLSX to PDF, convert Office to PDF free, online Word PDF converter',
        'og_title': 'Word & Excel to PDF Converter Free Online | WooaPDF',
        'og_desc':  'Convert Word and Excel files to PDF instantly. Free, no signup, browser-based conversion.',
        'app_name': 'Word/Excel to PDF Converter',
        'faq': [
            ('What file formats are supported?',
             '.docx (Word) and .xlsx (Excel) files are supported.'),
            ('Will charts and images be included?',
             'Basic charts and embedded images are preserved in the output PDF.'),
            ('Are files stored on a server?',
             'No. Everything is processed locally in your browser.'),
        ],
        'h1': 'Word / Excel to PDF – Free Online Converter',
        'tool_desc': 'Upload a Word (.docx) or Excel (.xlsx) file to convert it to PDF. All processing runs locally in your browser — no server upload.',
        'breadcrumb': 'Word/Excel → PDF',
        'cross_banner_text': 'Need to convert PDF back to Word?',
        'cross_banner_link_text': '🔤 PDF → Word →',
        'cross_banner_href': 'pdf-to-word.html',
    },
    'pdf-text-extract.html': {
        'title': 'Extract Text from PDF Free Online – PDF Text Extractor | WooaPDF',
        'desc':  'Extract text from PDF files for free, even from non-copyable PDFs. Copy or download extracted text. No signup. 100% browser-based.',
        'kw':    'extract text from PDF, PDF text extractor, copy text from PDF, PDF to text, OCR PDF text free online',
        'og_title': 'Extract Text from PDF Free Online | WooaPDF',
        'og_desc':  'Extract all text from a PDF, including non-copyable PDFs. Free, no signup, no server upload.',
        'app_name': 'PDF Text Extractor',
        'faq': [
            ('Can I extract text from scanned PDFs?',
             'Basic text extraction works for text-based PDFs. Scanned image PDFs may require OCR (coming soon).'),
            ('What can I do with the extracted text?',
             'Copy it to clipboard, download as a .txt file, or use it however you need.'),
            ('Are files sent to a server?',
             'No. Text extraction runs entirely in your browser.'),
        ],
        'h1': 'Extract Text from PDF – Free Online',
        'tool_desc': 'Upload a PDF to extract all text content. Works on PDFs where copy-paste is disabled. Copy or download the result. All browser-based.',
        'breadcrumb': 'Extract PDF Text',
        'cross_banner_text': 'Need to convert PDF to an editable Word document?',
        'cross_banner_link_text': '🔤 PDF → Word →',
        'cross_banner_href': 'pdf-to-word.html',
    },
    'pdf-viewer.html': {
        'title': 'Free PDF Viewer Download – Adobe Reader & Alternatives | WooaPDF',
        'desc':  'Download free PDF viewers including Adobe Acrobat Reader, Foxit Reader, Sumatra PDF and more. Find the best free PDF reader for your needs.',
        'kw':    'free PDF viewer, PDF reader download, Adobe Reader, Foxit Reader, Sumatra PDF, best free PDF reader',
        'og_title': 'Free PDF Viewer Downloads – Best PDF Readers | WooaPDF',
        'og_desc':  'Find and download free PDF viewers: Adobe Reader, Foxit, Sumatra PDF and more. Free PDF reader guide.',
        'app_name': 'PDF Viewer Guide',
        'faq': [
            ('Which PDF viewer is best?',
             'Adobe Acrobat Reader is the most widely used. Sumatra PDF is lightweight and fast. Foxit Reader is feature-rich.'),
            ('Are these PDF viewers free?',
             'Yes. All PDF viewers listed here are free for personal use.'),
            ('Do I need a PDF viewer if I use WooaPDF?',
             'WooaPDF tools work in any browser without a separate viewer. But a desktop viewer is useful for daily PDF reading.'),
        ],
        'h1': 'Free PDF Viewer Downloads',
        'tool_desc': 'Find and download the best free PDF viewers. Adobe Acrobat Reader, Foxit Reader, Sumatra PDF and more — all free for personal use.',
        'breadcrumb': 'PDF Viewer',
        'cross_banner_text': 'Need to edit or convert your PDF files?',
        'cross_banner_link_text': '🛠️ All PDF Tools →',
        'cross_banner_href': 'index.html',
    },
}

# ── 2. 공통 문자열 치환 ──────────────────────────────────────────────────────
COMMON = [
    # lang
    ('<html lang="ko">', '<html lang="en">'),
    # locale
    ('ko_KR', 'en_US'),
    # inLanguage
    ('"inLanguage": "ko"', '"inLanguage": "en"'),
    # priceCurrency
    ('"priceCurrency": "KRW"', '"priceCurrency": "USD"'),
    # paths: CSS, JS, manifest
    ('href="css/style.css"', 'href="../css/style.css"'),
    ('href="/manifest.json"', 'href="../manifest.json"'),
    ('src="js/', 'src="../js/'),
    ('href="js/', 'href="../js/'),
    # header nav
    ('>PDF→이미지<', '>PDF→Image<'),
    ('>이미지→PDF<', '>Image→PDF<'),
    ('>PDF 병합<', '>Merge PDF<'),
    ('>PDF 분할<', '>Split PDF<'),
    ('>PDF 압축<', '>Compress PDF<'),
    ('>전체 도구 ›<', '>All Tools ›<'),
    # breadcrumb home
    ('>🏠 홈<', '>🏠 Home<'),
    # drop zone
    ('PDF 파일을 여기에 끌어다 놓으세요', 'Drop your PDF file here'),
    ('또는 버튼을 클릭해서 파일을 선택하세요', 'or click the button to select a file'),
    ('PDF 파일 선택', 'Select PDF File'),
    ('파일 선택', 'Select File'),
    # file panel
    ('>선택된 파일<', '>Selected Files<'),
    # options
    ('>변환 옵션<', '>Options<'),
    ('>병합 옵션<', '>Options<'),
    ('>분할 옵션<', '>Options<'),
    ('>압축 옵션<', '>Options<'),
    ('>편집 옵션<', '>Options<'),
    ('>설정<', '>Settings<'),
    # common option labels
    ('이미지 형식', 'Image Format'),
    ('이미지 품질', 'Image Quality'),
    ('고화질 (2x 해상도)', 'High Quality (2x)'),
    ('중간 (1.5x 해상도)', 'Medium (1.5x)'),
    ('낮음 (1x 해상도)', 'Low (1x)'),
    ('변환 범위', 'Page Range'),
    ('전체 페이지', 'All Pages'),
    ('특정 페이지', 'Custom Range'),
    ('페이지 번호', 'Page Numbers'),
    ('예: 1,3,5-8 (쉼표 또는 하이픈으로 구분)', 'e.g. 1,3,5-8 (comma or hyphen)'),
    ('예: 1-3, 5, 7-10', 'e.g. 1-3, 5, 7-10'),
    # buttons
    ('>🔄 변환 시작<', '>🔄 Convert<'),
    ('>🔗 병합 시작<', '>🔗 Merge PDF<'),
    ('>✂️ 분할 시작<', '>✂️ Split PDF<'),
    ('>🗜️ 압축 시작<', '>🗜️ Compress PDF<'),
    ('>🔄 회전 적용<', '>🔄 Apply Rotation<'),
    ('>🗑️ 페이지 삭제<', '>🗑️ Delete Pages<'),
    ('>💧 워터마크 추가<', '>💧 Add Watermark<'),
    ('>🔢 페이지 번호 추가<', '>🔢 Add Page Numbers<'),
    ('>🔓 잠금 해제<', '>🔓 Unlock PDF<'),
    ('>🔐 암호 설정<', '>🔐 Protect PDF<'),
    ('>✍️ 서명 삽입<', '>✍️ Insert Signature<'),
    ('>🔀 페이지 재정렬<', '>🔀 Reorder Pages<'),
    ('>📝 Word 변환<', '>📝 Convert to Word<'),
    ('>📄 PDF 변환<', '>📄 Convert to PDF<'),
    ('>📋 텍스트 추출<', '>📋 Extract Text<'),
    # progress
    ('>변환 중...<', '>Processing...<'),
    ('>처리 중...<', '>Processing...<'),
    ('>압축 중...<', '>Compressing...<'),
    # result
    ('>변환 완료!<', '>Done!<'),
    ('>압축 완료!<', '>Compressed!<'),
    ('>병합 완료!<', '>Merged!<'),
    ('>분할 완료!<', '>Split!<'),
    ('>처리 완료!<', '>Done!<'),
    # download
    ('⬇️ 전체 다운로드 (ZIP)', '⬇️ Download All (ZIP)'),
    ('⬇️ 다운로드', '⬇️ Download'),
    ('>⬇️ PDF 다운로드<', '>⬇️ Download PDF<'),
    ('>⬇️ 텍스트 복사<', '>📋 Copy Text<'),
    ('>⬇️ 텍스트 다운로드<', '>⬇️ Download Text<'),
    # features section
    ('개인정보 보호', 'Privacy Protected'),
    ('파일이 서버로 전송되지 않습니다', 'Files never sent to server'),
    ('>빠른 처리<', '>Fast Processing<'),
    ('로컬 처리로 속도 빠름', 'Fast local processing'),
    ('>완전 무료<', '>Completely Free<'),
    ('회원가입 없이 무제한 사용', 'Unlimited, no signup'),
    # footer
    ('모든 권리 보유.', 'All rights reserved.'),
    ('>개인정보처리방침<', '>Privacy Policy<'),
    ('href="privacy.html"', 'href="../privacy.html"'),
    ('href="about.html"', 'href="../about.html"'),
    ('>소개<', '>About<'),
    # FAQ section heading
    ('>자주 묻는 질문<', '>Frequently Asked Questions<'),
    # ── 도구 설명 단락 (h1 아래 sub-text) ──
    ('PDF 파일을 업로드하면 각 페이지를 이미지로 변환해 드립니다. 파일은 브라우저에서만 처리되어 서버에 저장되지 않습니다.',
     'Upload a PDF and convert each page to an image. Files are processed in your browser and never stored on a server.'),
    ('여러 개의 PDF 파일을 하나의 PDF로 합칩니다. 드래그로 순서를 조정하세요.',
     'Combine multiple PDF files into one. Drag to reorder.'),
    ('PDF 파일을 pages별로 나누거나 원하는 범위로 분할합니다.',
     'Split a PDF by page or custom range.'),
    ('PDF pages의 방향을 90°, 180°, 270° 회전합니다.',
     'Rotate PDF pages 90°, 180°, or 270°.'),
    ('삭제할 pages를 클릭해서 선택한 후 "삭제하기" 버튼을 누르세요.',
     'Click pages to select them, then press the Delete button.'),
    ('PDF pages에 텍스트 워터마크를 삽입합니다.',
     'Insert a text watermark into PDF pages.'),
    ('PDF의 각 pages에 번호를 자동으로 삽입합니다.',
     'Automatically insert page numbers into each PDF page.'),
    ('워드(.docx) 또는 엑셀(.xlsx) 파일을 미리보기 후 PDF로 저장합니다.',
     'Preview Word (.docx) or Excel (.xlsx) files and save as PDF.'),
    ('PDF 파일에서 텍스트를 추출하여 복사하거나 TXT로 저장합니다.',
     'Extract text from a PDF and copy or save as TXT.'),
    ('PDF 파일에서 텍스트를 추출하여 편집 가능한 Word 문서(.doc)로 변환합니다.',
     'Extract text from a PDF and convert to an editable Word document (.doc).'),

    # ── 드롭존 sub-text ──
    ('여러 파일을 동시에 선택할 수 있습니다', 'Multiple files supported'),
    ('분할할 PDF 파일 1개를 선택하세요', 'Select 1 PDF file to split'),
    ('회전할 PDF 파일을 선택하세요', 'Select a PDF file to rotate'),
    ('pages를 선택해서 삭제할 PDF를 업로드하세요', 'Upload a PDF to select and delete pages'),
    ('워터마크를 추가할 PDF를 업로드하세요', 'Upload a PDF to add a watermark'),
    ('Page Numbers를 추가할 PDF를 업로드하세요', 'Upload a PDF to add page numbers'),
    ('텍스트를 추출할 PDF를 업로드하세요', 'Upload a PDF to extract text'),
    ('.docx 파일만 지원됩니다', 'Only .docx files supported'),
    ('.xlsx 파일만 지원됩니다', 'Only .xlsx files supported'),
    ('서명을 삽입할 PDF를 업로드하세요', 'Upload a PDF to insert a signature'),
    ('순서를 변경할 PDF를 업로드하세요', 'Upload a PDF to reorder pages'),
    ('잠금 해제할 PDF를 업로드하세요', 'Upload a PDF to unlock'),
    ('암호를 설정할 PDF를 업로드하세요', 'Upload a PDF to set a password'),
    ('압축할 PDF를 업로드하세요', 'Upload a PDF to compress'),

    # ── 크로스링크 배너 ──
    ('PDF에서 텍스트만 필요하신가요?', 'Just need text from a PDF?'),
    ('📄 PDF 텍스트 추출 바로가기 →', '📄 Extract PDF Text →'),
    ('PDF를 다시 Word로 변환하고 싶다면?', 'Want to convert PDF back to Word?'),
    ('추출한 텍스트를 Word로 편집하고 싶다면?', 'Want to edit the extracted text in Word?'),
    ('📄 PDF → Word 변환 →', '📄 PDF → Word →'),
    ('스캔된 이미지 PDF에서 텍스트를 추출하려면 OCR이 필요합니다.', 'To extract text from scanned image PDFs, OCR is required.'),
    ('WooaImage OCR 바로가기 →', 'WooaImage OCR →'),

    # ── 참고/경고 메시지 ──
    ('참고: PowerPoint(PPTX)는 현재 지원되지 않습니다.', 'Note: PowerPoint (PPTX) is not currently supported.'),
    ('참고:', 'Note:'),

    # ── option-label spans ──
    ('<span class="option-label">색상</span>', '<span class="option-label">Color</span>'),
    ('<span class="option-label">펜 굵기</span>', '<span class="option-label">Pen Width</span>'),
    ('<span class="option-label">위치</span>', '<span class="option-label">Position</span>'),
    ('<span class="option-label">글자 크기</span>', '<span class="option-label">Font Size</span>'),
    ('<span class="option-label">표시 형식</span>', '<span class="option-label">Format</span>'),
    ('<span class="option-label">시작 번호</span>', '<span class="option-label">Start Number</span>'),
    ('<span class="option-label">여백</span>', '<span class="option-label">Margin</span>'),
    ('<span class="option-label">적용 pages</span>', '<span class="option-label">Apply to Pages</span>'),
    ('<span class="option-label">적용 범위</span>', '<span class="option-label">Apply Range</span>'),
    ('<span class="option-label">워터마크 텍스트</span>', '<span class="option-label">Watermark Text</span>'),
    ('<span class="option-label">투명도</span>', '<span class="option-label">Opacity</span>'),
    ('<span class="option-label">분할 방식</span>', '<span class="option-label">Split Method</span>'),
    ('<span class="option-label">범위 입력</span>', '<span class="option-label">Enter Range</span>'),
    ('<span class="option-label">비밀번호</span>', '<span class="option-label">Password</span>'),
    ('<span class="option-label">비밀번호 확인</span>', '<span class="option-label">Confirm Password</span>'),
    ('<span class="option-label">열기 비밀번호</span>', '<span class="option-label">Open Password</span>'),
    ('<span class="option-label">소유자 비밀번호</span>', '<span class="option-label">Owner Password</span>'),
    ('<span class="option-label">권한 설정</span>', '<span class="option-label">Permissions</span>'),
    ('<span class="option-label">pages 선택</span>', '<span class="option-label">Select Pages</span>'),
    ('<span class="option-label">pages 크기</span>', '<span class="option-label">Page Size</span>'),
    ('<span class="option-label">회전 각도</span>', '<span class="option-label">Rotation Angle</span>'),
    ('<label>pages 선택:</label>', '<label>Select Pages:</label>'),
    ('<label>색상</label>', '<label>Color</label>'),
    ('<label>펜 굵기</label>', '<label>Pen Width</label>'),

    # ── options-title divs ──
    ('<div class="options-title">변환 설정</div>', '<div class="options-title">Convert Settings</div>'),
    ('<div class="options-title">분할 방식</div>', '<div class="options-title">Split Method</div>'),
    ('<div class="options-title">회전 옵션</div>', '<div class="options-title">Rotation Options</div>'),
    ('<div class="options-title">워터마크 설정</div>', '<div class="options-title">Watermark Settings</div>'),
    ('<div class="options-title">Page Numbers 설정</div>', '<div class="options-title">Page Number Settings</div>'),
    ('<div class="options-title">잠금 해제 설정</div>', '<div class="options-title">Unlock Settings</div>'),
    ('<div class="options-title">암호 설정</div>', '<div class="options-title">Password Settings</div>'),
    ('<div class="options-title">압축 품질 선택</div>', '<div class="options-title">Compression Quality</div>'),
    ('<div class="options-title">PDF 옵션</div>', '<div class="options-title">PDF Options</div>'),

    # ── button texts ──
    ('>🔗 PDF 병합하기<', '>🔗 Merge PDF<'),
    ('>✂️ 분할하기<', '>✂️ Split PDF<'),
    ('>✍️ 서명 삽입 및 다운로드<', '>✍️ Insert Signature & Download<'),
    ('>🔀 재정렬 적용 및 다운로드<', '>🔀 Apply Reorder & Download<'),
    ('>🔐 암호 설정 및 다운로드<', '>🔐 Protect & Download<'),
    ('>🔢 Page Numbers 추가<', '>🔢 Add Page Numbers<'),
    ('>📄 PDF로 변환<', '>📄 Convert to PDF<'),
    ('>🔤 Word 파일로 변환<', '>🔤 Convert to Word<'),
    ('>🗑️ 선택한 pages 삭제<', '>🗑️ Delete Selected Pages<'),
    ('>📋 전체 복사<', '>📋 Copy All<'),
    ('>⬇️ TXT 다운로드<', '>⬇️ Download TXT<'),
    ('>⬇️ ZIP으로 다운로드<', '>⬇️ Download ZIP<'),
    ('>⬇️ 병합된 PDF 다운로드<', '>⬇️ Download Merged PDF<'),
    ('>⬇️ 압축된 PDF 다운로드<', '>⬇️ Download Compressed PDF<'),
    ('>⬇️ Word 파일 다운로드 (.doc)<', '>⬇️ Download Word File (.doc)<'),
    ('>⬇️ 서명된 PDF 다운로드<', '>⬇️ Download Signed PDF<'),
    ('>⬇️ 잠금 해제된 PDF 다운로드<', '>⬇️ Download Unlocked PDF<'),
    ('>⬇️ 암호 보호된 PDF 다운로드<', '>⬇️ Download Protected PDF<'),
    ('>🖨️ PDF로 저장 (인쇄)<', '>🖨️ Save as PDF (Print)<'),
    ('>+ PDF 추가<', '>+ Add PDF<'),
    ('>지우기<', '>Clear<'),
    ('<span class="btn-dl btn-dl-secondary">✅ 이미 설치됨</span>', '<span class="btn-dl btn-dl-secondary">✅ Already Installed</span>'),

    # ── download links ──
    ('>⬇️ 무료 다운로드<', '>⬇️ Free Download<'),
    ('href="https://get.adobe.com/kr/reader/"', 'href="https://get.adobe.com/reader/"'),
    ('href="https://www.foxit.com/ko/pdf-reader/"', 'href="https://www.foxit.com/pdf-reader/"'),

    # ── result titles ──
    ('<div class="result-title">완료!</div>', '<div class="result-title">Done!</div>'),
    ('<div class="result-title">서명 삽입 완료!</div>', '<div class="result-title">Signature Added!</div>'),
    ('<div class="result-title">워터마크 추가 완료!</div>', '<div class="result-title">Watermark Added!</div>'),
    ('<div class="result-title">재정렬 완료!</div>', '<div class="result-title">Reordered!</div>'),
    ('<div class="result-title">잠금 해제 완료!</div>', '<div class="result-title">Unlocked!</div>'),
    ('<div class="result-title">회전 완료!</div>', '<div class="result-title">Rotated!</div>'),
    ('<div class="result-title">Word 변환 완료!</div>', '<div class="result-title">Converted to Word!</div>'),
    ('<div class="result-title">Page Numbers 추가 완료!</div>', '<div class="result-title">Page Numbers Added!</div>'),
    ('<div class="result-subtitle" id="resultSubtitle">비밀번호 보호가 제거된 PDF가 생성되었습니다</div>',
     '<div class="result-subtitle" id="resultSubtitle">Password protection has been removed.</div>'),

    # ── progress messages ──
    ("updateProgressUI(0, '준비 중...');", "updateProgressUI(0, 'Preparing...');"),
    ("updateProgressUI(100, '완료!');", "updateProgressUI(100, 'Done!');"),
    ("updateProgressUI(20, 'PDF 로드 중...');", "updateProgressUI(20, 'Loading PDF...');"),
    ("updateProgressUI(30, 'PDF 로드 중...');", "updateProgressUI(30, 'Loading PDF...');"),
    ("updateProgressUI(40, 'PDF 로드 중...');", "updateProgressUI(40, 'Loading PDF...');"),
    ("updateProgressUI(30, 'PDF 불러오는 중...');", "updateProgressUI(30, 'Loading PDF...');"),
    ("updateProgressUI(30, 'Page Numbers 삽입 중...');", "updateProgressUI(30, 'Inserting page numbers...');"),
    ("updateProgressUI(30, 'pages 제거 중...');", "updateProgressUI(30, 'Removing pages...');"),
    ("updateProgressUI(30, 'pages 회전 중...');", "updateProgressUI(30, 'Rotating pages...');"),
    ("updateProgressUI(40, '워터마크 삽입 중...');", "updateProgressUI(40, 'Inserting watermark...');"),
    ("updateProgressUI(50, 'pages 추출 중...');", "updateProgressUI(50, 'Extracting pages...');"),
    ("updateProgressUI(60, '서명 삽입 중...');", "updateProgressUI(60, 'Inserting signature...');"),
    ("updateProgressUI(60, '암호 설정 중...');", "updateProgressUI(60, 'Setting password...');"),
    ("updateProgressUI(75, '잠금 해제 후 저장 중...');", "updateProgressUI(75, 'Saving unlocked PDF...');"),
    ("updateProgressUI(80, 'PDF 저장 중...');", "updateProgressUI(80, 'Saving PDF...');"),
    ("updateProgressUI(85, 'PDF 저장 중...');", "updateProgressUI(85, 'Saving PDF...');"),
    ("updateProgressUI(90, 'PDF 저장 중...');", "updateProgressUI(90, 'Saving PDF...');"),
    ("updateProgressUI(95, 'PDF 생성 중...');", "updateProgressUI(95, 'Generating PDF...');"),
    ("updateProgressUI(95, 'Word 문서 생성 중...');", "updateProgressUI(95, 'Generating Word document...');"),
    ("'준비 중...'", "'Preparing...'"),
    ('<span id="progressText">병합 중...</span>', '<span id="progressText">Merging...</span>'),
    ('<span id="progressText">분할 중...</span>', '<span id="progressText">Splitting...</span>'),
    ('<span id="loadingText">썸네일 렌더링 중...</span>', '<span id="loadingText">Rendering thumbnails...</span>'),
    ('<div>pages 미리보기를 생성하고 있습니다...</div>', '<div>Generating page previews...</div>'),

    # ── result JS messages ──
    ("`${currentPage}pages에 서명이 삽입되었습니다`", "`Signature inserted on page ${currentPage}`"),
    ("`${pageOrder.length}pages 재정렬 완료 (${newOrderStr})`", "`${pageOrder.length} pages reordered (${newOrderStr})`"),
    ("`${pagesToRotate.length}개 pages가 ${angle}° 회전되었습니다`", "`${pagesToRotate.length} pages rotated ${angle}°`"),
    ("`${selectedPages.size}개 pages가 삭제되어 ${keepIndices.length}개 pages만 남았습니다`",
     "`${selectedPages.size} pages deleted, ${keepIndices.length} pages remaining`"),
    ("`${splitResults.length}개의 PDF 파일로 분할되었습니다`", "`Split into ${splitResults.length} PDF files`"),
    ("`${targetPages.length}개 pages에 워터마크가 추가되었습니다`", "`Watermark added to ${targetPages.length} pages`"),
    ("`${targetPages.length}개 pages의 텍스트가 Word 문서로 변환되었습니다`", "`Text from ${targetPages.length} pages converted to Word`"),
    ("`${totalPgs}개 pages에 번호가 추가되었습니다 (${startNum}번부터 시작)`",
     "`Page numbers added to ${totalPgs} pages (starting from ${startNum})`"),
    ("`1개의 PDF 파일이 생성되었습니다`", "`1 PDF file generated`"),
    ("`암호가 설정되었습니다. 허용: ${permDesc.join(', ') || '없음'}`",
     "`Password set. Allowed: ${permDesc.join(', ') || 'none'}`"),
    ("const text = total === 0 ? '완료' : `${done}/${total} pages 변환 중 (pages ${current})`;",
     "const text = total === 0 ? 'Done' : `Converting ${done}/${total} pages (page ${current})`;"),

    # ── progress update templates ──
    ("`pages ${i + 1}/${pageOrder.length} 복사 중...`", "`Copying page ${i + 1}/${pageOrder.length}...`"),
    ("`pages ${i}/${numPages} 추출 중...`", "`Extracting page ${i}/${numPages}...`"),
    ("`pages ${pageNum}/${numPages} 텍스트 추출 중...`", "`Extracting text from page ${pageNum}/${numPages}...`"),

    # ── info/selection spans ──
    ('<span class="selection-info" id="selectionInfo">선택된 pages 없음</span>',
     '<span class="selection-info" id="selectionInfo">No pages selected</span>'),
    ("info.textContent = `${count}개 선택됨 (전체 선택 — 최소 1pages는 남겨야 합니다)`;",
     "info.textContent = `${count} selected (all — at least 1 page must remain)`;"),
    ('<span style="font-size:0.85rem; color:#6B7280;">번부터 시작</span>',
     '<span style="font-size:0.85rem; color:#6B7280;">starting from</span>'),
    ('<div style="font-size:0.78rem; color:#6B7280; margin-top:6px;">선택한 pages만 하나의 PDF로 추출됩니다</div>',
     '<div style="font-size:0.78rem; color:#6B7280; margin-top:6px;">Selected pages will be extracted into one PDF</div>'),
    ('<div style="font-size:0.78rem; color:#6B7280; margin-top:6px;">쉼표로 구분하면 각 범위별로 별도 PDF가 생성됩니다</div>',
     '<div style="font-size:0.78rem; color:#6B7280; margin-top:6px;">Comma-separated ranges create separate PDFs each</div>'),
    ('<div style="font-size:0.78rem; color:var(--text-light); margin-top:4px;">비워두면 열기 비밀번호와 동일하게 설정됩니다</div>',
     '<div style="font-size:0.78rem; color:var(--text-light); margin-top:4px;">Leave blank to use the same as open password</div>'),
    ('<div style="font-size:0.85rem; color:#6B7280; margin-top:4px;">삭제할 pages를 클릭해서 선택하세요 (다시 클릭하면 취소)</div>',
     '<div style="font-size:0.85rem; color:#6B7280; margin-top:4px;">Click pages to select for deletion (click again to deselect)</div>'),

    # ── sidebar tool list links ──
    ('>🔗 PDF 병합<', '>🔗 Merge PDF<'),
    ('>🖼️ PDF → JPG 변환<', '>🖼️ PDF → JPG<'),
    ('>📸 PDF → PNG 변환<', '>📸 PDF → PNG<'),
    ('>🔄 PDF 회전<', '>🔄 Rotate PDF<'),
    ('>✂️ PDF 분할<', '>✂️ Split PDF<'),
    ('>🗑️ pages 삭제<', '>🗑️ Delete Pages<'),
    ('>💧 워터마크 추가<', '>💧 Add Watermark<'),
    ('>🔢 Page Numbers 추가<', '>🔢 Add Page Numbers<'),
    ('>🔓 PDF 잠금 해제<', '>🔓 Unlock PDF<'),
    ('>🔐 PDF 암호 설정<', '>🔐 Protect PDF<'),
    ('>✍️ PDF 서명 추가<', '>✍️ Sign PDF<'),
    ('>🔀 pages 재정렬<', '>🔀 Reorder Pages<'),
    ('>📋 PDF 텍스트 추출<', '>📋 Extract PDF Text<'),
    ('>📄 PDF → Word 변환<', '>📄 PDF → Word<'),
    ('>📊 Word/Excel → PDF 변환<', '>📊 Word/Excel → PDF<'),

    # ── cross-link banners ──
    ('<span>PDF → Word 변환</span>', '<span>PDF → Word</span>'),
    ('<span>PDF 서명 추가</span>', '<span>Sign PDF</span>'),
    ('<span>PDF 암호 설정</span>', '<span>Protect PDF</span>'),
    ('<span>PDF 잠금 해제</span>', '<span>Unlock PDF</span>'),
    ('<span>PDF 잠금을 해제하고 싶다면?</span>', '<span>Want to unlock a PDF?</span>'),
    ('<span>PDF 텍스트 추출</span>', '<span>Extract PDF Text</span>'),
    ('<span>PDF 회전</span>', '<span>Rotate PDF</span>'),
    ('<span>Page Numbers 추가</span>', '<span>Add Page Numbers</span>'),
    ('<span>Word/Excel → PDF 변환</span>', '<span>Word/Excel → PDF</span>'),
    ('<span>pages 삭제</span>', '<span>Delete Pages</span>'),
    ('<span>pages 재정렬</span>', '<span>Reorder Pages</span>'),
    ('<span>워터마크 추가</span>', '<span>Add Watermark</span>'),
    ('<span>이미지 → PDF 변환</span>', '<span>Image → PDF</span>'),
    ('<a href="pdf-to-jpg.html">📄 PDF 텍스트 추출 바로가기 →</a>',
     '<a href="pdf-text-extract.html">📋 Extract PDF Text →</a>'),
    ('<a href="pdf-text-extract.html">📋 PDF 텍스트 추출 바로가기 →</a>',
     '<a href="pdf-text-extract.html">📋 Extract PDF Text →</a>'),
    ('<a href="pdf-to-word.html">🔤 PDF → Word 변환 →</a>', '<a href="pdf-to-word.html">🔤 PDF → Word →</a>'),
    ('<a href="unlock-pdf.html">🔓 PDF 잠금 해제 →</a>', '<a href="unlock-pdf.html">🔓 Unlock PDF →</a>'),
    ('<a href="index.html" style="color:#FF4444; font-weight:600;">WooaPDF 도구 모음</a>을 무료로 이용하세요.',
     'Use <a href="index.html" style="color:#FF4444; font-weight:600;">WooaPDF tools</a> for free.'),
    ('<strong style="color:#374151;">💡 PDF를 편집·변환해야 한다면?</strong>',
     '<strong style="color:#374151;">💡 Need to edit or convert your PDF?</strong>'),

    # ── breadcrumb spans ──
    ('<span>PDF → Word 변환</span>', '<span>PDF → Word</span>'),
    ('<span>이미지 → PDF 변환</span>', '<span>Image → PDF</span>'),

    # ── signature tool ──
    ('<div class="step-title"><span class="step-number">1</span> 서명 그리기</div>',
     '<div class="step-title"><span class="step-number">1</span> Draw Signature</div>'),
    ('<div class="step-title"><span class="step-number">2</span> 서명 위치 선택</div>',
     '<div class="step-title"><span class="step-number">2</span> Place Signature</div>'),
    ('<p class="position-hint">PDF 미리보기를 클릭하여 서명 위치를 지정하세요.</p>',
     '<p class="position-hint">Click on the PDF preview to place your signature.</p>'),
    ('alt="서명"', 'alt="Signature"'),

    # ── compression quality cards ──
    ('<div class="quality-card-title">강력 압축</div>', '<div class="quality-card-title">Max Compress</div>'),
    ('<div class="quality-card-title">균형 (권장)</div>', '<div class="quality-card-title">Balanced (Recommended)</div>'),
    ('<div class="quality-card-title">고화질 압축</div>', '<div class="quality-card-title">High Quality</div>'),
    ('<div class="quality-card-desc">용량 최소화<br>화질 다소 저하</div>',
     '<div class="quality-card-desc">Smallest size<br>Lower quality</div>'),
    ('<div class="quality-card-desc">용량과 화질<br>균형 유지</div>',
     '<div class="quality-card-desc">Balanced size<br>& quality</div>'),
    ('<div class="quality-card-desc">화질 우선<br>압축률 낮음</div>',
     '<div class="quality-card-desc">Best quality<br>Less compression</div>'),

    # ── size labels ──
    ('<div class="size-label">원본</div>', '<div class="size-label">Original</div>'),
    ('<div class="size-label">압축 후</div>', '<div class="size-label">Compressed</div>'),
    ('<div class="size-label">감소율</div>', '<div class="size-label">Reduction</div>'),

    # ── PDF list title ──
    ('PDF 파일 목록 <span style="font-weight:400;font-size:0.8rem;">(드래그로 순서 변경)</span>',
     'PDF File List <span style="font-weight:400;font-size:0.8rem;">(drag to reorder)</span>'),

    # ── tab button ──
    ('<button class="text-tab-btn active" id="tabAll">전체</button>',
     '<button class="text-tab-btn active" id="tabAll">All</button>'),

    # ── PDF viewer page ──
    ('<h1 style="font-size:1.8rem;">PDF 뷰어 무료 다운로드</h1>',
     '<h1 style="font-size:1.8rem;">Free PDF Viewer Downloads</h1>'),
    ('<p>PDF 파일을 열 수 없을 때 필요한 무료 뷰어 모음</p>',
     '<p>Free PDF viewers for when you can\'t open a PDF file</p>'),
    ('<div class="viewer-category">🍎 아이폰 / 아이패드 (iOS)</div>',
     '<div class="viewer-category">🍎 iPhone / iPad (iOS)</div>'),
    ('<div class="viewer-category">📱 안드로이드 (Android)</div>',
     '<div class="viewer-category">📱 Android</div>'),
    ('<div class="viewer-card-maker">Apple (기본 내장)</div>', '<div class="viewer-card-maker">Apple (Built-in)</div>'),
    ('<div class="viewer-card-name">기본 파일 앱</div>', '<div class="viewer-card-name">Files App</div>'),
    ('<div class="viewer-card-desc">세계에서 가장 많이 사용되는 PDF 뷰어. 주석, 서명 등 기본 편집 기능 포함. 용량이 다소 큰 편.</div>',
     '<div class="viewer-card-desc">The world\'s most used PDF viewer. Includes annotations and basic editing. Larger install size.</div>'),
    ('<div class="viewer-card-desc">Adobe Reader보다 가볍고 빠른 PDF 뷰어. 주석, 폼 작성, 서명 기능 무료 제공.</div>',
     '<div class="viewer-card-desc">Lighter and faster than Adobe Reader. Free annotations, forms, and signature features.</div>'),
    ('<div class="viewer-card-desc">설치 없이 바로 실행 가능한 초경량 PDF 뷰어(포터블). 광고·업데이트 없이 빠르게 실행.</div>',
     '<div class="viewer-card-desc">Ultra-lightweight portable PDF viewer. No install needed. No ads or updates.</div>'),
    ('<div class="viewer-card-desc">iOS 최적화 PDF 뷰어. Apple Pencil로 주석 작성, iCloud 연동 지원.</div>',
     '<div class="viewer-card-desc">iOS-optimized PDF viewer. Apple Pencil annotations and iCloud sync supported.</div>'),
    ('<div class="viewer-card-desc">iOS/iPadOS에는 PDF 뷰어가 기본 내장되어 있습니다. 별도 앱 없이 파일 앱 또는 Safari에서 바로 열 수 있습니다.</div>',
     '<div class="viewer-card-desc">iOS/iPadOS has a built-in PDF viewer. Open PDFs directly in the Files app or Safari without any extra app.</div>'),
    ('<div class="viewer-card-desc">모바일 최적화된 PDF 뷰어. 주석, 서명, 폼 작성 등 기본 기능 무료 제공.</div>',
     '<div class="viewer-card-desc">Mobile-optimized PDF viewer. Free annotations, signatures, and form filling.</div>'),
    ('<div class="viewer-card-desc">가볍고 빠른 안드로이드용 PDF 뷰어. 클라우드 연동 및 야간 모드 지원.</div>',
     '<div class="viewer-card-desc">Lightweight Android PDF viewer. Cloud sync and night mode supported.</div>'),
    ('<span class="viewer-tag">업계 표준</span>', '<span class="viewer-tag">Industry Standard</span>'),
    ('<span class="viewer-tag">가볍고 빠름</span>', '<span class="viewer-tag">Lightweight</span>'),
    ('<span class="viewer-tag">초경량</span>', '<span class="viewer-tag">Ultra-light</span>'),
    ('<span class="viewer-tag">설치 불필요</span>', '<span class="viewer-tag">No Install</span>'),
    ('<span class="viewer-tag">무료</span>', '<span class="viewer-tag">Free</span>'),
    ('💡 PDF 파일이 안 열린다면 아래 뷰어 중 하나를 설치하세요. 모두 <strong>무료</strong>로 사용할 수 있습니다.',
     '💡 Can\'t open a PDF? Install one of the viewers below. All are <strong>free</strong>.'),
    ('PDF 뷰어는 PDF 파일을 읽기 위한 프로그램입니다. Windows, Mac, 스마트폰 등 기기별로 추천 뷰어를 안내합니다.',
     'A PDF viewer is a program for reading PDF files. We recommend the best viewer for each platform.'),
    ('PDF 뷰어는 보기 전용입니다. PDF를 이미지로 변환하거나, 합치거나, 압축하려면',
     'PDF viewers are read-only. To convert, merge, or compress PDFs,'),
    ('PDF를 편집하거나 변환하려면 상단의 <a href="index.html" style="color:#FF4444;">WooaPDF 도구</a>를 이용하세요.',
     'To edit or convert PDFs, use the <a href="index.html" style="color:#FF4444;">WooaPDF tools</a> above.'),
    ('🔐 PDF 잠금 해제 안내:', '🔐 PDF Unlock Guide:'),

    # ── unlock hints ──
    ('<li>비밀번호가 없어도 일부 PDF는 자동으로 해제됩니다</li>',
     '<li>Some PDFs can be unlocked automatically without a password</li>'),
    ('<li>비밀번호를 알고 있다면 아래에 입력하세요</li>',
     '<li>If you know the password, enter it below</li>'),
    ('<li>강력한 암호화 PDF(AES-256)는 올바른 비밀번호가 필요합니다</li>',
     '<li>Strongly encrypted PDFs (AES-256) require the correct password</li>'),
    ('<div class="result-subtitle" id="resultSubtitle">비밀번호 보호가 제거된 PDF가 생성되었습니다</div>',
     '<div class="result-subtitle" id="resultSubtitle">Password protection has been removed.</div>'),

    # ── status badges ──
    ('statusHtml = `<span class="status-badge status-locked">🔒 잠금된 PDF (비밀번호 필요할 수 있음)</span>`;',
     'statusHtml = `<span class="status-badge status-locked">🔒 Locked PDF (password may be required)</span>`;'),
    ('statusHtml = `<span class="status-badge status-unknown">❓ 상태 확인 불가</span>`;',
     'statusHtml = `<span class="status-badge status-unknown">❓ Status unknown</span>`;'),
    ('statusHtml = `<span class="status-badge status-unlocked">🔓 잠금 없음 (비밀번호 불필요)</span>`;',
     'statusHtml = `<span class="status-badge status-unlocked">🔓 No lock (no password needed)</span>`;'),

    # ── pen options ──
    ('<option value="2">가는 (2px)</option>', '<option value="2">Thin (2px)</option>'),
    ('<option value="3" selected>보통 (3px)</option>', '<option value="3" selected>Normal (3px)</option>'),
    ('<option value="5">굵은 (5px)</option>', '<option value="5">Thick (5px)</option>'),

    # ── office-to-pdf note ──
    ('<strong>안내:</strong> 인쇄 화면에서 <strong>\'대상: PDF로 저장\'</strong>을 선택하세요. (Chrome: "Save as PDF", Edge: "Microsoft Print to PDF")',
     '<strong>Note:</strong> In the print dialog, select <strong>"Save as PDF"</strong> as the destination.'),

    # ── warnings ──
    ('<strong>주의:</strong> 암호를 분실하면 PDF를 열 수 없습니다. 비밀번호를 안전한 곳에 기록해 두세요.',
     '<strong>Warning:</strong> If you forget the password, the PDF cannot be opened. Store it somewhere safe.'),
    ('<strong>Note:</strong> PowerPoint(PPTX)는 현재 지원되지 않습니다.',
     '<strong>Note:</strong> PowerPoint (PPTX) is not currently supported.'),

    # ── permissions ──
    ("if (permCopy) permDesc.push('복사');", "if (permCopy) permDesc.push('copy');"),
    ("if (permEdit) permDesc.push('편집');", "if (permEdit) permDesc.push('edit');"),
    ("if (permPrint) permDesc.push('인쇄');", "if (permPrint) permDesc.push('print');"),

    # ── delete button text ──
    ("content: '🗑️ 삭제';", "content: '🗑️ Delete';"),

    # ── font in Word export ──
    ("body { font-family: '맑은 고딕', 'Malgun Gothic', sans-serif; margin: 2cm; line-height: 1.8; color: #222; }",
     "body { font-family: Arial, sans-serif; margin: 2cm; line-height: 1.8; color: #222; }"),

    # ── JS error messages (more) ──
    ("showError('먼저 서명을 그려주세요.');", "showError('Please draw your signature first.');"),
    ("showError('워터마크 텍스트를 입력해 주세요.');", "showError('Please enter watermark text.');"),
    ("showError('열기 비밀번호를 입력해 주세요.');", "showError('Please enter the open password.');"),
    ("showError('이미지 파일(JPG, PNG)만 업로드할 수 있습니다.');", "showError('Only image files (JPG, PNG) are supported.');"),
    ("showError('유효한 Page Numbers가 없습니다.');", "showError('No valid page numbers.');"),
    ("if (!extractStr) { showError('추출할 pages를 입력해 주세요. 예: 1,3,5-8');",
     "if (!extractStr) { showError('Please enter pages to extract. e.g. 1,3,5-8');"),
    ("showError('유효한 pages 범위가 없습니다.');", "showError('No valid page range.');"),
    ("if (userPw.length < 4) { showError('비밀번호는 4자 이상이어야 합니다.'); return; }",
     "if (userPw.length < 4) { showError('Password must be at least 4 characters.'); return; }"),
    ("showError('병합하려면 PDF 파일이 2개 이상 필요합니다.');", "showError('At least 2 PDF files are required to merge.');"),
    ("showError('Excel 파일을 읽을 수 없습니다: ' + err.message);", "showError('Cannot read Excel file: ' + err.message);"),
    ("showError('Word 파일을 읽을 수 없습니다: ' + err.message);", "showError('Cannot read Word file: ' + err.message);"),
    ("showError('PDF를 불러오는 중 오류가 발생했습니다. 파일이 손상되었거나 암호로 보호되어 있을 수 있습니다.');",
     "showError('Failed to load PDF. The file may be corrupted or password-protected.');"),
    ("showError('PDF를 읽을 수 없습니다.');", "showError('Cannot read PDF.');"),
    ("showError('PDF를 읽을 수 없습니다: ' + err.message);", "showError('Cannot read PDF: ' + err.message);"),
    ("showError('ZIP 생성 중 오류가 발생했습니다.');", "showError('Failed to create ZIP file.');"),
    ("showError('변환 중 오류가 발생했습니다. PDF 파일이 손상되었거나 암호로 보호되어 있을 수 있습니다.');",
     "showError('Conversion failed. The PDF may be corrupted or password-protected.');"),
    ("showError('변환 중 오류가 발생했습니다: ' + err.message);", "showError('Conversion failed: ' + err.message);"),
    ("showError('병합 중 오류가 발생했습니다. 일부 PDF가 암호로 보호되어 있을 수 있습니다.');",
     "showError('Merge failed. Some PDFs may be password-protected.');"),
    ("showError('분할 중 오류가 발생했습니다: ' + err.message);", "showError('Split failed: ' + err.message);"),
    ("showError('처리 중 오류가 발생했습니다: ' + err.message);", "showError('Processing failed: ' + err.message);"),
    ("showError(err.message || '처리 중 오류가 발생했습니다.');", "showError(err.message || 'Processing failed.');"),

    # JS error messages (in script tags)
    ("'PDF 파일만 업로드할 수 있습니다.'", "'Only PDF files are supported.'"),
    ('"PDF 파일만 업로드할 수 있습니다."', '"Only PDF files are supported."'),
    ("'파일을 선택해주세요.'", "'Please select a file.'"),
    ("'비밀번호를 입력해주세요.'", "'Please enter the password.'"),
    ("'비밀번호가 일치하지 않습니다.'", "'Passwords do not match.'"),
    ("'페이지 범위가 올바르지 않습니다.'", "'Invalid page range.'"),
    ("'지원하지 않는 파일 형식입니다.'", "'Unsupported file format.'"),
    ('변환 중...', 'Processing...'),
    ('처리 중...', 'Processing...'),
    ('압축 중...', 'Compressing...'),
    # pwa install button
    ('>📌 홈 화면에 추가<', '>📌 Add to Home Screen<'),
    # our-sites-bar active link for tool pages
    ('href="https://pdfkit.wooahouse.com/" target="_blank" rel="noopener" class="active"',
     'href="https://pdfkit.wooahouse.com/en/" target="_blank" rel="noopener" class="active"'),

    # ── 추가 누락 문자열 ──
    # drop zone (이미지/Word/Excel)
    ('이미지 파일을 여기에 끌어다 놓으세요', 'Drop image files here'),
    ('Word 파일을 여기에 끌어다 놓으세요', 'Drop your Word file here'),
    ('Excel 파일을 여기에 끌어다 놓으세요', 'Drop your Excel file here'),
    ('PDF 파일들을 여기에 끌어다 놓으세요', 'Drop PDF files here'),
    ('파일을 여기에 끌어다 놓으세요', 'Drop your file here'),
    ('JPG, PNG, WEBP 형식 지원 · 여러 파일 동시 선택 가능', 'Supports JPG, PNG, WEBP · Multiple files supported'),
    ('JPG, PNG, WEBP, GIF 형식 지원', 'Supports JPG, PNG, WEBP, GIF'),
    ('여러 파일 동시 선택 가능', 'Multiple files supported'),
    # file input button labels
    ('이미지 Select File', 'Select Images'),
    ('이미지 추가', 'Add Image'),
    ('+ 이미지 추가', '+ Add Image'),
    # rotation labels
    ('>뒤집기<', '>Flip<'),
    ('>오른쪽<', '>Right<'),
    ('>왼쪽<', '>Left<'),
    ('<span style="font-size:0.72rem; color:#6B7280;">뒤집기</span>', '<span style="font-size:0.72rem; color:#6B7280;">Flip</span>'),
    ('<span style="font-size:0.72rem; color:#6B7280;">오른쪽</span>', '<span style="font-size:0.72rem; color:#6B7280;">Right</span>'),
    ('<span style="font-size:0.72rem; color:#6B7280;">왼쪽</span>', '<span style="font-size:0.72rem; color:#6B7280;">Left</span>'),
    # split options
    ('페이지마다 분할 (각 페이지를 별도 PDF로)', 'Split each page into separate PDFs'),
    ('범위로 분할 (직접 범위 지정)', 'Split by custom range'),
    # page number format
    ('숫자만', 'Numbers only'),
    ('줄표', 'Dash style'),
    ('전체 표시', 'Show total'),
    ('<span style="color:#9CA3AF; font-size:0.85rem;">예: - 1 - &nbsp; - 2 -</span>', '<span style="color:#9CA3AF; font-size:0.85rem;">e.g. - 1 - &nbsp; - 2 -</span>'),
    ('<span style="color:#9CA3AF; font-size:0.85rem;">예: 1 &nbsp; 2 &nbsp; 3</span>', '<span style="color:#9CA3AF; font-size:0.85rem;">e.g. 1 &nbsp; 2 &nbsp; 3</span>'),
    ('<span style="color:#9CA3AF; font-size:0.85rem;">예: 1 / 10 &nbsp; 2 / 10</span>', '<span style="color:#9CA3AF; font-size:0.85rem;">e.g. 1 / 10 &nbsp; 2 / 10</span>'),
    # watermark colors
    ('<span style="font-weight:600;">검정</span>', '<span style="font-weight:600;">Black</span>'),
    ('<span style="color:#1155CC; font-weight:600;">파랑</span>', '<span style="color:#1155CC; font-weight:600;">Blue</span>'),
    ('<span style="color:#888; font-weight:600;">회색</span>', '<span style="color:#888; font-weight:600;">Gray</span>'),
    ('<span style="color:#DD0000; font-weight:600;">빨강</span>', '<span style="color:#DD0000; font-weight:600;">Red</span>'),
    # watermark size
    ('>대<', '>Large<'),
    ('>중<', '>Medium<'),
    ('>소<', '>Small<'),
    # watermark range
    ('Custom Range만', 'Custom Range only'),
    ('Custom Range 추출 (선택한 페이지만)', 'Custom Range (selected pages only)'),
    # password fields
    ('placeholder="비밀번호 (없으면 빈칸으로 시도)"', 'placeholder="Password (leave blank if none)"'),
    ('placeholder="PDF를 열 때 필요한 비밀번호"', 'placeholder="Password to open PDF"'),
    ('placeholder="비밀번호를 다시 입력하세요"', 'placeholder="Confirm password"'),
    ('placeholder="(선택) 권한 변경용 비밀번호"', 'placeholder="(Optional) Owner password"'),
    # permissions checkboxes
    ('복사 허용', 'Allow copying'),
    ('편집 허용', 'Allow editing'),
    ('인쇄 허용', 'Allow printing'),
    # password toggle button
    ('title="비밀번호 보기/숨기기"', 'title="Show/Hide password"'),
    # select all / deselect
    ('>전체 선택<', '>Select All<'),
    ('>선택 해제<', '>Deselect All<'),
    # file list
    ('<div class="file-list-title">선택된 이미지 <span style="font-weight:400;font-size:0.8rem;">(드래그로 순서 변경)</span></div>',
     '<div class="file-list-title">Selected Images <span style="font-weight:400;font-size:0.8rem;">(drag to reorder)</span></div>'),
    # image layout option
    ('<span class="option-label">이미지 배치</span>', '<span class="option-label">Image Layout</span>'),
    ('<option value="auto">이미지 크기에 맞춤 (권장)</option>', '<option value="auto">Fit to image size (recommended)</option>'),
    # compression info
    ('ℹ️ 이 도구는 <strong>이미지가 포함된 PDF</strong>에 효과적입니다. 텍스트만 있는 PDF는 압축 효과가 제한될 수 있습니다.',
     'ℹ️ This tool works best with <strong>image-heavy PDFs</strong>. Text-only PDFs may see limited compression.'),
    (': \'텍스트 중심 PDF는 압축 효과가 제한됩니다.\';', ': \'Text-based PDFs may show limited compression.\';'),
    # page count
    ('페이지', 'pages'),
    # tool list sidebar links
    ('>📄 이미지 → PDF 변환<', '>📄 Image → PDF<'),
    # viewer card
    ('<div class="viewer-card-maker">Apple (기본 내장)</div>', '<div class="viewer-card-maker">Apple (built-in)</div>'),
    ('<div class="viewer-card-name">기본 파일 앱</div>', '<div class="viewer-card-name">Files App</div>'),
    # error messages in JS
    ("'비밀번호가 올바르지 않거나 해제할 수 없는 파일입니다.'", "'Incorrect password or file cannot be unlocked.'"),
    ('추출할 텍스트가 없습니다. 스캔된 이미지 PDF일 수 있습니다.', 'No text found. This may be a scanned image PDF.'),
    # tool desc paragraph (jpg-to-pdf)
    ('<p>JPG, PNG 이미지를 PDF로 변환합니다. 여러 이미지를 드래그로 순서를 바꾼 후 하나의 PDF로 만들 수 있습니다.</p>',
     '<p>Convert JPG, PNG images to PDF. Drag to reorder multiple images, then combine into one PDF.</p>'),
    # progress UI
    ('이미지 처리 중', 'Processing image'),
    ('서명 이미지 준비 중...', 'Preparing signature image...'),
    ('워터마크 이미지 생성 중...', 'Generating watermark...'),
    # result messages
    ('개 페이지가', 'pages converted to'),
    ('이미지로 변환되었습니다', ''),
    ('개의 이미지가 PDF로 변환되었습니다', 'images converted to PDF'),

    # ── 추가 누락 2차 ──
    # watermark size radio labels
    ('<label class="radio-item"><input type="radio" name="wmSize" value="large"> 대</label>',
     '<label class="radio-item"><input type="radio" name="wmSize" value="large"> Large</label>'),
    ('<label class="radio-item"><input type="radio" name="wmSize" value="medium" checked> 중</label>',
     '<label class="radio-item"><input type="radio" name="wmSize" value="medium" checked> Medium</label>'),
    ('<label class="radio-item"><input type="radio" name="wmSize" value="small"> 소</label>',
     '<label class="radio-item"><input type="radio" name="wmSize" value="small"> Small</label>'),
    # watermark position options
    ('<option value="diagonal">중앙 대각선 (45°) — 권장</option>', '<option value="diagonal">Center Diagonal (45°) — Recommended</option>'),
    ('<option value="center">중앙 수평</option>', '<option value="center">Center Horizontal</option>'),
    ('<option value="bottom-left">왼쪽 하단</option>', '<option value="bottom-left">Bottom Left</option>'),
    ('<option value="bottom-right">오른쪽 하단</option>', '<option value="bottom-right">Bottom Right</option>'),
    # watermark opacity / margin options
    ('<option value="0.10">10% (매우 연하게)</option>', '<option value="0.10">10% (Very light)</option>'),
    ('<option value="0.50">50% (진하게)</option>', '<option value="0.50">50% (Dark)</option>'),
    ('<option value="20" selected>보통 (20px)</option>', '<option value="20" selected>Normal (20px)</option>'),
    ('<option value="40">넓음 (40px)</option>', '<option value="40">Wide (40px)</option>'),
    ('<option value="0">여백 없음</option>', '<option value="0">No margin</option>'),
    # paper size options
    ('<option value="a4">A4 (210 × 297mm)</option>', '<option value="a4">A4 (210 × 297mm)</option>'),
    ('<option value="letter">Letter (216 × 279mm)</option>', '<option value="letter">Letter (216 × 279mm)</option>'),
    # image fit options
    ('<option value="contain">pages에 맞춤 (비율 유지)</option>', '<option value="contain">Fit to page (keep ratio)</option>'),
    ('<option value="fill">pages 채우기</option>', '<option value="fill">Fill page</option>'),
    # result title
    ('<div class="result-title">암호 설정 완료!</div>', '<div class="result-title">Password Set!</div>'),
    # error in JS
    ("showError('올바른 Page Numbers를 입력해 주세요.');", "showError('Please enter valid page numbers.');"),
    ("showError('올바른 페이지 번호를 입력해 주세요.');", "showError('Please enter valid page numbers.');"),

    # ── JS 동적 텍스트 (textContent) ──
    # PDF→PNG dynamic title/desc
    ("document.getElementById('toolTitle').textContent = 'PDF를 PNG로 변환';",
     "document.getElementById('toolTitle').textContent = 'PDF to PNG Converter';"),
    ("document.getElementById('toolDesc').textContent = 'PDF 파일을 업로드하면 각 페이지를 PNG 이미지로 변환해 드립니다. 투명 배경이 지원됩니다.';",
     "document.getElementById('toolDesc').textContent = 'Upload a PDF and convert each page to a PNG image. Transparent backgrounds supported.';"),
    ("document.getElementById('toolDesc').textContent = 'PDF 파일을 업로드하면 각 pages를 PNG 이미지로 변환해 드립니다. 투명 배경이 지원됩니다.';",
     "document.getElementById('toolDesc').textContent = 'Upload a PDF and convert each page to a PNG image. Transparent backgrounds supported.';"),
    ("document.getElementById('breadcrumbTitle').textContent = 'PDF → PNG 변환';",
     "document.getElementById('breadcrumbTitle').textContent = 'PDF → PNG';"),
    ("document.title = 'PDF를 PNG로 변환 - WooaPDF';",
     "document.title = 'PDF to PNG Converter - WooaPDF';"),
    # button states
    ("btn.textContent = '⏳ 변환 중...';", "btn.textContent = '⏳ Converting...';"),
    ("btn.disabled = true; btn.textContent = '⏳ 변환 중...';", "btn.disabled = true; btn.textContent = '⏳ Converting...';"),
    ("btn.textContent = '⏳ 압축 중...';", "btn.textContent = '⏳ Compressing...';"),
    ("btn.disabled = true; btn.textContent = '⏳ 압축 중...';", "btn.disabled = true; btn.textContent = '⏳ Compressing...';"),
    ("btn.textContent = '⏳ 처리 중...';", "btn.textContent = '⏳ Processing...';"),
    ("btn.disabled = true; btn.textContent = '⏳ 처리 중...';", "btn.disabled = true; btn.textContent = '⏳ Processing...';"),
    ("btn.textContent = '⏳ 병합 중...';", "btn.textContent = '⏳ Merging...';"),
    ("btn.textContent = '⏳ 분할 중...';", "btn.textContent = '⏳ Splitting...';"),
    ("btn.textContent = '🔄 변환 시작';", "btn.textContent = '🔄 Convert';"),
    ("btn.textContent = '🔄 회전 적용';", "btn.textContent = '🔄 Apply Rotation';"),
    ("btn.textContent = '🔗 PDF 병합하기';", "btn.textContent = '🔗 Merge PDF';"),
    ("btn.textContent = '✂️ 분할하기';", "btn.textContent = '✂️ Split PDF';"),
    ("btn.textContent = '🗜️ 압축 시작';", "btn.textContent = '🗜️ Compress PDF';"),
    ("btn.disabled = false; btn.textContent = '🔓 잠금 해제';", "btn.disabled = false; btn.textContent = '🔓 Unlock PDF';"),
    ("btn.textContent = '📄 PDF로 변환';", "btn.textContent = '📄 Convert to PDF';"),
    ("btn.textContent = '📦 ZIP 생성 중...';", "btn.textContent = '📦 Creating ZIP...';"),
    ("btn.textContent = '⬇️ ZIP으로 다운로드';", "btn.textContent = '⬇️ Download ZIP';"),
    ("btn.textContent = '⬇️ 전체 다운로드 (ZIP)';", "btn.textContent = '⬇️ Download All (ZIP)';"),
    ("btn.textContent = '✅ 복사됨!';", "btn.textContent = '✅ Copied!';"),
    ("setTimeout(() => btn.textContent = '📋 전체 복사', 2000);", "setTimeout(() => btn.textContent = '📋 Copy All', 2000);"),
    # resetBtn functions
    ("function resetBtn(btn) { btn.disabled = false; btn.textContent = '✍️ 서명 삽입 및 다운로드'; }",
     "function resetBtn(btn) { btn.disabled = false; btn.textContent = '✍️ Insert Signature & Download'; }"),
    ("function resetBtn(btn) { btn.disabled = false; btn.textContent = '💧 워터마크 추가'; }",
     "function resetBtn(btn) { btn.disabled = false; btn.textContent = '💧 Add Watermark'; }"),
    ("function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔀 재정렬 적용 및 다운로드'; }",
     "function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔀 Apply Reorder & Download'; }"),
    ("function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔐 암호 설정 및 다운로드'; }",
     "function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔐 Protect & Download'; }"),
    ("function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔢 페이지 번호 추가'; }",
     "function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔢 Add Page Numbers'; }"),
    ("function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔤 Word 파일로 변환'; }",
     "function resetBtn(btn) { btn.disabled = false; btn.textContent = '🔤 Convert to Word'; }"),
    # delete page button states
    ("btn.textContent = '🗑️ 선택한 페이지 삭제';", "btn.textContent = '🗑️ Delete Selected Pages';"),
    ("`🗑️ ${count}개 페이지 삭제`", "`🗑️ Delete ${count} Pages`"),
    ("`🗑️ ${selectedPages.size}개 페이지 삭제`", "`🗑️ Delete ${selectedPages.size} Pages`"),
    # file info
    ("`${file.name} · ${totalPages}페이지`", "`${file.name} · ${totalPages} pages`"),
    ("`썸네일 렌더링 중... (${i + 1}/${totalPages})`", "`Rendering thumbnails... (${i + 1}/${totalPages})`"),
    ("'선택된 페이지 없음'", "'No pages selected'"),
    ("`${count}개 선택됨 (전체 선택 — 최소 1페이지는 남겨야 합니다)`",
     "`${count} selected (all selected — at least 1 page must remain)`"),
    ("`${count}개 페이지 선택됨 → ${totalPages - count}개 남음`",
     "`${count} pages selected → ${totalPages - count} remaining`"),
    # label / opt
    ("`원본 ${i + 1}p`", "`Page ${i + 1}`"),
    ("`${i}페이지`", "`Page ${i}`"),
    # text output
    ("|| '(텍스트 없음)'", "|| '(No text found)'"),
    # split errors
    ("showError('추출할 페이지를 입력해 주세요. 예: 1,3,5-8')", "showError('Please enter pages to extract. e.g. 1,3,5-8')"),
    ("showError('범위를 입력해 주세요. 예: 1-3, 4-7')", "showError('Please enter a range. e.g. 1-3, 4-7')"),
    # password toggle
    ("else { inp.type = 'password'; btn.textContent = '👁️'; }",
     "else { inp.type = 'password'; btn.textContent = '👁️'; }"),
    # title attr
    ("item.title = '클릭하여 개별 다운로드';", "item.title = 'Click to download individually';"),

    # ── JS 동적 텍스트 추가 ──
    ("showError('올바른 pages 범위를 입력해 주세요. 예: 1,3,5-8');",
     "showError('Please enter a valid page range. e.g. 1,3,5-8');"),
    ("throw new Error('이 PDF는 비밀번호가 필요합니다. 비밀번호를 입력하고 다시 시도하세요.');",
     "throw new Error('This PDF requires a password. Please enter the password and try again.');"),
    ("`${i + 1}/${totalPages} pages 처리 중`", "`Processing ${i + 1}/${totalPages} pages`"),
    ("`범위 ${ri + 1}/${ranges.length} 처리 중`", "`Processing range ${ri + 1}/${ranges.length}`"),
    ("? `${formatSize(origSize)} → ${formatSize(compSize)} (${ratio}% 감소)`",
     "? `${formatSize(origSize)} → ${formatSize(compSize)} (${ratio}% smaller)`"),
    # App Store link (kr → com)
    ('href="https://apps.apple.com/kr/app/adobe-acrobat-reader-pdf-뷰어/id469337564"',
     'href="https://apps.apple.com/app/adobe-acrobat-reader/id469337564"'),

    # ── 추가 누락 3차 ──
    # page number position options
    ('<option value="bottom-center">아래 중앙</option>', '<option value="bottom-center">Bottom Center</option>'),
    ('<option value="bottom-left">아래 왼쪽</option>', '<option value="bottom-left">Bottom Left</option>'),
    ('<option value="bottom-right">아래 오른쪽</option>', '<option value="bottom-right">Bottom Right</option>'),
    ('<option value="top-center">위 중앙</option>', '<option value="top-center">Top Center</option>'),
    ('<option value="top-left">위 왼쪽</option>', '<option value="top-left">Top Left</option>'),
    ('<option value="top-right">위 오른쪽</option>', '<option value="top-right">Top Right</option>'),
    # font size options
    ('<option value="8">8pt (작게)</option>', '<option value="8">8pt (Small)</option>'),
    ('<option value="10" selected>10pt (기본)</option>', '<option value="10" selected>10pt (Default)</option>'),
    ('<option value="14">14pt (크게)</option>', '<option value="14">14pt (Large)</option>'),
    # margin options
    ('<option value="20">20px (좁게)</option>', '<option value="20">20px (Narrow)</option>'),
    ('<option value="28" selected>28px (기본)</option>', '<option value="28" selected>28px (Default)</option>'),
    ('<option value="36">36px (넓게)</option>', '<option value="36">36px (Wide)</option>'),

    # ── unlock-pdf JS comment ──
    ('// 비밀번호 없이 저장 = 잠금 해제', '// Save without password = unlocked'),

    # ── jpg-to-pdf page size option ──
    ('<span class="option-label">pages 크기</span>',
     '<span class="option-label">Page Size</span>'),

    # ── watermark apply pages option ──
    ('<span class="option-label">적용 pages</span>',
     '<span class="option-label">Apply To</span>'),

    # ── pdf-to-jpg JS progress text (no exclamation) ──
    ("total === 0 ? '완료' :",
     "total === 0 ? 'Done' :"),
    ('`${done}/${total} pages 변환 중 (pages ${current})`',
     '`Converting page ${current} (${done}/${total})`'),

    # ── Tool description paragraphs (no id="toolDesc") ──
    ('<p>PDF 파일 용량을 줄여 저장 및 공유를 쉽게 합니다.</p>',
     '<p>Reduces PDF file size for easy storage and sharing.</p>'),
    ('<p>용량을 줄일 PDF 파일을 업로드하세요</p>',
     '<p>Upload a PDF file to compress its size</p>'),
    ('<p>PDF pages의 방향을 90°, 180°, 270° 회전합니다.</p>',
     '<p>Rotates PDF pages 90°, 180°, or 270°.</p>'),
    ('<p>PDF pages에 텍스트 워터마크를 삽입합니다.</p>',
     '<p>Inserts a text watermark on PDF pages.</p>'),
    ('<p>PDF 파일을 pages별로 나누거나 원하는 범위로 분할합니다.</p>',
     '<p>Splits a PDF into individual pages or custom page ranges.</p>'),
    ('<p>비밀번호로 보호된 PDF의 잠금을 해제합니다.</p>',
     '<p>Removes password protection from a PDF file.</p>'),
    ('<p>잠금을 해제할 PDF 파일을 업로드하세요</p>',
     '<p>Upload the password-protected PDF to unlock</p>'),
    ('<p>PDF의 각 pages에 번호를 자동으로 삽입합니다.</p>',
     '<p>Automatically inserts page numbers into each PDF page.</p>'),
    ('<p>드래그 앤 드롭으로 PDF pages 순서를 자유롭게 변경합니다.</p>',
     '<p>Freely rearrange PDF page order with drag and drop.</p>'),
    ('<p>캔버스에 서명을 그린 뒤 PDF 문서에 삽입합니다.</p>',
     '<p>Draw a signature on the canvas then insert it into your PDF.</p>'),
    ('<p>서명을 추가할 PDF를 업로드하세요</p>',
     '<p>Upload a PDF to add your signature</p>'),
    ('<p>Word로 변환할 PDF를 업로드하세요</p>',
     '<p>Upload a PDF to convert to Word</p>'),
    ('<p>PDF 파일에 열기 비밀번호를 설정하여 문서를 보호합니다.</p>',
     '<p>Protect your PDF by setting a password to restrict access.</p>'),

    # ── Breadcrumb / section spans ──
    ('<span>pages 삭제</span>', '<span>Delete Pages</span>'),
    ('<span>pages 재정렬</span>', '<span>Reorder Pages</span>'),

    # ── Delete pages UI ──
    ('<p>삭제할 pages를 클릭해서 선택한 후 "삭제하기" 버튼을 누르세요.</p>',
     '<p>Click pages to select them, then press the "Delete" button.</p>'),
    ('<p>pages를 선택해서 삭제할 PDF를 업로드하세요</p>',
     '<p>Upload a PDF to select and delete pages</p>'),
    ('<div>pages 미리보기를 생성하고 있습니다...</div>',
     '<div>Generating page previews...</div>'),
    ('삭제할 pages를 클릭해서 선택하세요 (다시 클릭하면 취소)',
     'Click to select pages to delete (click again to deselect)'),
    ('<span class="selection-info" id="selectionInfo">선택된 pages 없음</span>',
     '<span class="selection-info" id="selectionInfo">No pages selected</span>'),
    ('<button class="btn-convert" id="deleteBtn" disabled>🗑️ 선택한 pages 삭제</button>',
     '<button class="btn-convert" id="deleteBtn" disabled>🗑️ Delete Selected Pages</button>'),

    # ── Rotate PDF UI ──
    ('>전체 <span id="totalPagesHint">0</span>pages</div>',
     '>Total: <span id="totalPagesHint">0</span> pages</div>'),

    # ── Split PDF UI ──
    ('<span class="option-label">pages 선택</span>',
     '<span class="option-label">Page Selection</span>'),
    ('선택한 pages만 하나의 PDF로 추출됩니다',
     'Only selected pages will be extracted as one PDF'),

    # ── Watermark UI ──
    ('placeholder="예: CONFIDENTIAL, 사본, 샘플"',
     'placeholder="e.g. CONFIDENTIAL, COPY, SAMPLE"'),

    # ── Sign PDF UI ──
    ('<label>pages 선택:</label>', '<label>Page:</label>'),

    # ── PDF viewer body text ──
    ('회원가입 없이 브라우저에서 바로 사용 가능합니다.',
     'Use directly in your browser — no sign-up needed.'),

    # ── PDF to Word info note ──
    ('<strong>안내:</strong> 텍스트 기반 PDF만 지원됩니다. 스캔된 이미지 PDF는 <a href="https://imagekit.wooahouse.com/ocr-pdf.html" target="_blank" rel="noopener" style="color:#F57F17; font-weight:700;">WooaImage OCR 도구</a>를 이용하세요.',
     '<strong>Note:</strong> Only text-based PDFs are supported. For scanned image PDFs, use <a href="https://imagekit.wooahouse.com/ocr-pdf.html" target="_blank" rel="noopener" style="color:#F57F17; font-weight:700;">WooaImage OCR Tool</a>.'),

    # ── JS progress/result messages ──
    ("updateProgressUI(30, 'pages 회전 중...')",
     "updateProgressUI(30, 'Rotating pages...')"),
    ("updateProgressUI(30, 'pages 제거 중...')",
     "updateProgressUI(30, 'Removing pages...')"),
    ("updateProgressUI(50, 'pages 추출 중...')",
     "updateProgressUI(50, 'Extracting pages...')"),

    # JS template literals — delete pages
    ("info.textContent = '선택된 pages 없음';",
     "info.textContent = 'No pages selected';"),
    ("btn.textContent = '🗑️ 선택한 pages 삭제';",
     "btn.textContent = '🗑️ Delete Selected Pages';"),
    ('info.textContent = `${count}개 선택됨 (전체 선택 — 최소 1pages는 남겨야 합니다)`;',
     'info.textContent = `${count} selected (all pages — at least 1 page must remain)`;'),
    ('info.textContent = `${count}개 pages 선택됨 → ${totalPages - count}개 남음`;',
     'info.textContent = `${count} pages selected → ${totalPages - count} remaining`;'),
    ('btn.textContent = `🗑️ ${count}개 pages 삭제`;',
     'btn.textContent = `🗑️ Delete ${count} Pages`;'),
    ('`${selectedPages.size}개 pages가 삭제되어 ${keepIndices.length}개 pages만 남았습니다`',
     '`${selectedPages.size} pages deleted, ${keepIndices.length} pages remaining`'),
    ('btn.textContent = `🗑️ ${selectedPages.size}개 pages 삭제`',
     'btn.textContent = `🗑️ Delete ${selectedPages.size} Pages`'),

    # JS template literals — rotate
    ('`${pagesToRotate.length}개 pages가 ${angle}° 회전되었습니다`',
     '`${pagesToRotate.length} pages rotated by ${angle}°`'),

    # JS template literals — watermark
    ('`${targetPages.length}개 pages에 워터마크가 추가되었습니다`',
     '`Watermark added to ${targetPages.length} pages`'),

    # JS template literals — split
    ("showError('유효한 pages 범위가 없습니다.');",
     "showError('No valid page ranges found.');"),
    ("showError('추출할 pages를 입력해 주세요. 예: 1,3,5-8');",
     "showError('Enter pages to extract. e.g. 1,3,5-8');"),

    # JS template literals — page numbers
    ('`${totalPgs}개 pages에 번호가 추가되었습니다 (${startNum}번부터 시작)`',
     '`Page numbers added to ${totalPgs} pages (starting from ${startNum})`'),
    ("btn.textContent = '🔢 Page Numbers 추가';",
     "btn.textContent = '🔢 Add Page Numbers';"),

    # JS template literals — reorder
    ('`pages ${i + 1}/${pageOrder.length} 복사 중...`',
     '`Copying page ${i + 1}/${pageOrder.length}...`'),
    ('`${pageOrder.length}pages 재정렬 완료 (${newOrderStr})`',
     '`${pageOrder.length} pages reordered (${newOrderStr})`'),

    # JS template literals — sign
    ('`${currentPage}pages에 서명이 삽입되었습니다`',
     '`Signature inserted on page ${currentPage}`'),

    # JS template literals — pdf-to-word
    ('`pages ${pageNum}/${numPages} 텍스트 추출 중...`',
     '`Extracting text from page ${pageNum}/${numPages}...`'),
    ('`${targetPages.length}개 pages의 텍스트가 Word 문서로 변환되었습니다`',
     '`Text from ${targetPages.length} pages converted to Word document`'),

    # JS template literals — merge
    ('`${i + 1}/${fileItems.length} 처리 중: ${fileItems[i].file.name}`',
     '`Processing ${i + 1}/${fileItems.length}: ${fileItems[i].file.name}`'),
    ('`${fileItems.length}개 파일, 총 ${totalPages}pages가 하나의 PDF로 병합되었습니다`',
     '`${fileItems.length} files, ${totalPages} pages merged into one PDF`'),

    # JS template literals — text extract
    ('`pages ${i}/${numPages} 추출 중...`',
     '`Extracting page ${i}/${numPages}...`'),
]

# ── 3. 언어 선택기 CSS ────────────────────────────────────────────────────────
LANG_SWITCHER_CSS = """    .lang-switcher { display:flex; align-items:center; gap:4px; }
    .lang-switcher a { color:rgba(255,255,255,0.7); text-decoration:none; font-size:0.8rem; font-weight:600; padding:3px 8px; border-radius:12px; transition:background 0.15s; }
    .lang-switcher a.active { color:white; background:rgba(255,255,255,0.25); }
    .lang-switcher a:hover { color:white; background:rgba(255,255,255,0.18); }
    .lang-switcher span { color:rgba(255,255,255,0.3); font-size:0.75rem; }
"""

def build_page(filename, meta):
    ko_path = os.path.join(BASE, filename)
    en_path = os.path.join(EN_DIR, filename)

    with open(ko_path, encoding='utf-8') as f:
        html = f.read()

    # ── 메타 태그 교체 ──
    html = re.sub(r'<title>[^<]+</title>', f'<title>{meta["title"]}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{meta["desc"]}"', html)
    html = re.sub(r'<meta name="keywords" content="[^"]*"', f'<meta name="keywords" content="{meta["kw"]}"', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{meta["og_title"]}"', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{meta["og_desc"]}"', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://pdfkit.wooahouse.com/en/{filename}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://pdfkit.wooahouse.com/en/{filename}"', html)

    # ── hreflang 추가 (canonical 바로 뒤) ──
    hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="https://pdfkit.wooahouse.com/{filename}">'
                f'\n  <link rel="alternate" hreflang="en" href="https://pdfkit.wooahouse.com/en/{filename}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="https://pdfkit.wooahouse.com/en/{filename}">')
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

    # ── ld+json 업데이트 ──
    # Replace any "name" field containing Korean characters
    html = re.sub(r'"name": "([^"]*[가-힣][^"]*)"', f'"name": "{meta["app_name"]}"', html)
    # Replace any "description" field containing Korean characters in ld+json
    html = re.sub(r'"description": "([^"]*[가-힣][^"]*)"', f'"description": "{meta["desc"]}"', html)
    html = re.sub(r'"url": "https://pdfkit\.wooahouse\.com/' + re.escape(filename) + '"',
                  f'"url": "https://pdfkit.wooahouse.com/en/{filename}"', html)

    # ── FAQ 교체 ──
    if meta.get('faq'):
        faq_items = meta['faq']
        faq_html_parts = []
        for i, (q, a) in enumerate(faq_items):
            is_last = (i == len(faq_items) - 1)
            mb = '' if is_last else 'margin-bottom:1.2rem;'
            faq_html_parts.append(
                f'      <div class="faq-item" style="{mb}padding:1rem;background:#f8f9fa;border-radius:8px;">\n'
                f'        <h3 style="font-size:1rem;font-weight:600;margin-bottom:0.5rem;">Q. {q}</h3>\n'
                f'        <p style="color:#555;margin:0;">{a}</p>\n'
                f'      </div>'
            )
        faq_inner = '\n'.join(faq_html_parts)
        html = re.sub(
            r'<div class="faq-list">.*?</div>\s*</section>',
            f'<div class="faq-list">\n{faq_inner}\n    </div>\n  </section>',
            html, flags=re.DOTALL
        )
        # Handle <details>/<summary> FAQ format
        faq_details_parts = []
        for i, (q, a) in enumerate(faq_items):
            is_last = (i == len(faq_items) - 1)
            border = '' if is_last else 'border-bottom:1px solid #E5E7EB;'
            faq_details_parts.append(
                f'      <details style="{border}padding:16px">\n'
                f'        <summary style="font-weight:700;cursor:pointer;color:#111827">{q}</summary>\n'
                f'        <p style="margin-top:10px;color:#6B7280;line-height:1.6">{a}</p>\n'
                f'      </details>'
            )
        faq_details_inner = '\n'.join(faq_details_parts)
        html = re.sub(
            r'(<div[^>]*border[^>]*border-radius[^>]*overflow[^>]*>)\s*<details.*?</details>\s*</div>',
            r'\1\n' + faq_details_inner + '\n    </div>',
            html, flags=re.DOTALL
        )
        html = re.sub(r'<h2[^>]*>자주 묻는 질문</h2>', '<h2 style="font-size:1.4rem;margin-bottom:1.5rem;">Frequently Asked Questions</h2>', html)
        # Also fix the smaller faq-section h2 format used by some pages
        html = re.sub(r'<h2[^>]*font-weight:800[^>]*>자주 묻는 질문</h2>', '<h2 style="font-size:1.1rem;font-weight:800;color:#374151;margin-bottom:16px">Frequently Asked Questions</h2>', html)
        # ── FAQPage ld+json 교체 ──
        import json as _json
        faq_entities = []
        for q, a in faq_items:
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            })
        new_faq_json = _json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }, ensure_ascii=False, indent=2)
        html = re.sub(
            r'<script type="application/ld\+json">\s*\{[^<]*"FAQPage"[^<]*\}[^<]*</script>',
            f'<script type="application/ld+json">\n{new_faq_json}\n</script>',
            html, flags=re.DOTALL
        )

    # ── cross-link banner 교체 ──
    if meta.get('cross_banner_text'):
        html = re.sub(
            r'<span style="font-size:0\.95rem;color:#444;">[^<]*</span>',
            f'<span style="font-size:0.95rem;color:#444;">{meta["cross_banner_text"]}</span>',
            html
        )
        html = re.sub(
            r'<a href="[^"]*" target="_blank" rel="noopener" style="background:#4F6EF7[^>]*>[^<]*</a>',
            f'<a href="{meta["cross_banner_href"]}" target="_blank" rel="noopener" style="background:#4F6EF7;color:#fff;padding:0.5rem 1rem;border-radius:8px;text-decoration:none;font-size:0.9rem;white-space:nowrap;">{meta["cross_banner_link_text"]}</a>',
            html
        )

    # ── Tool header (h1, desc, breadcrumb) ──
    if meta.get('h1'):
        # id="toolTitle" 있는 경우
        replaced = re.sub(r'<h1 id="toolTitle">[^<]*</h1>', f'<h1 id="toolTitle">{meta["h1"]}</h1>', html)
        if replaced == html:
            # id 없는 plain <h1> 교체 (첫 번째만)
            replaced = re.sub(r'<h1>([^<]*)</h1>', f'<h1>{meta["h1"]}</h1>', html, count=1)
        html = replaced
    if meta.get('tool_desc'):
        replaced = re.sub(r'<p id="toolDesc">[^<]*</p>', f'<p id="toolDesc">{meta["tool_desc"]}</p>', html)
        if replaced == html:
            # id 없는 경우 COMMON 치환으로 처리됨
            pass
        html = replaced
    if meta.get('breadcrumb'):
        html = re.sub(r'<span id="breadcrumbTitle">[^<]*</span>', f'<span id="breadcrumbTitle">{meta["breadcrumb"]}</span>', html)

    # ── 공통 문자열 치환 ──
    for ko, en in COMMON:
        html = html.replace(ko, en)

    # ── CSS 경로 (style 태그 내 inline) ──
    # link manifest already handled by COMMON
    # g.js path (already absolute, fine)

    # ── 언어 선택기 CSS 삽입 ──
    if 'lang-switcher' not in html:
        html = html.replace('  </style>', LANG_SWITCHER_CSS + '  </style>', 1)

    # ── 헤더에 언어 선택기 삽입 ──
    ko_link = f'../{ filename }'
    lang_switcher_html = (
        f'    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="{ko_link}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>'
    )
    # Replace closing </header> section — About 링크 포함
    html = re.sub(
        r'(\s*</div>\s*</header>)',
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'      <a href="../about.html" style="color:rgba(255,255,255,0.85); font-size:0.85rem; text-decoration:none; margin-left:8px;">About</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>',
        html, count=1
    )

    # ── 영어 버전: 쿠팡 완전 제거 → 애드센스로 교체 ──
    ADSENSE_BLOCK = (
        '<div style="text-align:center;margin:32px auto 0;max-width:728px;padding:0 8px">\n'
        '<ins class="adsbygoogle"\n'
        '     style="display:block"\n'
        '     data-ad-client="ca-pub-6464921081676309"\n'
        '     data-ad-slot="7080296704"\n'
        '     data-ad-format="auto"\n'
        '     data-full-width-responsive="true"></ins>\n'
        '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n'
        '</div>'
    )
    # head의 g.js 제거
    html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
    # 쿠팡 Partners 블록 전체를 애드센스로 교체
    html = re.sub(
        r'<!-- Coupang Partners -->\s*<div[^>]*>.*?</div>',
        ADSENSE_BLOCK,
        html, flags=re.DOTALL
    )
    # 혹시 남은 PartnersCoupang 스크립트 제거
    html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)
    # coupang-notice 제거
    html = re.sub(r'<p class="coupang-notice">[^<]*</p>', '', html)

    # ── og:locale 교체 ──
    html = html.replace('content="ko_KR"', 'content="en_US"')

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  ✅ en/{filename}')


# ── 4. 실행 ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Building English pages...')
    for filename, meta in PAGE_META.items():
        ko_path = os.path.join(BASE, filename)
        if os.path.exists(ko_path):
            build_page(filename, meta)
        else:
            print(f'  ⚠️  {filename} not found, skipping')

    # about, privacy 복사 후 기본 번역
    ABOUT_EXTRA = [
        ('<title>서비스 소개 | WooaPDF</title>', '<title>About WooaPDF – Free Online PDF Tools</title>'),
        ('<meta name="description" content="WooaPDF은 PDF 변환, 병합, 분할 등 다양한 PDF 작업을 무료로 제공하는 온라인 도구입니다. 파일이 서버에 저장되지 않아 개인정보가 안전합니다.">', '<meta name="description" content="WooaPDF is a free online PDF toolkit for converting, merging, splitting, and more. Your files never leave your browser — 100% private.">'),
        ('<h1 style="font-size:1.8rem;">WooaPDF 서비스 소개</h1>', '<h1 style="font-size:1.8rem;">About WooaPDF</h1>'),
        # About page body content
        ('<p>무료 PDF 도구 모음 서비스</p>', '<p>Free Online PDF Toolkit</p>'),
        ('<h2>WooaPDF이란?</h2>', '<h2>What is WooaPDF?</h2>'),
        ('WooaPDF은 누구나 쉽게 PDF 파일을 다룰 수 있도록 도와주는 <strong>무료 온라인 PDF 도구 서비스</strong>입니다.',
         'WooaPDF is a <strong>free online PDF toolkit</strong> that makes it easy for anyone to work with PDF files.'),
        ('회원가입이나 프로그램 설치 없이 웹 브라우저에서 바로 사용할 수 있으며,',
         'No sign-up or software installation needed — just open your browser and get started.'),
        ('모든 처리가 사용자의 브라우저 안에서 이루어집니다.',
         'All processing happens entirely within your browser.'),
        ('업무용 문서, 학교 과제, 개인 자료 등 다양한 상황에서 PDF를 간편하게 처리할 수 있도록',
         'Whether for work documents, school assignments, or personal files,'),
        ('최적화된 도구들을 제공합니다.',
         'WooaPDF provides optimized tools for every PDF task.'),
        ('<h2>제공 서비스</h2>', '<h2>Our Tools</h2>'),
        ('🖼️ PDF → JPG 변환', '🖼️ PDF → JPG'),
        ('📸 PDF → PNG 변환', '📸 PDF → PNG'),
        ('📄 이미지 → PDF 변환', '📄 Image → PDF'),
        ('🔗 PDF 병합', '🔗 Merge PDF'),
        ('✂️ PDF 분할', '✂️ Split PDF'),
        ('🔄 PDF 회전', '🔄 Rotate PDF'),
        ('🗑️ 페이지 삭제', '🗑️ Delete Pages'),
        ('<h2>핵심 특징</h2>', '<h2>Key Features</h2>'),
        ('<strong>🔒 완전한 Privacy Protected</strong> — 업로드한 파일은 서버로 전송되거나 저장되지 않습니다.',
         '<strong>🔒 100% Private</strong> — Uploaded files are never sent to or stored on any server.'),
        ('모든 PDF 처리는 사용자의 컴퓨터(브라우저) 안에서만 이루어집니다.',
         'All PDF processing happens only inside your computer (browser).'),
        ('<strong>⚡ 빠른 처리 속도</strong> — 서버 업로드 대기 없이 로컬에서 직접 처리하므로',
         '<strong>⚡ Fast Processing</strong> — Files are processed locally without server upload delays,'),
        ('인터넷 속도와 관계없이 빠르게 작업할 수 있습니다.',
         'so you get results fast regardless of internet speed.'),
        ('<strong>💸 완전 무료</strong> — 모든 기능을 제한 없이 무료로 사용할 수 있습니다.',
         '<strong>💸 Completely Free</strong> — All features are available for free with no limitations.'),
        ('회원가입, 로그인, 유료 결제가 전혀 필요하지 않습니다.',
         'No sign-up, no login, no payment required.'),
        ('<strong>📱 모든 기기 지원</strong> — PC, 노트북, 태블릿, 스마트폰 등 어떤 기기에서도',
         '<strong>📱 All Devices</strong> — Works on PC, laptop, tablet, and smartphone.'),
        ('사용할 수 있는 반응형 디자인을 지원합니다.',
         'Responsive design ensures a great experience on any screen.'),
        ('<strong>🌐 설치 불필요</strong> — 별도의 소프트웨어를 설치할 필요 없이',
         '<strong>🌐 No Installation</strong> — No software to install.'),
        ('웹 브라우저만 있으면 어디서든 사용할 수 있습니다.',
         'All you need is a web browser, and you can use it anywhere.'),
        ('<h2>이용 방법</h2>', '<h2>How to Use</h2>'),
        ('<p>모든 도구는 동일한 방식으로 사용할 수 있습니다:</p>',
         '<p>All tools work the same simple way:</p>'),
        ('<strong>1단계</strong> — 원하는 도구를 선택합니다', '<strong>Step 1</strong> — Choose the tool you need'),
        ('<strong>2단계</strong> — PDF 또는 이미지 파일을 드래그하거나 버튼으로 선택합니다',
         '<strong>Step 2</strong> — Drag & drop your PDF or image file, or click to select'),
        ('<strong>3단계</strong> — 변환 옵션을 설정합니다 (선택사항)',
         '<strong>Step 3</strong> — Set conversion options (optional)'),
        ('<strong>4단계</strong> — 변환/처리 버튼을 클릭합니다',
         '<strong>Step 4</strong> — Click the Convert / Process button'),
        ('<strong>5단계</strong> — 완료된 파일을 다운로드합니다',
         '<strong>Step 5</strong> — Download the finished file'),
        ('<h2>기술 정보</h2>', '<h2>Technical Info</h2>'),
        ('WooaPDF은 최신 웹 기술을 활용하여 구현되었습니다.',
         'WooaPDF is built with modern web technologies.'),
        ('<strong>PDF.js</strong>(Mozilla 오픈소스)를 통해 PDF를 이미지로 렌더링하고,',
         '<strong>PDF.js</strong> (Mozilla open source) renders PDFs as images,'),
        ('<strong>pdf-lib</strong>를 통해 PDF 편집 기능을 제공합니다.',
         'and <strong>pdf-lib</strong> powers PDF editing features.'),
        ('모든 처리는 클라이언트 사이드(브라우저)에서 이루어지며, 어떠한 파일도 서버로 전송되지 않습니다.',
         'All processing is client-side (in the browser) — no files are ever sent to a server.'),
        ('지원 브라우저: Chrome, Edge, Firefox, Safari (최신 버전 권장)',
         'Supported browsers: Chrome, Edge, Firefox, Safari (latest version recommended)'),
        ('<h2>문의</h2>', '<h2>Contact</h2>'),
        ('서비스 이용 중 문제가 발생하거나 개선 제안이 있으시면 언제든지 연락해 주세요.',
         'If you experience any issues or have suggestions for improvement, feel free to reach out.'),
        ('더 나은 서비스를 만들기 위해 사용자 여러분의 의견을 소중히 여깁니다.',
         'We value your feedback and are always working to improve the service.'),
    ]
    PRIVACY_EXTRA = [
        ('<title>개인정보처리방침 | WooaPDF</title>', '<title>Privacy Policy | WooaPDF</title>'),
        ('<meta name="description" content="WooaPDF의 개인정보처리방침입니다. 파일은 서버에 저장되지 않으며 사용자의 개인정보를 수집하지 않습니다.">', '<meta name="description" content="WooaPDF Privacy Policy. Files are never uploaded to servers. We do not collect personal information.">'),
        ('<h1 style="font-size:1.8rem;">개인정보처리방침</h1>', '<h1 style="font-size:1.8rem;">Privacy Policy</h1>'),
        # Privacy page body content
        ('✅ 시행일: 2024년 1월 1일 &nbsp;|&nbsp; 최종 수정일: 2024년 1월 1일',
         '✅ Effective: January 1, 2024 &nbsp;|&nbsp; Last updated: January 1, 2024'),
        ('WooaPDF(이하 "당사" 또는 "서비스")은 사용자의 Privacy Protected를 매우 중요하게 생각합니다.',
         'WooaPDF ("we" or "the Service") takes your privacy seriously.'),
        ('본 개인정보처리방침은 당사가 제공하는 서비스를 이용하는 과정에서 수집되는 정보와',
         'This Privacy Policy explains what information is collected when you use our service'),
        ('그 처리 방법에 대해 안내합니다.', 'and how it is handled.'),
        ('<h2>1. 수집하는 정보</h2>', '<h2>1. Information We Collect</h2>'),
        ('<h3>1-1. 파일 정보 (서버 미전송)</h3>', '<h3>1-1. File Data (Never Sent to Server)</h3>'),
        ('<strong>WooaPDF에서 처리하는 모든 파일은 사용자의 브라우저(컴퓨터)에서만 처리됩니다.</strong>',
         '<strong>All files processed by WooaPDF are handled entirely within your browser (computer).</strong>'),
        ('업로드하신 PDF 파일, 이미지 파일 등 어떠한 파일도 당사 서버로 전송되거나 저장되지 않습니다.',
         'No PDF, image, or other file you upload is ever sent to or stored on our servers.'),
        ('파일 처리가 완료되거나 브라우저를 닫으면 모든 데이터는 즉시 삭제됩니다.',
         'All data is immediately discarded when processing is complete or the browser is closed.'),
        ('<h3>1-2. 자동 수집 정보</h3>', '<h3>1-2. Automatically Collected Information</h3>'),
        ('<p>서비스 개선 및 통계 목적으로 다음 정보가 자동으로 수집될 수 있습니다:</p>',
         '<p>The following information may be collected automatically for service improvement and analytics:</p>'),
        ('<li>접속 IP 주소 (익명 처리됨)</li>', '<li>IP address (anonymized)</li>'),
        ('<li>브라우저 종류 및 버전</li>', '<li>Browser type and version</li>'),
        ('<li>방문한 pages, 접속 시간</li>', '<li>Pages visited and access time</li>'),
        ('<li>운영체제 정보</li>', '<li>Operating system information</li>'),
        ('<li>유입 경로 (검색어, 이전 방문 사이트)</li>', '<li>Referral source (search terms, referring site)</li>'),
        ('<p>이 정보는 개인을 식별하는 데 사용되지 않으며, 서비스 개선을 위한 통계 분석에만 활용됩니다.</p>',
         '<p>This information is not used to identify individuals and is used only for statistical analysis to improve the service.</p>'),
        ('<h2>2. 쿠키 및 광고</h2>', '<h2>2. Cookies &amp; Advertising</h2>'),
        ('<h3>2-1. 쿠키</h3>', '<h3>2-1. Cookies</h3>'),
        ('당사는 서비스 편의성 향상을 위해 쿠키를 사용할 수 있습니다.',
         'We may use cookies to improve your experience with the service.'),
        ('쿠키는 사용자 설정(예: 최근 사용한 옵션)을 저장하는 데 사용되며,',
         'Cookies store user preferences (e.g. recently used options)'),
        ('브라우저 설정에서 쿠키 사용을 거부할 수 있습니다.',
         'and can be disabled in your browser settings.'),
        ('<h3>2-2. Google 애드센스</h3>', '<h3>2-2. Google AdSense</h3>'),
        ('당사는 서비스 운영 비용 충당을 위해 Google 애드센스를 통한 광고를 표시할 수 있습니다.',
         'We may display ads through Google AdSense to cover the cost of running the service.'),
        ('Google은 사용자의 관심사에 맞는 광고를 제공하기 위해 쿠키를 사용할 수 있습니다.',
         'Google may use cookies to show ads relevant to your interests.'),
        ('Google의 광고 쿠키 사용에 대한 자세한 내용은',
         'For more information about Google\'s use of advertising cookies, see'),
        ('>Google 광고 정책</a>에서 확인하실 수 있습니다.',
         '>Google Ads Policy</a>.'),
        ('<h3>2-3. Google 애널리틱스</h3>', '<h3>2-3. Google Analytics</h3>'),
        ('당사는 방문자 통계 분석을 위해 Google 애널리틱스를 사용할 수 있습니다.',
         'We may use Google Analytics to analyze visitor statistics.'),
        ('수집된 데이터는 익명화 처리되어 개인을 식별하는 데 사용되지 않습니다.',
         'Collected data is anonymized and not used to identify individuals.'),
        ('<h2>3. 개인정보의 이용 목적</h2>', '<h2>3. Purpose of Data Use</h2>'),
        ('<p>수집된 정보는 다음 목적으로만 사용됩니다:</p>',
         '<p>Collected information is used only for the following purposes:</p>'),
        ('<li>서비스 제공 및 개선</li>', '<li>Providing and improving the service</li>'),
        ('<li>서비스 이용 통계 분석</li>', '<li>Statistical analysis of service usage</li>'),
        ('<li>기술적 문제 해결</li>', '<li>Troubleshooting technical issues</li>'),
        ('<li>서비스 보안 및 악용 방지</li>', '<li>Service security and abuse prevention</li>'),
        ('<h2>4. 개인정보의 제3자 제공</h2>', '<h2>4. Sharing with Third Parties</h2>'),
        ('당사는 다음의 경우를 제외하고 사용자의 개인정보를 제3자에게 제공하지 않습니다:',
         'We do not share personal information with third parties except in the following cases:'),
        ('<li>사용자의 명시적 동의가 있는 경우</li>', '<li>With explicit user consent</li>'),
        ('<li>법령에 의하거나 수사기관의 요청이 있는 경우</li>',
         '<li>As required by law or requested by law enforcement</li>'),
        ('<li>서비스 제공을 위해 필요한 외부 서비스 사용 시 (Google 등, 익명 처리된 통계 데이터에 한함)</li>',
         '<li>When using external services necessary for operation (e.g. Google, limited to anonymized statistical data)</li>'),
        ('<h2>5. Privacy Protected 조치</h2>', '<h2>5. Privacy Protection Measures</h2>'),
        ('<li>모든 파일 처리는 사용자 브라우저 내에서만 이루어집니다</li>',
         '<li>All file processing happens only within your browser</li>'),
        ('<li>HTTPS를 통한 암호화 통신을 사용합니다</li>',
         '<li>Encrypted communication via HTTPS</li>'),
        ('<li>불필요한 개인정보를 수집하지 않습니다</li>',
         '<li>We do not collect unnecessary personal information</li>'),
        ('<li>수집된 통계 데이터는 익명화하여 보관합니다</li>',
         '<li>Statistical data is anonymized before storage</li>'),
        ('<h2>6. 사용자의 권리</h2>', '<h2>6. Your Rights</h2>'),
        ('<p>사용자는 언제든지 다음 권리를 행사할 수 있습니다:</p>',
         '<p>You may exercise the following rights at any time:</p>'),
        ('<li>개인정보 수집 및 이용에 대한 동의 철회</li>',
         '<li>Withdraw consent for data collection and use</li>'),
        ('<li>쿠키 사용 거부 (브라우저 설정에서 가능)</li>',
         '<li>Refuse cookies (via browser settings)</li>'),
        ('<li>개인정보 처리 관련 문의 및 이의 제기</li>',
         '<li>Submit inquiries or objections regarding data handling</li>'),
        ('<h2>7. 아동의 Privacy Protected</h2>', '<h2>7. Children\'s Privacy</h2>'),
        ('당사의 서비스는 만 14세 미만 아동을 대상으로 하지 않습니다.',
         'Our service is not directed at children under 14 years of age.'),
        ('만 14세 미만 아동의 개인정보를 의도적으로 수집하지 않습니다.',
         'We do not intentionally collect personal information from children under 14.'),
        ('<h2>8. 개인정보처리방침의 변경</h2>', '<h2>8. Changes to This Policy</h2>'),
        ('본 개인정보처리방침은 법령 또는 서비스 변경에 따라 수정될 수 있습니다.',
         'This Privacy Policy may be updated in response to legal or service changes.'),
        ('변경 시 본 pages를 통해 공지하며, 중요한 변경 사항은 서비스 내 공지를 통해 안내합니다.',
         'Updates will be posted on this page. Significant changes will be announced within the service.'),
        ('<h2>9. 문의</h2>', '<h2>9. Contact</h2>'),
        ('개인정보 처리에 관한 문의 사항이 있으시면 아래로 연락해 주세요.<br>',
         'If you have any questions about this Privacy Policy, please contact us:<br>'),
        ('서비스명: WooaPDF (WooaPDF)<br>', 'Service: WooaPDF<br>'),
        ('이메일 문의는 서비스 내 문의 기능을 통해 주시기 바랍니다.',
         'Contact: linker@wooahouse.com'),
    ]
    for f in ['about.html', 'privacy.html']:
        src = os.path.join(BASE, f)
        dst = os.path.join(EN_DIR, f)
        if os.path.exists(src):
            with open(src, encoding='utf-8') as fp:
                html = fp.read()
            for ko, en in COMMON:
                html = html.replace(ko, en)
            html = html.replace('<html lang="ko">', '<html lang="en">')
            html = html.replace('content="ko_KR"', 'content="en_US"')
            extras = ABOUT_EXTRA if f == 'about.html' else PRIVACY_EXTRA
            for ko, en in extras:
                html = html.replace(ko, en)
            # canonical & og:url
            html = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://pdfkit.wooahouse.com/en/{f}"', html)
            html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://pdfkit.wooahouse.com/en/{f}"', html)
            # lang switcher CSS
            if 'lang-switcher' not in html:
                html = html.replace('  </style>', LANG_SWITCHER_CSS + '  </style>', 1)
            # lang switcher HTML
            ko_link = f'../{f}'
            sw_html = (
                f'    <div class="header-right">\n'
                f'      <div class="lang-switcher">\n'
                f'        <a href="{ko_link}">KO</a>\n'
                f'        <span>|</span>\n'
                f'        <a href="{f}" class="active">EN</a>\n'
                f'      </div>\n'
            )
            if 'lang-switcher' not in html:
                html = html.replace('    <div class="header-right">', sw_html, 1)
            # 쿠팡 완전 제거
            html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
            html = re.sub(r'<!-- Coupang Partners -->\s*<div[^>]*>.*?</div>', '', html, flags=re.DOTALL)
            html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)
            html = re.sub(r'<p class="coupang-notice">[^<]*</p>', '', html)
            with open(dst, 'w', encoding='utf-8') as fp:
                fp.write(html)
            print(f'  ✅ en/{f}')

    print(f'\nDone! {len(PAGE_META) + 2} files generated in en/')
