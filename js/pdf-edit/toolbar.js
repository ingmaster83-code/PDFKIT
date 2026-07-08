/**
 * toolbar.js
 * ─────────────────────────────────────────
 * 좌측 도구 아이콘 바의 도구 선택 상태를 관리하고,
 * 현재 선택된 도구에 따라 PDF 오버레이 위 클릭/드래그 동작을
 * "새 요소 생성"으로 연결한다.
 *
 * - text, image : 클릭 한 번으로 기본 크기의 요소 생성 (이미지는 파일 선택 후)
 * - rect, circle, line, arrow, whiteout : 드래그로 시작점~끝점 지정해 생성
 * - select : 아무것도 새로 만들지 않고 기존 요소 선택/이동만 가능
 */

const Toolbar = (() => {
  let currentTool = 'select';
  let defaultStyle = {
    fontSize: 20, color: '#111111', bold: false, fontFamily: 'Helvetica',
    strokeWidth: 3, shapeColor: '#EF4444',
  };

  function getTool() { return currentTool; }
  function getDefaultStyle() { return defaultStyle; }

  function setTool(tool, buttonsContainer) {
    currentTool = tool;
    if (buttonsContainer) {
      buttonsContainer.querySelectorAll('.pe-tool-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.tool === tool);
      });
    }
    document.querySelectorAll('.pe-page-wrap').forEach(w => {
      w.style.cursor = (tool === 'select') ? 'default' : 'crosshair';
    });
  }

  /**
   * overlay 위에서의 클릭/드래그를 감지해 현재 도구에 맞는 새 요소를 만든다.
   * pageIndex를 알고 있어야 state에 반영 가능하므로 mount 시점에 바인딩한다.
   */
  function attachOverlay(overlayEl, pageIndex, onCreated) {
    overlayEl.addEventListener('pointerdown', (e) => {
      if (e.target !== overlayEl) return; // 기존 요소 위 클릭은 여기서 처리 안 함
      if (currentTool === 'select') { ElementFactory.deselectAll(); return; }

      const rect = overlayEl.getBoundingClientRect();
      const startX = e.clientX - rect.left;
      const startY = e.clientY - rect.top;

      if (currentTool === 'text') {
        createTextAt(overlayEl, pageIndex, startX, startY, onCreated);
        return;
      }
      if (currentTool === 'image') {
        pickImageAt(overlayEl, pageIndex, startX, startY, onCreated);
        return;
      }

      // 드래그로 그리는 도구들 (rect/circle/line/arrow/whiteout)
      let curX = startX, curY = startY;
      const ghost = document.createElement('div');
      ghost.className = 'pe-drag-ghost';
      overlayEl.appendChild(ghost);
      updateGhost();

      function updateGhost() {
        const x = Math.min(startX, curX), y = Math.min(startY, curY);
        const w = Math.abs(curX - startX), h = Math.abs(curY - startY);
        ghost.style.left = x + 'px'; ghost.style.top = y + 'px';
        ghost.style.width = w + 'px'; ghost.style.height = h + 'px';
      }
      function onMove(ev) {
        curX = ev.clientX - rect.left;
        curY = ev.clientY - rect.top;
        updateGhost();
      }
      function onUp() {
        document.removeEventListener('pointermove', onMove);
        document.removeEventListener('pointerup', onUp);
        ghost.remove();
        const x = Math.min(startX, curX), y = Math.min(startY, curY);
        const w = Math.max(Math.abs(curX - startX), 20);
        const h = Math.max(Math.abs(curY - startY), 20);
        createShapeAt(overlayEl, pageIndex, currentTool, x, y, w, h, onCreated);
      }
      document.addEventListener('pointermove', onMove);
      document.addEventListener('pointerup', onUp);
    });
  }

  function createTextAt(overlayEl, pageIndex, x, y, onCreated) {
    const data = {
      type: 'text', x, y, w: 220, h: 40,
      text: '텍스트를 입력하세요',
      fontSize: defaultStyle.fontSize,
      color: defaultStyle.color,
      bold: defaultStyle.bold,
      fontFamily: defaultStyle.fontFamily,
    };
    PdfEditState.addElement(pageIndex, data);
    PdfEditState.commit();
    const el = ElementFactory.render(overlayEl, pageIndex, data);
    onCreated && onCreated(data, el);
    // 생성 즉시 편집 포커스
    const content = el.querySelector('.pe-text-content');
    if (content) {
      requestAnimationFrame(() => {
        content.focus();
        document.execCommand && selectAllText(content);
      });
    }
  }

  function selectAllText(el) {
    const range = document.createRange();
    range.selectNodeContents(el);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function pickImageAt(overlayEl, pageIndex, x, y, onCreated) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/png,image/jpeg';
    input.onchange = () => {
      const file = input.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        const img = new Image();
        img.onload = () => {
          const maxW = 220;
          const scale = Math.min(1, maxW / img.width);
          const data = {
            type: 'image', x, y,
            w: img.width * scale, h: img.height * scale,
            src: reader.result,
            mime: file.type,
          };
          PdfEditState.addElement(pageIndex, data);
          PdfEditState.commit();
          const el = ElementFactory.render(overlayEl, pageIndex, data);
          onCreated && onCreated(data, el);
        };
        img.src = reader.result;
      };
      reader.readAsDataURL(file);
    };
    input.click();
  }

  function createShapeAt(overlayEl, pageIndex, type, x, y, w, h, onCreated) {
    const data = {
      type, x, y, w, h,
      color: type === 'whiteout' ? '#FFFFFF' : defaultStyle.shapeColor,
      strokeWidth: defaultStyle.strokeWidth,
    };
    PdfEditState.addElement(pageIndex, data);
    PdfEditState.commit();
    const el = ElementFactory.render(overlayEl, pageIndex, data);
    onCreated && onCreated(data, el);
  }

  return { getTool, setTool, getDefaultStyle, attachOverlay };
})();
