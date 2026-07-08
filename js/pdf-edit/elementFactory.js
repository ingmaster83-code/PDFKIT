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
    if (data.type === 'line') {
      return `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <line x1="0" y1="0" x2="${w}" y2="${h}" stroke="${stroke}" stroke-width="${sw}"/></svg>`;
    }
    if (data.type === 'arrow') {
      return `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <defs><marker id="arrowhead-${data.id}" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
          <polygon points="0 0, 10 4, 0 8" fill="${stroke}"/></marker></defs>
        <line x1="0" y1="0" x2="${w}" y2="${h}" stroke="${stroke}" stroke-width="${sw}"
          marker-end="url(#arrowhead-${data.id})"/></svg>`;
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
    const bounds = overlayEl.getBoundingClientRect();

    function onMove(ev) {
      const dx = ev.clientX - startX;
      const dy = ev.clientY - startY;
      data.x = clamp(origX + dx, 0, bounds.width - data.w);
      data.y = clamp(origY + dy, 0, bounds.height - data.h);
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
    const MIN = 16;

    function onMove(ev) {
      const dx = ev.clientX - startX;
      const dy = ev.clientY - startY;
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
