/**
 * modals.js
 * ─────────────────────────────────────────
 * 스탬프 선택, 서명 그리기, 링크 URL 입력처럼 "새 요소를 만들기 전에
 * 사용자 입력을 한 번 더 받아야 하는" 도구들을 위한 팝업 모달 모음.
 * 도장/스탬프 프리셋도 여기서 SVG data-URI로 정의한다(외부 이미지 파일 불필요).
 */

const PdfEditModals = (() => {
  const STAMP_PRESETS = [
    { id: 'approved', label: '승인', color: '#16A34A', text: 'APPROVED' },
    { id: 'completed', label: '완료', color: '#2563EB', text: 'COMPLETED' },
    { id: 'confidential', label: '기밀', color: '#DC2626', text: 'CONFIDENTIAL' },
    { id: 'draft', label: '초안', color: '#D97706', text: 'DRAFT' },
  ];

  /**
   * pdf-lib은 SVG를 직접 embed할 수 없으므로(embedPng/embedJpg만 지원),
   * SVG를 오프스크린 canvas에 그린 뒤 PNG data URI로 변환해서 돌려준다.
   * onReady(pngDataUri)로 비동기 결과를 전달한다.
   */
  function stampPngDataUri(preset, onReady) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="80">
      <rect x="3" y="3" width="234" height="74" rx="10" fill="none" stroke="${preset.color}" stroke-width="5"/>
      <text x="120" y="48" font-family="Arial, sans-serif" font-size="26" font-weight="800"
        fill="${preset.color}" text-anchor="middle" transform="rotate(-8 120 40)">${preset.text}</text>
    </svg>`;
    const svgDataUri = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svg)));
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = 240; canvas.height = 80;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
      onReady(canvas.toDataURL('image/png'));
    };
    img.src = svgDataUri;
  }

  function backdrop() {
    const bg = document.createElement('div');
    bg.className = 'pe-modal-backdrop';
    return bg;
  }

  function closeModal(bg) { bg.remove(); }

  /** 도장 프리셋 선택 모달. 선택하면 onPick(dataUri, w, h)를 호출한다. */
  function openStampPicker(onPick) {
    const bg = backdrop();
    bg.innerHTML = `
      <div class="pe-modal-box">
        <h3>도장/스탬프 선택</h3>
        <div class="pe-stamp-grid"></div>
        <button class="pe-modal-cancel">취소</button>
      </div>`;
    const grid = bg.querySelector('.pe-stamp-grid');
    STAMP_PRESETS.forEach(preset => {
      const btn = document.createElement('button');
      btn.className = 'pe-stamp-option';
      btn.style.borderColor = preset.color;
      btn.style.color = preset.color;
      btn.textContent = preset.label;
      btn.addEventListener('click', () => {
        closeModal(bg);
        stampPngDataUri(preset, (pngDataUri) => onPick(pngDataUri, 180, 60));
      });
      grid.appendChild(btn);
    });
    bg.querySelector('.pe-modal-cancel').addEventListener('click', () => closeModal(bg));
    document.body.appendChild(bg);
  }

  /**
   * 서명 그리기 모달. 캔버스에 직접 그리거나 이미지 파일을 업로드할 수 있다.
   * 확인을 누르면 onConfirm(dataUri, w, h)를 호출한다.
   */
  function openSignaturePad(onConfirm) {
    const bg = backdrop();
    bg.innerHTML = `
      <div class="pe-modal-box">
        <h3>서명 그리기</h3>
        <div class="pe-sign-canvas-wrap">
          <canvas id="peSignCanvas" height="160"></canvas>
        </div>
        <div class="pe-sign-controls">
          <label>굵기
            <select id="peSignWidth">
              <option value="2">가늘게</option>
              <option value="3" selected>보통</option>
              <option value="5">굵게</option>
            </select>
          </label>
          <label>색상 <input type="color" id="peSignColor" value="#111111"></label>
          <button type="button" id="peSignClear">지우기</button>
          <label class="pe-sign-upload-label">또는 이미지 업로드
            <input type="file" id="peSignUpload" accept="image/png,image/jpeg" style="display:none">
          </label>
        </div>
        <div class="pe-modal-actions">
          <button class="pe-modal-cancel">취소</button>
          <button class="pe-modal-confirm" id="peSignConfirm">서명 사용하기</button>
        </div>
      </div>`;
    document.body.appendChild(bg);

    const canvas = bg.querySelector('#peSignCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.parentElement.clientWidth;
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    let drawing = false, hasInk = false;
    let uploadedDataUri = null;

    function pos(e) {
      const r = canvas.getBoundingClientRect();
      const t = e.touches ? e.touches[0] : e;
      return { x: t.clientX - r.left, y: t.clientY - r.top };
    }
    function start(e) { drawing = true; hasInk = true; uploadedDataUri = null; const p = pos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); }
    function move(e) {
      if (!drawing) return;
      const p = pos(e);
      ctx.lineTo(p.x, p.y);
      ctx.strokeStyle = bg.querySelector('#peSignColor').value;
      ctx.lineWidth = +bg.querySelector('#peSignWidth').value;
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.stroke();
    }
    function stop() { drawing = false; }
    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', move);
    window.addEventListener('mouseup', stop);
    canvas.addEventListener('touchstart', e => { e.preventDefault(); start(e); });
    canvas.addEventListener('touchmove', e => { e.preventDefault(); move(e); });
    canvas.addEventListener('touchend', stop);

    bg.querySelector('#peSignClear').addEventListener('click', () => {
      ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
      hasInk = false; uploadedDataUri = null;
    });

    bg.querySelector('#peSignUpload').addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        uploadedDataUri = reader.result;
        const img = new Image();
        img.onload = () => {
          ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
          const scale = Math.min(canvas.width / img.width, canvas.height / img.height, 1);
          const w = img.width * scale, h = img.height * scale;
          ctx.drawImage(img, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
          hasInk = true;
        };
        img.src = uploadedDataUri;
      };
      reader.readAsDataURL(file);
    });

    bg.querySelector('.pe-modal-cancel').addEventListener('click', () => closeModal(bg));
    bg.querySelector('#peSignConfirm').addEventListener('click', () => {
      if (!hasInk) { alert('서명을 그리거나 이미지를 업로드해 주세요.'); return; }
      const dataUri = uploadedDataUri || canvas.toDataURL('image/png');
      closeModal(bg);
      onConfirm(dataUri, 180, 70);
    });
  }

  /** 간단한 URL 입력 모달 (링크 삽입용). onConfirm(url)을 호출한다. */
  function openLinkPrompt(onConfirm) {
    const bg = backdrop();
    bg.innerHTML = `
      <div class="pe-modal-box">
        <h3>링크 URL 입력</h3>
        <input type="url" id="peLinkUrl" placeholder="https://example.com" class="pe-link-input">
        <div class="pe-modal-actions">
          <button class="pe-modal-cancel">취소</button>
          <button class="pe-modal-confirm" id="peLinkConfirm">추가</button>
        </div>
      </div>`;
    document.body.appendChild(bg);
    const input = bg.querySelector('#peLinkUrl');
    input.focus();
    bg.querySelector('.pe-modal-cancel').addEventListener('click', () => closeModal(bg));
    bg.querySelector('#peLinkConfirm').addEventListener('click', confirm);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') confirm(); });
    function confirm() {
      let url = input.value.trim();
      if (!url) { closeModal(bg); return; }
      if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
      closeModal(bg);
      onConfirm(url);
    }
  }

  return { openStampPicker, openSignaturePad, openLinkPrompt };
})();
