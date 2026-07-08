/**
 * formFields.js
 * ─────────────────────────────────────────
 * 업로드된 PDF 안에 이미 존재하는 AcroForm 필드(텍스트/체크박스)를
 * pdf-lib으로 감지해 우측 패널에 입력 UI를 만들어주고,
 * 사용자가 입력한 값을 내보내기(export) 시점에 원본 필드에 채워 넣는다.
 *
 * 캔버스 위에 자유 배치하는 다른 요소들과 달리, 이 값들은 pageIndex별
 * overlay 요소가 아니라 "필드 이름 → 값" 형태로 별도 보관한다.
 */

const FormFields = (() => {
  let detectedFields = []; // [{ name, type: 'text'|'checkbox' }]
  let values = {};          // { [fieldName]: string | boolean }

  async function detect(arrayBuffer) {
    detectedFields = [];
    values = {};
    try {
      const { PDFDocument, PDFTextField, PDFCheckBox } = PDFLib;
      const doc = await PDFDocument.load(arrayBuffer, { ignoreEncryption: true });
      const form = doc.getForm();
      const fields = form.getFields();
      fields.forEach(f => {
        // pdf-lib의 minified 빌드는 constructor.name이 뭉개지므로 instanceof로 판별한다
        if (f instanceof PDFTextField) {
          detectedFields.push({ name: f.getName(), type: 'text' });
          values[f.getName()] = '';
        } else if (f instanceof PDFCheckBox) {
          detectedFields.push({ name: f.getName(), type: 'checkbox' });
          values[f.getName()] = false;
        }
      });
    } catch (e) {
      // 폼이 없거나 읽기 실패해도 편집기 자체는 계속 동작해야 하므로 조용히 무시
      console.warn('폼 필드 감지 실패(무시):', e.message);
    }
    return detectedFields;
  }

  function renderPanel(panelEl, listEl) {
    if (!detectedFields.length) { panelEl.style.display = 'none'; return; }
    panelEl.style.display = 'block';
    listEl.innerHTML = detectedFields.map(f => {
      if (f.type === 'checkbox') {
        return `<div class="pe-form-field-row">
          <label><input type="checkbox" data-field="${f.name}"> ${f.name}</label>
        </div>`;
      }
      return `<div class="pe-form-field-row">
        <label>${f.name}</label>
        <input type="text" data-field="${f.name}">
      </div>`;
    }).join('');

    listEl.querySelectorAll('[data-field]').forEach(input => {
      const name = input.dataset.field;
      input.addEventListener('input', () => {
        values[name] = input.type === 'checkbox' ? input.checked : input.value;
      });
      input.addEventListener('change', () => {
        values[name] = input.type === 'checkbox' ? input.checked : input.value;
      });
    });
  }

  /** export 단계에서 이미 로드된 pdfDoc(pdf-lib)에 값들을 채워 넣는다. */
  function applyToDoc(pdfDoc) {
    if (!detectedFields.length) return;
    const form = pdfDoc.getForm();
    detectedFields.forEach(f => {
      try {
        if (f.type === 'text') {
          const field = form.getTextField(f.name);
          if (values[f.name]) field.setText(values[f.name]);
        } else if (f.type === 'checkbox') {
          const field = form.getCheckBox(f.name);
          if (values[f.name]) field.check(); else field.uncheck();
        }
      } catch (e) {
        console.warn('폼 필드 적용 실패:', f.name, e.message);
      }
    });
  }

  function hasFields() { return detectedFields.length > 0; }

  return { detect, renderPanel, applyToDoc, hasFields };
})();
