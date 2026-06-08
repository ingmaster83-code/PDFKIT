"""
pdfkit.wooahouse.com KO 페이지 메타 디스크립션 CTR 최적화
- 기준: 네이버 서치어드바이저 노출 대비 CTR 개선
- 전략: 키워드 선행 배치, 구체적 수치/혜택, 중복 보일러플레이트 제거
"""
import re

BASE = 'C:/개인/wooahouse/PDFKIT'

# { 파일: (현재_desc_포함문자열, 새_description) }
# 현재 값의 앞부분으로 매칭 (전체 일치 불필요)
PAGES = {
    'index.html': (
        'PDF 변환, 합치기, 분할, 압축',
        'PDF 합치기·분할·압축·변환 모두 무료! 설치·회원가입 없이 브라우저에서 바로 사용하는 PDF 도구 모음. 파일이 서버에 저장되지 않아 100% 안전 — 우아PDF(WooaPDF)'
    ),
    'merge-pdf.html': (
        '여러 PDF 파일을 하나로 합치기',
        'PDF 합치기 무료 — 드래그로 순서 조정 후 클릭 한 번에 완성! 여러 PDF를 하나로 합치기, 회원가입·설치 없이 바로 가능. 파일은 서버에 저장되지 않아 100% 안전합니다.'
    ),
    'compress-pdf.html': (
        'PDF 파일 용량을 줄여 저장과 공유',
        'PDF 압축 무료 — 용량을 최대 90% 줄이세요. 강력·균형·고화질 3단계 선택, 이메일·카카오톡 첨부 가능한 크기로 즉시 압축. 설치·로그인 없이 브라우저에서 바로.'
    ),
    'split-pdf.html': (
        'PDF 파일을 페이지별로 나누거나',
        'PDF 분할 무료 — 특정 페이지만 추출하거나 범위별로 나누기. 클릭 몇 번이면 완성, 회원가입 없이 브라우저에서 바로 사용. 파일 서버 저장 없음.'
    ),
    'pdf-image-extract.html': (
        'PDF 파일에 포함된 이미지',
        'PDF 이미지 추출 무료 — PDF 속 사진·그림·로고를 JPG·PNG로 저장. 드래그앤드롭으로 간편 업로드, 브라우저에서 바로 처리. 서버 전송 없이 100% 안전.'
    ),
    'pdf-to-jpg.html': (
        'PDF를 JPG, PNG 이미지로 무료',
        'PDF를 JPG 이미지로 무료 변환 — 고화질 변환, 페이지 범위 선택 가능. 브라우저에서 바로 처리되어 파일이 서버에 저장되지 않아 100% 안전. 설치·로그인 불필요.'
    ),
    'jpg-to-pdf.html': (
        'JPG, PNG 이미지를 PDF로 무료',
        'JPG·PNG 이미지를 PDF로 무료 변환 — 여러 이미지를 한 PDF로 합치기, 드래그로 순서 조정 가능. 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'watermark-pdf.html': (
        'PDF에 CONFIDENTIAL, 사본',
        'PDF 워터마크 추가 무료 — CONFIDENTIAL·사본·샘플 등 텍스트 도장 삽입. 위치·색상·투명도 자유 설정, 한글 지원. 브라우저에서 바로 처리, 서버 전송 없음.'
    ),
    'rotate-pdf.html': (
        'PDF 페이지를 90도',
        'PDF 회전 무료 — 페이지를 90°·180°·270°로 즉시 회전. 전체 또는 특정 페이지만 선택 가능. 설치·로그인 없이 브라우저에서 바로 처리, 파일 서버 저장 없음.'
    ),
    'delete-pages.html': (
        'PDF에서 불필요한 페이지를 클릭',
        'PDF 페이지 삭제 무료 — 불필요한 페이지를 클릭으로 선택해 즉시 제거. 미리보기로 확인 후 삭제, 원본은 그대로. 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'pdf-to-word.html': (
        'PDF 파일을 Word 문서',
        'PDF를 Word 파일로 무료 변환 — 텍스트 기반 PDF를 편집 가능한 .doc 파일로 저장. 설치·로그인 없이 브라우저에서 바로 사용, 파일이 서버에 저장되지 않아 안전.'
    ),
    'unlock-pdf.html': (
        '비밀번호로 보호된 PDF의 잠금을',
        'PDF 잠금 해제 무료 — 비밀번호로 잠긴 PDF를 브라우저에서 바로 열기. 암호화된 PDF를 일반 PDF로 변환, 설치·로그인 불필요. 파일은 서버에 저장되지 않습니다.'
    ),
    'pdf-password.html': (
        'PDF 파일에 열기 비밀번호를 무료로',
        'PDF 비밀번호 설정 무료 — PDF에 열기 암호를 추가해 문서를 안전하게 보호. 인쇄·복사·편집 권한도 제어 가능. 설치·로그인 없이 브라우저에서 바로 처리.'
    ),
    'pdf-text-extract.html': (
        'PDF에서 텍스트를 무료 추출',
        'PDF 텍스트 추출 무료 — 복사 안 되는 PDF에서 글자를 추출해 TXT 저장 또는 복사. 페이지별 텍스트 확인 가능, 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'pdf-sign.html': (
        'PDF에 전자서명을 무료로 추가',
        'PDF 전자서명 추가 무료 — 캔버스에 직접 서명 후 PDF에 삽입. 마우스·터치 모두 지원, 서명 위치 자유 선택. 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'office-to-pdf.html': (
        'Word(.docx), Excel(.xlsx)',
        'Word·Excel을 PDF로 무료 변환 — .docx·.xlsx 파일을 PDF로 저장. 미리보기 후 인쇄 기능으로 PDF 저장, 회원가입 없이 브라우저에서 바로 사용 가능.'
    ),
    'page-number-pdf.html': (
        'PDF 각 페이지에 번호를 자동으로',
        'PDF 페이지 번호 추가 무료 — 모든 페이지에 자동으로 번호 삽입. 위치·형식·시작 번호 설정 가능. 설치·로그인 없이 브라우저에서 바로 처리, 서버 전송 없음.'
    ),
    'pdf-reorder.html': (
        'PDF 페이지 순서를 드래그',
        'PDF 페이지 순서 변경 무료 — 썸네일 미리보기를 보며 드래그로 페이지 재정렬. 회원가입 없이 브라우저에서 바로 사용, 파일이 서버에 저장되지 않아 안전.'
    ),
    'pdf-metadata.html': (
        'PDF 파일의 제목, 작성자, 주제',
        'PDF 메타데이터 편집 무료 — 제목·작성자·주제·키워드를 브라우저에서 바로 수정. 현재 정보를 즉시 확인하고 편집 가능, 서버 전송 없이 100% 안전.'
    ),
    'pdf-header-footer.html': (
        'PDF 모든 페이지에 헤더',
        'PDF 헤더·푸터 추가 무료 — 모든 페이지 상단·하단에 회사명·날짜·제목 텍스트 삽입. 설치·로그인 없이 브라우저에서 바로 처리, 파일 서버 저장 없음.'
    ),
    'pdf-resize.html': (
        'PDF 페이지 크기를 A4',
        'PDF 페이지 크기 변환 무료 — A4·A3·Letter 등 원하는 규격으로 즉시 변환. 내용을 자동 축소·확대, 설치·로그인 없이 브라우저에서 바로 처리.'
    ),
    'pdf-compare.html': (
        '두 PDF 파일의 텍스트 차이를',
        'PDF 비교 무료 — 두 PDF의 텍스트 차이를 색상으로 한눈에 확인! 추가·삭제·변경 내용 자동 표시. 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'pdf-odd-even.html': (
        'PDF에서 홀수 페이지 또는 짝수',
        'PDF 홀짝 페이지 분리 무료 — 홀수 또는 짝수 페이지만 추출. 양면 인쇄 스캔 정리에 최적, 설치·로그인 없이 브라우저에서 바로 처리. 서버 전송 없음.'
    ),
    'pdf-to-csv.html': (
        'PDF 파일의 표와 텍스트 데이터를 CSV',
        'PDF를 CSV로 변환 무료 — PDF 속 표와 텍스트 데이터를 CSV로 추출, 엑셀에서 바로 열기 가능. 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'pdf-to-epub.html': (
        'PDF 파일을 전자책 EPUB',
        'PDF를 EPUB으로 변환 무료 — PDF 텍스트를 추출해 전자책 EPUB 파일로 저장. 설치·로그인 없이 브라우저에서 바로 처리, 파일이 서버에 저장되지 않아 안전.'
    ),
    'epub-to-pdf.html': (
        'EPUB 전자책 파일을 PDF로',
        'EPUB을 PDF로 변환 무료 — 전자책 EPUB 파일을 인쇄 기능으로 PDF 저장. 내용을 미리보기 후 변환, 설치·로그인 없이 브라우저에서 바로 사용.'
    ),
    'heic-to-pdf.html': (
        '아이폰 HEIC/HEIF 사진을 PDF로',
        'HEIC를 PDF로 변환 무료 — 아이폰 HEIC·HEIF 사진을 PDF로 변환. 여러 장을 한 PDF로 합치기 가능, 설치·로그인 없이 브라우저에서 바로 처리. 서버 전송 없음.'
    ),
    'pdf-viewer.html': (
        'PDF 파일을 열 수 없을 때',
        '무료 PDF 뷰어 다운로드 — PDF 파일이 안 열릴 때 필요한 뷰어 모음. Adobe Acrobat Reader·Foxit·SumatraPDF 공식 다운로드 링크 PC·모바일별 정리.'
    ),
    'pptx-to-pdf.html': (
        '파워포인트(.pptx) 파일을 PDF로',
        '파워포인트를 PDF로 변환 무료 — .pptx 슬라이드 레이아웃·이미지·텍스트 그대로 PDF로 저장. 회원가입·설치 없이 브라우저에서 바로 사용, 파일이 서버에 전송되지 않아 안전.'
    ),
}

import os

ok_count = 0
fail_count = 0

for fname, (match_prefix, new_desc) in PAGES.items():
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        print(f'  SKIP (없음): {fname}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # meta name="description" content="..." 전체 교체
    # 현재 content 값에 match_prefix가 포함되어 있는지 확인 후 교체
    pattern = r'(<meta name="description" content=")[^"]*(")'

    def replacer(m):
        current = m.group(0)
        if match_prefix in current:
            return m.group(1) + new_desc + m.group(2)
        return current

    new_content = re.sub(pattern, replacer, content)

    if new_content == content:
        print(f'  MISS (매칭 안됨): {fname} — prefix: {match_prefix[:30]}')
        fail_count += 1
    else:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'  OK: {fname}')
        ok_count += 1

print(f'\n완료: {ok_count}개 교체, {fail_count}개 실패')
