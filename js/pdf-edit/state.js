/**
 * state.js
 * ─────────────────────────────────────────
 * 편집기 전체 상태(State)와 실행취소/재실행(Undo/Redo) 히스토리를 관리한다.
 *
 * 상태 구조:
 *   state.pages = [
 *     { elements: [ {id, type, x, y, w, h, rot, ...type별 속성}, ... ] },  // page 1
 *     ...
 *   ]
 *   좌표(x, y, w, h)는 항상 "렌더링된 캔버스 픽셀 기준"으로 저장한다.
 *   내보내기(export) 시점에만 PDF 포인트 좌표로 환산한다.
 *
 * 히스토리는 매 확정 동작(요소 추가/이동종료/리사이즈종료/삭제/속성변경)마다
 * 전체 상태의 깊은 복사본을 스택에 쌓는 단순한 방식이다.
 * 문서가 수백 페이지 단위로 커지기 전까지는 성능 문제가 없다.
 */

const PdfEditState = (() => {
  let pages = [];          // [{ elements: [...] }, ...]
  let undoStack = [];
  let redoStack = [];
  const MAX_HISTORY = 60;

  let elementIdSeq = 1;

  function nextId() {
    return 'el_' + (elementIdSeq++);
  }

  function init(pageCount) {
    pages = Array.from({ length: pageCount }, () => ({ elements: [] }));
    undoStack = [];
    redoStack = [];
  }

  function getPage(pageIndex) {
    return pages[pageIndex];
  }

  function getAllPages() {
    return pages;
  }

  function addElement(pageIndex, element) {
    element.id = element.id || nextId();
    pages[pageIndex].elements.push(element);
    return element;
  }

  function removeElement(pageIndex, elementId) {
    const page = pages[pageIndex];
    page.elements = page.elements.filter(el => el.id !== elementId);
  }

  function findElement(pageIndex, elementId) {
    return pages[pageIndex].elements.find(el => el.id === elementId);
  }

  // ── 히스토리(Undo/Redo) ─────────────────────────────
  function snapshot() {
    return JSON.parse(JSON.stringify(pages));
  }

  function commit() {
    undoStack.push(snapshot());
    if (undoStack.length > MAX_HISTORY) undoStack.shift();
    redoStack = []; // 새 동작이 생기면 redo 스택은 폐기
  }

  function undo() {
    if (undoStack.length === 0) return false;
    redoStack.push(snapshot());
    pages = undoStack.pop();
    return true;
  }

  function redo() {
    if (redoStack.length === 0) return false;
    undoStack.push(snapshot());
    pages = redoStack.pop();
    return true;
  }

  function canUndo() { return undoStack.length > 0; }
  function canRedo() { return redoStack.length > 0; }

  function hasAnyElements() {
    return pages.some(p => p.elements.length > 0);
  }

  return {
    init, getPage, getAllPages,
    addElement, removeElement, findElement,
    commit, undo, redo, canUndo, canRedo,
    hasAnyElements, nextId,
  };
})();
