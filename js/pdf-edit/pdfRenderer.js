/**
 * pdfRenderer.js
 * ─────────────────────────────────────────
 * PDF.js를 이용해 업로드된 PDF의 각 페이지를 <canvas>에 렌더링한다.
 * 대용량 PDF(50페이지 이상) 대응을 위해, 화면에 보이는 페이지 근처만
 * 실제로 렌더링하고 나머지는 자리表시(placeholder)만 만들어두는
 * lazy-loading(IntersectionObserver) 방식을 사용한다.
 */

const PdfRenderer = (() => {
  const RENDER_SCALE = 1.5; // PDF 포인트 → 캔버스 픽셀 배율

  let pdfDoc = null;        // pdfjsLib document
  let pageViewports = [];   // 페이지별 { width, height } (렌더 스케일 적용된 px 기준)
  let renderedPages = new Set();
  let container = null;
  let onPageReady = null;   // (pageIndex, pageWrapEl) => void  콜백

  function getScale() { return RENDER_SCALE; }

  async function load(arrayBuffer) {
    pdfDoc = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    pageViewports = [];
    renderedPages = new Set();
    for (let i = 1; i <= pdfDoc.numPages; i++) {
      const page = await pdfDoc.getPage(i);
      const vp = page.getViewport({ scale: RENDER_SCALE });
      pageViewports.push({ width: vp.width, height: vp.height });
    }
    return pdfDoc.numPages;
  }

  function getPageSize(pageIndex) {
    return pageViewports[pageIndex];
  }

  /**
   * 컨테이너 안에 페이지 수만큼 빈 wrap div를 만들고,
   * IntersectionObserver로 화면 근처에 들어온 페이지만 실제 렌더링한다.
   */
  function mount(containerEl, pageCount, readyCallback) {
    container = containerEl;
    onPageReady = readyCallback;
    container.innerHTML = '';

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const idx = parseInt(entry.target.dataset.pageIndex, 10);
          renderPage(idx);
        }
      });
    }, { root: container, rootMargin: '800px 0px' }); // 근처 800px까지 미리 렌더

    for (let i = 0; i < pageCount; i++) {
      const size = pageViewports[i];
      const wrap = document.createElement('div');
      wrap.className = 'pe-page-wrap';
      wrap.dataset.pageIndex = String(i);
      wrap.style.width = size.width + 'px';
      wrap.style.height = size.height + 'px';

      const placeholder = document.createElement('div');
      placeholder.className = 'pe-page-placeholder';
      placeholder.textContent = `${i + 1} 페이지`;
      wrap.appendChild(placeholder);

      container.appendChild(wrap);
      observer.observe(wrap);
    }
  }

  async function renderPage(pageIndex) {
    if (renderedPages.has(pageIndex)) return;
    renderedPages.add(pageIndex);

    const wrap = container.querySelector(`.pe-page-wrap[data-page-index="${pageIndex}"]`);
    if (!wrap) return;

    const page = await pdfDoc.getPage(pageIndex + 1);
    const viewport = page.getViewport({ scale: RENDER_SCALE });

    const canvas = document.createElement('canvas');
    canvas.className = 'pe-page-canvas';
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    const ctx = canvas.getContext('2d');
    await page.render({ canvasContext: ctx, viewport }).promise;

    const placeholder = wrap.querySelector('.pe-page-placeholder');
    if (placeholder) placeholder.remove();
    wrap.prepend(canvas);

    // overlay 레이어(요소들이 배치되는 곳)를 항상 canvas 위에 유지
    let overlay = wrap.querySelector('.pe-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'pe-overlay';
      wrap.appendChild(overlay);
    }

    if (onPageReady) onPageReady(pageIndex, wrap, overlay);
  }

  function getNumPages() {
    return pdfDoc ? pdfDoc.numPages : 0;
  }

  return { load, mount, getPageSize, getScale, getNumPages };
})();
