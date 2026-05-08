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
    html = re.sub(r'"name": "[^"]*변환기[^"]*"', f'"name": "{meta["app_name"]}"', html)
    html = re.sub(r'"name": "[^"]*기[^"]*"', f'"name": "{meta["app_name"]}"', html)
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
        html = re.sub(r'<h2[^>]*>자주 묻는 질문</h2>', '<h2 style="font-size:1.4rem;margin-bottom:1.5rem;">Frequently Asked Questions</h2>', html)
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
    # Replace closing </header> section
    html = re.sub(
        r'(\s*</div>\s*</header>)',
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>',
        html, count=1
    )

    # ── Coupang g.js를 head로 (tool pages에서는 body 안에 있는 경우) ──
    # Remove inline g.js from body if present (already in head of ko version or add it)
    if 'src="https://ads-partners.coupang.com/g.js"' not in html.split('</head>')[0]:
        html = html.replace('</head>', '<script src="https://ads-partners.coupang.com/g.js"></script>\n</head>', 1)

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
    ]
    PRIVACY_EXTRA = [
        ('<title>개인정보처리방침 | WooaPDF</title>', '<title>Privacy Policy | WooaPDF</title>'),
        ('<meta name="description" content="WooaPDF의 개인정보처리방침입니다. 파일은 서버에 저장되지 않으며 사용자의 개인정보를 수집하지 않습니다.">', '<meta name="description" content="WooaPDF Privacy Policy. Files are never uploaded to servers. We do not collect personal information.">'),
        ('<h1 style="font-size:1.8rem;">개인정보처리방침</h1>', '<h1 style="font-size:1.8rem;">Privacy Policy</h1>'),
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
            with open(dst, 'w', encoding='utf-8') as fp:
                fp.write(html)
            print(f'  ✅ en/{f}')

    print(f'\nDone! {len(PAGE_META) + 2} files generated in en/')
