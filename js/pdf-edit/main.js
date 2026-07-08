/**
 * main.js
 * ─────────────────────────────────────────
 * pdf-edit.html 페이지의 전체 흐름을 엮는 진입점.
 * 업로드 → 렌더링 → 도구 바 연결 → 속성 패널 연결 → 다운로드/내보내기까지
 * 각 모듈(PdfRenderer, PdfEditState, ElementFactory, Toolbar, ExportManager)을
 * 순서대로 초기화하고 이벤트를 연결한다.
 */

(() => {
  pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

  let originalArrayBuffer = null;
  let selectedFile = null;
  let hasUnsavedWork = false;

  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const editorWrap = document.getElementById('editorWrap');
  const pagesContainer = document.getElementById('pagesContainer');
  const toolBtns = document.getElementById('toolButtons');
  const propPanel = document.getElementById('propPanel');
  const undoBtn = document.getElementById('undoBtn');
  const redoBtn = document.getElementById('redoBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const errorMsg = document.getElementById('errorMsg');

  // ── 파일 업로드 ─────────────────────────
  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault(); dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', e => {
    if (e.target.files[0]) loadFile(e.target.files[0]);
  });

  async function loadFile(file) {
    if (!file.name.toLowerCase().endsWith('.pdf') && file.type !== 'application/pdf') {
      showError('PDF 파일만 업로드할 수 있습니다.');
      return;
    }
    hideError();
    selectedFile = file;
    originalArrayBuffer = await file.arrayBuffer();

    let numPages;
    try {
      numPages = await PdfRenderer.load(originalArrayBuffer.slice(0));
    } catch (e) {
      showError('PDF를 읽을 수 없습니다: ' + e.message);
      return;
    }

    PdfEditState.init(numPages);
    dropZone.style.display = 'none';
    editorWrap.style.display = 'flex';

    PdfRenderer.mount(pagesContainer, numPages, (pageIndex, wrap, overlay) => {
      // 이미 저장돼 있던 요소가 있으면(다른 페이지 편집 후 되돌아온 경우) 다시 그려준다
      const page = PdfEditState.getPage(pageIndex);
      page.elements.forEach(data => ElementFactory.render(overlay, pageIndex, data));
      Toolbar.attachOverlay(overlay, pageIndex, () => { hasUnsavedWork = true; updateHistoryButtons(); });
    });

    applyFitScale();
    updateHistoryButtons();
  }

  // ── 도구 바 ─────────────────────────
  toolBtns.querySelectorAll('.pe-tool-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      Toolbar.setTool(btn.dataset.tool, toolBtns);
      ElementFactory.deselectAll();
      propPanel.style.display = 'none';
    });
  });
  Toolbar.setTool('select', toolBtns);

  // ── 속성 패널 (요소 선택 시에만 표시) ─────────────────────────
  ElementFactory.setOnSelectionChange((data) => {
    if (!data) { propPanel.style.display = 'none'; return; }
    renderPropPanel(data);
  });

  function renderPropPanel(data) {
    propPanel.style.display = 'block';
    if (data.type === 'text') {
      propPanel.innerHTML = `
        <label>글자 크기 <input type="range" id="pf-size" min="10" max="72" value="${data.fontSize}"></label>
        <label>색상 <input type="color" id="pf-color" value="${data.color}"></label>
        <label>폰트 <select id="pf-font">
          <option value="Helvetica" ${data.fontFamily === 'Helvetica' ? 'selected' : ''}>Helvetica</option>
          <option value="TimesRoman" ${data.fontFamily === 'TimesRoman' ? 'selected' : ''}>Times</option>
          <option value="Courier" ${data.fontFamily === 'Courier' ? 'selected' : ''}>Courier</option>
        </select></label>
        <label class="pe-bold-row"><input type="checkbox" id="pf-bold" ${data.bold ? 'checked' : ''}> 굵게</label>`;
      byId('pf-size').addEventListener('input', e => ElementFactory.updateStyle(data, { fontSize: +e.target.value }));
      byId('pf-color').addEventListener('input', e => ElementFactory.updateStyle(data, { color: e.target.value }));
      byId('pf-font').addEventListener('change', e => ElementFactory.updateStyle(data, { fontFamily: e.target.value }));
      byId('pf-bold').addEventListener('change', e => ElementFactory.updateStyle(data, { bold: e.target.checked }));
    } else if (data.type !== 'image' && data.type !== 'whiteout') {
      propPanel.innerHTML = `
        <label>선 색상 <input type="color" id="pf-color" value="${data.color}"></label>
        <label>선 굵기 <input type="range" id="pf-width" min="1" max="20" value="${data.strokeWidth}"></label>`;
      byId('pf-color').addEventListener('input', e => ElementFactory.updateStyle(data, { color: e.target.value }));
      byId('pf-width').addEventListener('input', e => ElementFactory.updateStyle(data, { strokeWidth: +e.target.value }));
    } else {
      propPanel.innerHTML = `<p class="pe-prop-hint">선택한 요소를 드래그해 이동하거나 모서리를 잡아 크기를 조절하세요.</p>`;
    }
  }

  function byId(id) { return document.getElementById(id); }

  // ── Undo / Redo ─────────────────────────
  undoBtn.addEventListener('click', () => { if (PdfEditState.undo()) { redrawAllPages(); updateHistoryButtons(); } });
  redoBtn.addEventListener('click', () => { if (PdfEditState.redo()) { redrawAllPages(); updateHistoryButtons(); } });

  document.addEventListener('keydown', (e) => {
    const ctrlOrCmd = e.ctrlKey || e.metaKey;
    if (ctrlOrCmd && e.key.toLowerCase() === 'z' && !e.shiftKey) { e.preventDefault(); undoBtn.click(); }
    if (ctrlOrCmd && (e.key.toLowerCase() === 'y' || (e.shiftKey && e.key.toLowerCase() === 'z'))) { e.preventDefault(); redoBtn.click(); }
  });

  function redrawAllPages() {
    document.querySelectorAll('.pe-overlay').forEach(overlay => overlay.innerHTML = '');
    PdfEditState.getAllPages().forEach((page, pageIndex) => {
      const overlay = pagesContainer.querySelector(`.pe-page-wrap[data-page-index="${pageIndex}"] .pe-overlay`);
      if (!overlay) return; // 아직 렌더 안 된(화면 밖) 페이지는 다음에 보일 때 자동 반영됨
      page.elements.forEach(data => ElementFactory.render(overlay, pageIndex, data));
    });
    ElementFactory.deselectAll();
    propPanel.style.display = 'none';
  }

  function updateHistoryButtons() {
    undoBtn.disabled = !PdfEditState.canUndo();
    redoBtn.disabled = !PdfEditState.canRedo();
  }

  // ── 새로고침 경고 ─────────────────────────
  window.addEventListener('beforeunload', (e) => {
    if (hasUnsavedWork) { e.preventDefault(); e.returnValue = ''; }
  });

  // ── 다운로드(내보내기) ─────────────────────────
  downloadBtn.addEventListener('click', async () => {
    if (!originalArrayBuffer) return;
    downloadBtn.disabled = true;
    const origText = downloadBtn.textContent;
    downloadBtn.textContent = '⏳ PDF 생성 중...';
    document.getElementById('progressWrap').style.display = 'block';
    updateProgress(5, 'PDF 불러오는 중...');

    try {
      const bytes = await ExportManager.exportPdf(
        originalArrayBuffer.slice(0),
        PdfEditState.getAllPages(),
        PdfRenderer.getScale(),
        (pct) => updateProgress(pct, '요소 삽입 중...')
      );
      updateProgress(100, '완료!');
      document.getElementById('progressWrap').style.display = 'none';

      const blob = new Blob([bytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (selectedFile ? selectedFile.name.replace(/\.pdf$/i, '') : 'document') + '_edited.pdf';
      a.click();
      URL.revokeObjectURL(url);
      hasUnsavedWork = false;
    } catch (err) {
      console.error(err);
      showError('내보내기 중 오류가 발생했습니다: ' + err.message);
      document.getElementById('progressWrap').style.display = 'none';
    }
    downloadBtn.disabled = false;
    downloadBtn.textContent = origText;
  });

  function updateProgress(pct, text) {
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = text;
    document.getElementById('progressPct').textContent = pct + '%';
  }

  function showError(msg) { errorMsg.textContent = msg; errorMsg.style.display = 'block'; }
  function hideError() { errorMsg.style.display = 'none'; }

  // ── 화면 너비에 맞춰 페이지를 축소 표시 (좌표계는 원본 픽셀 그대로 유지) ──
  // CSS zoom은 표시 크기와 함께 클릭 좌표(getBoundingClientRect)도 같이
  // 축소해주므로, 오버레이 좌표 계산 코드를 스케일별로 따로 분기할 필요가 없다.
  function applyFitScale() {
    const wraps = pagesContainer.querySelectorAll('.pe-page-wrap');
    if (!wraps.length) return;
    const containerWidth = pagesContainer.clientWidth - 24; // 좌우 여백 감안
    let maxPageWidth = 0;
    for (let i = 0; i < PdfRenderer.getNumPages(); i++) {
      maxPageWidth = Math.max(maxPageWidth, PdfRenderer.getPageSize(i).width);
    }
    const fitScale = Math.min(1, containerWidth / maxPageWidth);
    wraps.forEach(w => { w.style.zoom = fitScale; });
  }

  window.addEventListener('resize', () => { if (originalArrayBuffer) applyFitScale(); });
})();
