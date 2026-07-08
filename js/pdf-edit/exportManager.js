/**
 * exportManager.js
 * ─────────────────────────────────────────
 * state.js에 저장된 편집 요소들을, 렌더링 캔버스 좌표계에서
 * 실제 PDF 포인트 좌표계로 변환하여 pdf-lib으로 원본 PDF에 그려 넣는다.
 *
 * 좌표 변환 규칙:
 *   - 렌더 캔버스는 PDF 포인트 × RENDER_SCALE 크기로 그려졌으므로,
 *     pdfX = domX / RENDER_SCALE
 *   - PDF는 좌하단이 원점이고 브라우저는 좌상단이 원점이므로 Y축을 뒤집는다.
 *     pdfY = pageHeightPt - (domY / RENDER_SCALE) - (domH / RENDER_SCALE)
 */

const ExportManager = (() => {
  const { PDFDocument, rgb, StandardFonts } = PDFLib;

  function hexToRgb01(hex) {
    const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex || '#000000');
    if (!m) return rgb(0, 0, 0);
    return rgb(parseInt(m[1], 16) / 255, parseInt(m[2], 16) / 255, parseInt(m[3], 16) / 255);
  }

  function fontForFamily(pdfDoc, family, bold) {
    const map = {
      Helvetica: bold ? StandardFonts.HelveticaBold : StandardFonts.Helvetica,
      TimesRoman: bold ? StandardFonts.TimesRomanBold : StandardFonts.TimesRoman,
      Courier: bold ? StandardFonts.CourierBold : StandardFonts.Courier,
    };
    return pdfDoc.embedFont(map[family] || map.Helvetica);
  }

  async function exportPdf(originalArrayBuffer, statePages, renderScale, onProgress) {
    const pdfDoc = await PDFDocument.load(originalArrayBuffer);
    const pdfPages = pdfDoc.getPages();

    // 폰트는 페이지마다 새로 embed하지 않도록 캐시
    const fontCache = {};
    async function getFont(family, bold) {
      const key = family + '_' + bold;
      if (!fontCache[key]) fontCache[key] = await fontForFamily(pdfDoc, family, bold);
      return fontCache[key];
    }

    for (let i = 0; i < statePages.length; i++) {
      const elements = statePages[i].elements;
      if (!elements.length) continue;
      const page = pdfPages[i];
      const { height: pageHeightPt } = page.getSize();

      for (const el of elements) {
        await drawElement(pdfDoc, page, el, renderScale, pageHeightPt, getFont);
      }

      if (onProgress) onProgress(Math.round(((i + 1) / statePages.length) * 80) + 10);
    }

    return pdfDoc.save();
  }

  async function drawElement(pdfDoc, page, el, scale, pageHeightPt, getFont) {
    const x = el.x / scale;
    const w = el.w / scale;
    const h = el.h / scale;
    const y = pageHeightPt - (el.y / scale) - h;

    if (el.type === 'text') {
      const font = await getFont(el.fontFamily, el.bold);
      const size = el.fontSize / scale * 1.0; // 폰트 크기도 같은 배율로 환산
      const lines = String(el.text || '').split('\n');
      let cursorY = y + h - size; // 텍스트 박스 상단에서부터 아래로
      for (const line of lines) {
        page.drawText(line, {
          x, y: Math.max(cursorY, 0),
          size, font,
          color: hexToRgb01(el.color),
        });
        cursorY -= size * 1.25;
      }
      return;
    }

    if (el.type === 'whiteout') {
      page.drawRectangle({ x, y, width: w, height: h, color: rgb(1, 1, 1) });
      return;
    }

    if (el.type === 'rect') {
      page.drawRectangle({
        x, y, width: w, height: h,
        borderColor: hexToRgb01(el.color),
        borderWidth: (el.strokeWidth || 3) / scale,
      });
      return;
    }

    if (el.type === 'circle') {
      page.drawEllipse({
        x: x + w / 2, y: y + h / 2,
        xScale: w / 2, yScale: h / 2,
        borderColor: hexToRgb01(el.color),
        borderWidth: (el.strokeWidth || 3) / scale,
      });
      return;
    }

    if (el.type === 'line' || el.type === 'arrow') {
      // DOM에서 좌상단(0,0)→우하단(w,h) 대각선으로 그렸으므로 PDF 좌표로 양끝점 변환
      const startPdf = { x, y: y + h };
      const endPdf = { x: x + w, y };
      const thickness = (el.strokeWidth || 3) / scale;
      page.drawLine({ start: startPdf, end: endPdf, thickness, color: hexToRgb01(el.color) });
      if (el.type === 'arrow') drawArrowHead(page, startPdf, endPdf, thickness, hexToRgb01(el.color));
      return;
    }

    if (el.type === 'image') {
      const base64 = el.src.split(',')[1];
      const bytes = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
      const image = el.mime === 'image/png' ? await pdfDoc.embedPng(bytes) : await pdfDoc.embedJpg(bytes);
      page.drawImage(image, { x, y, width: w, height: h });
      return;
    }
  }

  function drawArrowHead(page, start, end, thickness, color) {
    const angle = Math.atan2(end.y - start.y, end.x - start.x);
    const headLen = Math.max(10, thickness * 4);
    const spread = Math.PI / 7;
    const p1 = {
      x: end.x - headLen * Math.cos(angle - spread),
      y: end.y - headLen * Math.sin(angle - spread),
    };
    const p2 = {
      x: end.x - headLen * Math.cos(angle + spread),
      y: end.y - headLen * Math.sin(angle + spread),
    };
    page.drawLine({ start: end, end: p1, thickness, color });
    page.drawLine({ start: end, end: p2, thickness, color });
  }

  return { exportPdf };
})();
