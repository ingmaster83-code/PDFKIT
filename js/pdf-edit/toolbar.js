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
  let lastSignature = null; // { src, w, h } — 한 번 그린 서명은 계속 재사용(다시 그리기 전까지)

  function resetSignature() { lastSignature = null; }

  /** elementFactory.js의 동일 함수와 같은 이유로 zoom 배율을 되돌려준다 */
  function getZoom(overlayEl) {
    const wrap = overlayEl.closest('.pe-page-wrap');
    const z = wrap ? parseFloat(wrap.style.zoom) : 1;
    return z > 0 ? z : 1;
  }

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

      // CSS zoom은 오버레이 하위 요소 전체의 px 좌표계를 함께 축소하므로,
      // 화면(screen) 픽셀 delta를 zoom 배율로 나눠 로컬(zoom 적용 전) px로 변환해야
      // ghost/실제 요소가 클릭 지점과 어긋나지 않는다.
      const rect = overlayEl.getBoundingClientRect();
      const zoom = getZoom(overlayEl);
      const startX = (e.clientX - rect.left) / zoom;
      const startY = (e.clientY - rect.top) / zoom;

      if (currentTool === 'text') {
        createTextAt(overlayEl, pageIndex, startX, startY, onCreated);
        return;
      }
      if (currentTool === 'image') {
        pickImageAt(overlayEl, pageIndex, startX, startY, onCreated);
        return;
      }
      if (currentTool === 'stamp') {
        PdfEditModals.openStampPicker((dataUri, w, h) => {
          placeRasterAt(overlayEl, pageIndex, 'stamp', dataUri, startX, startY, w, h, onCreated);
        });
        return;
      }
      if (currentTool === 'signature') {
        if (lastSignature) {
          placeRasterAt(overlayEl, pageIndex, 'signature', lastSignature.src, startX, startY, lastSignature.w, lastSignature.h, onCreated);
        } else {
          PdfEditModals.openSignaturePad((dataUri, w, h) => {
            lastSignature = { src: dataUri, w, h };
            placeRasterAt(overlayEl, pageIndex, 'signature', dataUri, startX, startY, w, h, onCreated);
          });
        }
        return;
      }
      if (currentTool === 'freehand') {
        startFreehand(e, overlayEl, pageIndex, rect, startX, startY, onCreated);
        return;
      }

      // 드래그로 그리는 도구들 (rect/circle/line/arrow/whiteout/highlight/link)
      let curX = startX, curY = startY;
      const isLineTool = currentTool === 'line' || currentTool === 'arrow';
      // 선/화살표는 박스 모양 미리보기 대신, 실제 드래그 경로를 그대로 보여주는
      // SVG 선 미리보기를 사용한다 (그렇지 않으면 "선을 그려도 네모만 보인다"는 혼란이 생김).
      let ghost, ghostLine;
      if (isLineTool) {
        const svgNs = 'http://www.w3.org/2000/svg';
        ghost = document.createElementNS(svgNs, 'svg');
        ghost.setAttribute('class', 'pe-drag-ghost pe-drag-ghost-line');
        ghost.style.position = 'absolute'; ghost.style.left = '0'; ghost.style.top = '0';
        ghost.style.width = '100%'; ghost.style.height = '100%'; ghost.style.pointerEvents = 'none';
        ghost.style.border = 'none'; ghost.style.background = 'none';
        ghostLine = document.createElementNS(svgNs, 'line');
        ghostLine.setAttribute('stroke', defaultStyle.shapeColor);
        ghostLine.setAttribute('stroke-width', String(defaultStyle.strokeWidth));
        ghostLine.setAttribute('stroke-linecap', 'round');
        ghost.appendChild(ghostLine);
      } else {
        ghost = document.createElement('div');
        ghost.className = 'pe-drag-ghost';
      }
      overlayEl.appendChild(ghost);
      updateGhost();

      function updateGhost() {
        if (isLineTool) {
          ghostLine.setAttribute('x1', startX); ghostLine.setAttribute('y1', startY);
          ghostLine.setAttribute('x2', curX); ghostLine.setAttribute('y2', curY);
          return;
        }
        const x = Math.min(startX, curX), y = Math.min(startY, curY);
        const w = Math.abs(curX - startX), h = Math.abs(curY - startY);
        ghost.style.left = x + 'px'; ghost.style.top = y + 'px';
        ghost.style.width = w + 'px'; ghost.style.height = h + 'px';
      }
      function onMove(ev) {
        curX = (ev.clientX - rect.left) / zoom;
        curY = (ev.clientY - rect.top) / zoom;
        updateGhost();
      }
      function onUp() {
        document.removeEventListener('pointermove', onMove);
        document.removeEventListener('pointerup', onUp);
        ghost.remove();
        const x = Math.min(startX, curX), y = Math.min(startY, curY);
        const w = Math.max(Math.abs(curX - startX), 20);
        const h = Math.max(Math.abs(curY - startY), 20);
        if (currentTool === 'link') {
          PdfEditModals.openLinkPrompt((url) => {
            const data = { type: 'link', x, y, w, h, url };
            PdfEditState.addElement(pageIndex, data);
            PdfEditState.commit();
            const el = ElementFactory.render(overlayEl, pageIndex, data);
            onCreated && onCreated(data, el);
          });
          return;
        }
        createShapeAt(overlayEl, pageIndex, currentTool, x, y, w, h, onCreated, startX, startY, curX, curY);
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

  function createShapeAt(overlayEl, pageIndex, type, x, y, w, h, onCreated, startX, startY, curX, curY) {
    let color = defaultStyle.shapeColor;
    if (type === 'whiteout') color = '#FFFFFF';
    else if (type === 'highlight') color = '#FFEB3B';
    const data = { type, x, y, w, h, color, strokeWidth: defaultStyle.strokeWidth };
    if (type === 'line' || type === 'arrow') {
      // 실제 드래그 방향(좌→우/우→좌, 위→아래/아래→위)을 박스 안 비율로 저장해
      // 어느 방향으로 그려도 화살표가 항상 드래그 방향대로 보이게 한다.
      data.x1Frac = w ? (startX - x) / w : 0;
      data.y1Frac = h ? (startY - y) / h : 0;
      data.x2Frac = w ? (curX - x) / w : 1;
      data.y2Frac = h ? (curY - y) / h : 1;
    }
    PdfEditState.addElement(pageIndex, data);
    PdfEditState.commit();
    const el = ElementFactory.render(overlayEl, pageIndex, data);
    onCreated && onCreated(data, el);
  }

  /** 도장/서명처럼 이미 만들어진 래스터 이미지를 클릭 지점에 바로 배치 */
  function placeRasterAt(overlayEl, pageIndex, type, src, x, y, w, h, onCreated) {
    const mime = /^data:([^;]+);/.exec(src)?.[1] || 'image/png';
    const data = { type, x: x - w / 2, y: y - h / 2, w, h, src, mime };
    PdfEditState.addElement(pageIndex, data);
    PdfEditState.commit();
    const el = ElementFactory.render(overlayEl, pageIndex, data);
    onCreated && onCreated(data, el);
  }

  /** 자유 드로잉: pointerdown~pointerup 동안의 궤적을 모아 하나의 path 요소로 저장 */
  function startFreehand(e, overlayEl, pageIndex, rect, startX, startY, onCreated) {
    const zoom = getZoom(overlayEl);
    const points = [{ x: startX, y: startY }];
    const svgNs = 'http://www.w3.org/2000/svg';
    const ghostSvg = document.createElementNS(svgNs, 'svg');
    ghostSvg.setAttribute('class', 'pe-drag-ghost');
    ghostSvg.style.position = 'absolute'; ghostSvg.style.left = '0'; ghostSvg.style.top = '0';
    ghostSvg.style.width = '100%'; ghostSvg.style.height = '100%'; ghostSvg.style.pointerEvents = 'none';
    ghostSvg.style.border = 'none'; ghostSvg.style.background = 'none';
    const path = document.createElementNS(svgNs, 'path');
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', defaultStyle.shapeColor);
    path.setAttribute('stroke-width', String(defaultStyle.strokeWidth));
    path.setAttribute('stroke-linecap', 'round');
    path.setAttribute('stroke-linejoin', 'round');
    ghostSvg.appendChild(path);
    overlayEl.appendChild(ghostSvg);

    function updatePath() {
      path.setAttribute('d', 'M ' + points.map(p => `${p.x} ${p.y}`).join(' L '));
    }
    function onMove(ev) {
      points.push({ x: (ev.clientX - rect.left) / zoom, y: (ev.clientY - rect.top) / zoom });
      updatePath();
    }
    function onUp() {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup', onUp);
      ghostSvg.remove();
      if (points.length < 2) return;

      const minX = Math.min(...points.map(p => p.x));
      const minY = Math.min(...points.map(p => p.y));
      const maxX = Math.max(...points.map(p => p.x));
      const maxY = Math.max(...points.map(p => p.y));
      const w = Math.max(maxX - minX, 2), h = Math.max(maxY - minY, 2);
      const localPoints = points.map(p => ({ x: p.x - minX, y: p.y - minY }));

      const data = {
        type: 'freehand', x: minX, y: minY, w, h,
        points: localPoints, color: defaultStyle.shapeColor, strokeWidth: defaultStyle.strokeWidth,
      };
      PdfEditState.addElement(pageIndex, data);
      PdfEditState.commit();
      const el = ElementFactory.render(overlayEl, pageIndex, data);
      onCreated && onCreated(data, el);
    }
    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup', onUp);
  }

  return { getTool, setTool, getDefaultStyle, attachOverlay, resetSignature };
})();
