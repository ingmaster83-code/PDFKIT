# PDFKIT 프로젝트 지침

## 프로젝트 개요
- **사이트명:** PDF킷
- **URL:** https://pdfkit.wooahouse.com
- **GitHub:** https://github.com/ingmaster83-code/PDFKIT
- **배포:** GitHub Pages (main 브랜치 → root)
- **도메인 관리:** 호스팅케이알
- **DNS:** pdfkit CNAME → ingmaster83-code.github.io

## 기술 스택
- 순수 HTML / CSS / JS (프레임워크 없음)
- PDF 처리: 브라우저 내 로컬 처리 (서버 전송 없음)
- PWA: manifest.json + sw.js + js/pwa-install.js

## 파일 구조
```
PDFKIT/
├── index.html              # 메인 (툴 목록)
├── pdf-to-jpg.html         # PDF → JPG/PNG 변환
├── jpg-to-pdf.html         # 이미지 → PDF 변환
├── merge-pdf.html          # PDF 병합
├── split-pdf.html          # PDF 분할
├── rotate-pdf.html         # PDF 회전
├── delete-pages.html       # 페이지 삭제
├── watermark-pdf.html      # 워터마크 추가
├── page-number-pdf.html    # 페이지 번호
├── compress-pdf.html       # PDF 압축
├── unlock-pdf.html         # 잠금 해제
├── pdf-viewer.html         # PDF 뷰어 다운로드 안내
├── about.html              # 서비스 소개
├── privacy.html            # 개인정보처리방침
├── css/style.css           # 공통 스타일
├── js/pwa-install.js       # PWA 설치 유도
├── manifest.json           # PWA 매니페스트
├── sw.js                   # 서비스 워커
└── CNAME                   # pdfkit.wooahouse.com
```

## 작업 규칙
- 새 도구 페이지 추가 시 index.html 카드, footer 링크, sitemap.xml, ld+json 구조화 데이터 모두 업데이트
- 모든 페이지에 `<script src="js/pwa-install.js"></script>` 포함
- 다운로드 버튼은 반드시 `id="downloadBtn"` 사용 (PWA 배너 트리거)
- 파일은 서버에 저장되지 않는다는 문구 유지 (신뢰도)

## SEO 방향
- "무료" 키워드 강조 (타이틀, 설명, 카드 뱃지)
- 각 툴카드에 녹색 "무료" 뱃지 (.free-badge) 적용 중
- Hero 문구: "모든 PDF 작업 무료로, 한 곳에서"

## 현재 상태 (2026-03-14)
- HTTPS 인증서 발급 대기 중 (GitHub Pages 자동 처리, 최대 24시간)
- http://로는 정상 접속됨
- PWA 설치 배너 구현됨 (다운로드 버튼 클릭 후 1.5초 뒤 표시)
