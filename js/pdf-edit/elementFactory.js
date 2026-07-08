/**
 * elementFactory.js
 * ─────────────────────────────────────────
 * 편집 요소(텍스트/도형/이미지/화이트아웃) 하나하나를 실제 DOM 노드로
 * 그려내고, 선택·이동·크기조절·삭제 상호작용을 붙여주는 모듈.
 *
 * 요소 데이터(state.js의 element 객체)와 화면에 보이는 DOM 노드는
 * 항상 1:1로 매칭되며, 이동/리사이즈가 끝나는 시점에만 state에 반영하고
 * PdfEditState.commit()으로 히스토리에 기록한다(드래그 중간중간은 기록 안 함).
 */

const SHAPE_TYPES = ['rect', 'circle', 'line', 'arrow'];

const ElementFactory = (() => {
  let selectedEl = null;       // 현재 선택된 DOM 엘리먼트
  let onSelectionChange = null; // (element data | null) => void

  function setOnSelectionChange(cb) { onSelectionChange = cb; }

  /**
   * CSS zoom은 페이지 wrap 전체(자식 포함)의 픽셀 좌표계를 함께 축소하므로,
   * 화면(screen) 픽셀 delta를 요소 좌표(zoom 적용 전 로컬 px)로 되돌리려면
   * 반드시 현재 zoom 배율로 나눠야 한다. 나누지 않으면 zoom<1일 때
   * 클릭 지점보다 원점 쪽으로 쏠려서 요소가 배치/이동/리사이즈된다.
   */
  function getZoom(overlayEl) {
    const wrap = overlayEl.closest('.pe-page-wrap');
    const z = wrap ? parseFloat(wrap.style.zoom) : 1;
    return z > 0 ? z : 1;
  }

  function deselectAll() {
    document.querySelectorAll('.pe-element.selected').forEach(el => el.classList.remove('selected'));
    selectedEl = null;
    if (onSelectionChange) onSelectionChange(null);
  }

  /**
   * element 데이터를 기반으로 DOM 노드를 생성해 overlay에 붙인다.
   * pageIndex, overlayEl은 이동/삭제 시 state 동기화를 위해 필요.
   */
  function render(overlayEl, pageIndex, data) {
    const el = document.createElement('div');
    el.className = 'pe-element pe-type-' + data.type;
    el.dataset.id = data.id;
    positionEl(el, data);

    const inner = buildInner(data);
    el.appendChild(inner);

    // 자유 드로잉(freehand)은 선 굵기·좌표가 뒤틀리는 걸 막기 위해
    // 리사이즈 핸들 없이 이동만 가능하게 한다. 나머지는 4방향 핸들 제공.
    if (data.type !== 'freehand') {
      ['nw', 'ne', 'sw', 'se'].forEach(pos => {
        const h = document.createElement('div');
        h.className = 'pe-resize-handle pe-handle-' + pos;
        h.dataset.pos = pos;
        el.appendChild(h);
      });
    }

    const delBtn = document.createElement('button');
    delBtn.className = 'pe-delete-btn';
    delBtn.type = 'button';
    delBtn.innerHTML = '✕';
    delBtn.title = '삭제';
    el.appendChild(delBtn);

    overlayEl.appendChild(el);
    attachInteractions(el, overlayEl, pageIndex, data);
    return el;
  }

  function positionEl(el, data) {
    el.style.left = data.x + 'px';
    el.style.top = data.y + 'px';
    el.style.width = data.w + 'px';
    el.style.height = data.h + 'px';
  }

  function buildInner(data) {
    if (data.type === 'text') {
      const div = document.createElement('div');
      div.className = 'pe-text-content';
      div.contentEditable = 'true';
      div.style.fontSize = data.fontSize + 'px';
      div.style.color = data.color;
      div.style.fontWeight = data.bold ? '700' : '400';
      div.style.fontFamily = fontFamilyCss(data.fontFamily);
      div.textContent = data.text || '';
      return div;
    }
    if (data.type === 'image' || data.type === 'signature' || data.type === 'stamp') {
      const img = document.createElement('img');
      img.src = data.src;
      img.draggable = false;
      return img;
    }
    if (data.type === 'whiteout') {
      const div = document.createElement('div');
      div.className = 'pe-whiteout-fill';
      return div;
    }
    if (data.type === 'highlight') {
      const div = document.createElement('div');
      div.className = 'pe-highlight-fill';
      div.style.background = hexToRgba(data.color || '#FFEB3B', 0.45);
      return div;
    }
    if (data.type === 'link') {
      const div = document.createElement('div');
      div.className = 'pe-link-marker';
      div.innerHTML = '🔗';
      div.title = data.url || '';
      return div;
    }
    if (data.type === 'freehand') {
      const svgWrap = document.createElement('div');
      svgWrap.className = 'pe-shape-svg-wrap';
      svgWrap.innerHTML = buildFreehandSvg(data);
      return svgWrap;
    }
    // 도형: rect / circle / line / arrow → SVG로 그린다 (박스 크기에 맞춰 자동 재계산)
    const svgWrap = document.createElement('div');
    svgWrap.className = 'pe-shape-svg-wrap';
    svgWrap.innerHTML = buildShapeSvg(data);
    return svgWrap;
  }

  function hexToRgba(hex, alpha) {
    const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!m) return hex;
    return `rgba(${parseInt(m[1], 16)},${parseInt(m[2], 16)},${parseInt(m[3], 16)},${alpha})`;
  }

  function buildFreehandSvg(data) {
    const pts = data.points || [];
    if (pts.length < 2) return '';
    const d = 'M ' + pts.map(p => `${p.x} ${p.y}`).join(' L ');
    return `<svg width="100%" height="100%" viewBox="0 0 ${data.w} ${data.h}" preserveAspectRatio="none">
      <path d="${d}" fill="none" stroke="${data.color || '#EF4444'}" stroke-width="${data.strokeWidth || 3}"
        stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  }

  function buildShapeSvg(data) {
    const w = data.w, h = data.h;
    const stroke = data.color || '#EF4444';
    const sw = data.strokeWidth || 3;
    if (data.type === 'rect') {
      return `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <rect x="${sw / 2}" y="${sw / 2}" width="${Math.max(w - sw, 0)}" height="${Math.max(h - sw, 0)}"
          fill="none" stroke="${stroke}" stroke-width="${sw}"/></svg>`;
    }
    if (data.type === 'circle') {
      return `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <ellipse cx="${w / 2}" cy="${h / 2}" rx="${Math.max(w / 2 - sw / 2, 0)}" ry="${Math.max(h / 2 - sw / 2, 0)}"
          fill="none" stroke="${stroke}" stroke-width="${sw}"/></svg>`;
    }
    if (data.type === 'line' || data.type === 'arrow') {
      // x1Frac~y2Frac: 실제 드래그 시작→끝 방향을 박스 대비 비율(0~1)로 저장해둔 값.
      // 예전 요소(필드 없음)는 기본값 (0,0)→(1,1)로 대각선 유지(하위 호환).
      const x1 = (data.x1Frac ?? 0) * w, y1 = (data.y1Frac ?? 0) * h;
      const x2 = (data.x2Frac ?? 1) * w, y2 = (data.y2Frac ?? 1) * h;
      if (data.type === 'line') {
        return `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
          <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${sw}"/></svg>`;
      }
      // 화살촉은 SVG <marker orient="auto">를 쓰지 않고 각도를 직접 계산해서 그린다.
      // marker+orient=auto는 CSS zoom으로 축소된 상태에서 화살촉이 일그러지는
      // 문제가 있어(줌 배율이 작을수록 심해짐), export 쪽(exportManager.js)과 동일하게
      // 순수 삼각함수로 두 개의 짧은 선을 그려 항상 정삼각형 모양을 유지한다.
      const angle = Math.atan2(y2 - y1, x2 - x1);
      const headLen = Math.max(10, sw * 4);
      const spread = Math.PI / 7;
      const hx1 = x2 - headLen * Math.cos(angle - spread), hy1 = y2 - headLen * Math.sin(angle - spread);
      const hx2 = x2 - headLen * Math.cos(angle + spread), hy2 = y2 - headLen * Math.sin(angle + spread);
      return `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${sw}"/>
        <line x1="${x2}" y1="${y2}" x2="${hx1}" y2="${hy1}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round"/>
        <line x1="${x2}" y1="${y2}" x2="${hx2}" y2="${hy2}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round"/>
      </svg>`;
    }
    return '';
  }

  function fontFamilyCss(name) {
    const map = {
      Helvetica: "'Arial', sans-serif",
      TimesRoman: "'Times New Roman', serif",
      Courier: "'Courier New', monospace",
    };
    return map[name] || map.Helvetica;
  }

  // ── 상호작용: 선택 / 이동 / 리사이즈 / 삭제 / 텍스트 편집 ──
  function attachInteractions(el, overlayEl, pageIndex, data) {
    el.addEventListener('pointerdown', (e) => {
      // 다른 도구(사각형/화살표 등)가 선택된 상태에서 기존 요소 위를 클릭하면
      // 여기서 이동을 시작하지 않고 그대로 overlay 쪽 "새 요소 그리기"로 넘긴다.
      // (그렇지 않으면 이미 그려둔 요소 위에서는 새 도형을 그릴 수 없게 된다.)
      if (typeof Toolbar !== 'undefined' && Toolbar.getTool() !== 'select') return;
      if (e.target.classList.contains('pe-resize-handle')) return;
      if (e.target.classList.contains('pe-delete-btn')) return;
      if (data.type === 'text' && e.target.classList.contains('pe-text-content') && el.classList.contains('selected')) {
        return; // 이미 선택된 텍스트는 편집 모드로 두고 드래그하지 않음
      }
      select(el, data);
      startDrag(e, el, overlayEl, pageIndex, data);
    });

    el.querySelectorAll('.pe-resize-handle').forEach(handle => {
      handle.addEventListener('pointerdown', (e) => {
        e.stopPropagation();
        select(el, data);
        startResize(e, el, overlayEl, pageIndex, data, handle.dataset.pos);
      });
    });

    el.querySelector('.pe-delete-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      PdfEditState.removeElement(pageIndex, data.id);
      PdfEditState.commit();
      el.remove();
      deselectAll();
    });

    if (data.type === 'text') {
      const content = el.querySelector('.pe-text-content');
      content.addEventListener('blur', () => {
        data.text = content.textContent;
        PdfEditState.commit();
      });
      content.addEventListener('pointerdown', (e) => e.stopPropagation());
      el.addEventListener('dblclick', () => content.focus());
    }
  }

  function select(el, data) {
    deselectAll();
    el.classList.add('selected');
    selectedEl = el;
    if (onSelectionChange) onSelectionChange(data);
  }

  function startDrag(e, el, overlayEl, pageIndex, data) {
    e.preventDefault();
    const startX = e.clientX, startY = e.clientY;
    const origX = data.x, origY = data.y;
    const zoom = getZoom(overlayEl);
    const boundsW = overlayEl.getBoundingClientRect().width / zoom;
    const boundsH = overlayEl.getBoundingClientRect().height / zoom;

    function onMove(ev) {
      const dx = (ev.clientX - startX) / zoom;
      const dy = (ev.clientY - startY) / zoom;
      data.x = clamp(origX + dx, 0, boundsW - data.w);
      data.y = clamp(origY + dy, 0, boundsH - data.h);
      positionEl(el, data);
    }
    function onUp() {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup', onUp);
      PdfEditState.commit();
    }
    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup', onUp);
  }

  function startResize(e, el, overlayEl, pageIndex, data, pos) {
    e.preventDefault();
    const startX = e.clientX, startY = e.clientY;
    const orig = { x: data.x, y: data.y, w: data.w, h: data.h };
    const zoom = getZoom(overlayEl);
    const MIN = 16;

    function onMove(ev) {
      const dx = (ev.clientX - startX) / zoom;
      const dy = (ev.clientY - startY) / zoom;
      let { x, y, w, h } = orig;
      if (pos.includes('e')) w = Math.max(MIN, orig.w + dx);
      if (pos.includes('s')) h = Math.max(MIN, orig.h + dy);
      if (pos.includes('w')) { w = Math.max(MIN, orig.w - dx); x = orig.x + orig.w - w; }
      if (pos.includes('n')) { h = Math.max(MIN, orig.h - dy); y = orig.y + orig.h - h; }
      data.x = x; data.y = y; data.w = w; data.h = h;
      positionEl(el, data);
      if (SHAPE_TYPES.includes(data.type)) {
        const svgWrap = el.querySelector('.pe-shape-svg-wrap');
        if (svgWrap) svgWrap.innerHTML = buildShapeSvg(data);
      }
    }
    function onUp() {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup', onUp);
      PdfEditState.commit();
    }
    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup', onUp);
  }

  function clamp(v, min, max) { return Math.max(min, Math.min(v, Math.max(min, max))); }

  function updateStyle(data, patch) {
    Object.assign(data, patch);
    const el = document.querySelector(`.pe-element[data-id="${data.id}"]`);
    if (!el) return;
    if (data.type === 'text') {
      const content = el.querySelector('.pe-text-content');
      content.style.fontSize = data.fontSize + 'px';
      content.style.color = data.color;
      content.style.fontWeight = data.bold ? '700' : '400';
      content.style.fontFamily = fontFamilyCss(data.fontFamily);
    } else if (data.type === 'highlight') {
      const fill = el.querySelector('.pe-highlight-fill');
      if (fill) fill.style.background = hexToRgba(data.color || '#FFEB3B', 0.45);
    } else if (SHAPE_TYPES.includes(data.type)) {
      const svgWrap = el.querySelector('.pe-shape-svg-wrap');
      if (svgWrap) svgWrap.innerHTML = buildShapeSvg(data);
    }
  }

  return { render, deselectAll, setOnSelectionChange, updateStyle, positionEl };
})();
