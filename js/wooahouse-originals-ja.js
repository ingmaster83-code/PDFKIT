(function () {
  const SITES = [
    { host: 'pdfkit.wooahouse.com',      badge: 'WOOOAPDF',    color: '#FF4444', icon: '📄', title: '無料オンラインPDFツール',              desc: 'PDF変換・結合・分割・圧縮・回転・透かし追加。ファイルはブラウザ外に出ず100%安全で無料。',    url: 'https://pdfkit.wooahouse.com/ja/' },
    { host: 'imagekit.wooahouse.com',     badge: 'WOOAIMAGE',   color: '#6366F1', icon: '🖼️', title: '無料オンライン画像ツール',            desc: '圧縮・リサイズ・変換・背景削除をブラウザで直接。アップロード不要。',                            url: 'https://imagekit.wooahouse.com/en/' },
    { host: 'colorkit.wooahouse.com',     badge: 'WOOACOLOR',   color: '#F59E0B', icon: '🎨', title: 'カラーピッカー＆パレット生成',   desc: '画像から色を抽出、HEX/RGB変換、美しいパレットを瞬時に生成。',                            url: 'https://colorkit.wooahouse.com/en/' },
    { host: 'textkit.wooahouse.com',      badge: 'WOOATEXT',    color: '#10B981', icon: '✏️', title: 'テキスト変換・編集ツール',        desc: 'テキスト変換・整列・行番号追加など多様なテキスト作業を一箇所で。',                                      url: 'https://textkit.wooahouse.com/en/' },
    { host: 'qrkit.wooahouse.com',        badge: 'WOOAQR',      color: '#3B82F6', icon: '📱', title: 'QRコード生成・スキャン',        desc: 'URL・テキスト・連絡先など多様なQRコードを無料で制限なく生成。',                                      url: 'https://qrkit.wooahouse.com/en/' },
    { host: 'calckit.wooahouse.com',      badge: 'WOOALCALC',   color: '#8B5CF6', icon: '🧮', title: '単位変換・計算機',        desc: '長さ・重さ・温度などの単位変換と数式計算を一箇所で。',                                    url: 'https://calckit.wooahouse.com/en/' },
    { host: 'fontkit.wooahouse.com',      badge: 'WOOAFONT',    color: '#EC4899', icon: '🔤', title: '無料商用フォント集',              desc: '著作権の心配なく使える無料商用フォントの公式ダウンロードリンク集。',                          url: 'https://fontkit.wooahouse.com/en/' },
    { host: 'mactools.wooahouse.com',     badge: 'WOOAMAC',     color: '#6B7280', icon: '🍎', title: 'Mac必須アプリ集',                 desc: 'Mac購入・再フォーマット後に入れるべき必須アプリの公式リンク集。',                                   url: 'https://mactools.wooahouse.com/en/' },
    { host: 'pctools.wooahouse.com',      badge: 'WOOAPC',      color: '#0EA5E9', icon: '🖥️', title: 'Windows必須ソフト集',         desc: 'Windowsフォーマット後に必要な必須プログラムの公式リンク集。',                                        url: 'https://pctools.wooahouse.com/en/' },
    { host: 'vskit.wooahouse.com',        badge: 'WOOAVS',      color: '#007ACC', icon: '💻', title: 'VS Code拡張機能集',      desc: '開発生産性を上げるVS Code拡張機能のおすすめ厳選集。',                                                url: 'https://vskit.wooahouse.com/en/' },
    { host: 'wooaaudio.wooahouse.com',    badge: 'WOOAAUDIO',   color: '#F97316', icon: '🎵', title: 'オンライン音声ツール',                 desc: '変換・編集・トリミング・録音など音声作業を無料でブラウザから。',                                       url: 'https://wooaaudio.wooahouse.com/en/' },
    { host: 'wooavideo.wooahouse.com',    badge: 'WOOAVIDEO',   color: '#EF4444', icon: '🎬', title: 'オンライン動画ツール',                 desc: '変換・圧縮・編集などの動画作業を無料で。サーバーへのアップロード不要。',                                          url: 'https://wooavideo.wooahouse.com/en/' },
    { host: 'wooaviewer.wooahouse.com',   badge: 'WOOAVIEWER',  color: '#14B8A6', icon: '🔍', title: 'ファイルビューア集',             desc: '様々なファイル形式をブラウザで直接表示。ソフトウェアのインストール不要。',                                  url: 'https://wooaviewer.wooahouse.com/en/' },
    { host: 'wooadev.wooahouse.com',      badge: 'WOOADEV',     color: '#64748B', icon: '🛠️', title: '開発者ツール',                    desc: 'JSONフォーマッター・Base64・URLエンコーダーなど開発ツールを一箇所に。',                                        url: 'https://wooadev.wooahouse.com/en/' },
    { host: 'wooaocr.wooahouse.com',      badge: 'WOOAOCR',     color: '#A855F7', icon: '🔎', title: 'OCR — 画像からテキスト抽出',     desc: '画像やスキャン文書からテキストを自動認識して抽出。',                                      url: 'https://wooaocr.wooahouse.com/en/' },
    { host: 'wooasheet.wooahouse.com',    badge: 'WOOASHEET',   color: '#22C55E', icon: '📊', title: 'オンライン表計算ツール',           desc: 'CSV・Excelファイルをブラウザで直接開いて編集・変換。',                                               url: 'https://wooasheet.wooahouse.com/en/' },
    { host: 'wooaseo.wooahouse.com',      badge: 'WOOASEO',     color: '#F59E0B', icon: '🔎', title: 'SEO分析ツール',                 desc: 'SEOスコア分析・キーワードリサーチ・メタタグ生成であなたのサイトを最適化。',                                   url: 'https://wooaseo.wooahouse.com/en/' },
    { host: 'wooagosa.wooahouse.com',     badge: 'WOOAGOSA',    color: '#6366F1', icon: '📝', title: '無料資格模擬試験',            desc: '免許・資格試験の練習を49種のジャンルで無料実施。',                                      url: 'https://wooagosa.wooahouse.com/en/' },
  ];

  function bgLuminance() {
    const bg = getComputedStyle(document.body).backgroundColor;
    const m = bg.match(/\d+/g);
    if (!m || m.length < 3) return 255;
    return 0.299 * +m[0] + 0.587 * +m[1] + 0.114 * +m[2];
  }
  const dark = bgLuminance() < 80;

  const isToolPage = !!document.querySelector('.wooa-orig-anchor');
  const currentHost = window.location.hostname;
  const utmSource = currentHost.replace('.wooahouse.com', '');
  const picks = SITES
    .filter(s => s.host !== currentHost)
    .sort(() => Math.random() - 0.5)
    .slice(0, isToolPage ? 4 : 5);

  if (!picks.length) return;

  const style = document.createElement('style');
  style.textContent = `
    .wooa-orig-wrap {
      margin: 0 0 40px;
    }
    .wooa-orig-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }
    .wooa-orig-dot {
      width: 10px; height: 10px;
      border-radius: 50%;
      background: #3B82F6;
      flex-shrink: 0;
    }
    .wooa-orig-label {
      font-size: 13px;
      font-weight: 800;
      letter-spacing: .08em;
      color: ${dark ? '#e2e8f0' : '#333'};
    }
    .wooa-orig-sub {
      font-size: 13px;
      color: ${dark ? '#94a3b8' : '#888'};
      margin: 0 0 20px 18px;
    }
    .wooa-orig-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 14px;
    }
    .wooa-orig-card {
      background: ${dark ? '#1e293b' : '#fff'};
      border: 1px solid ${dark ? '#334155' : '#e5e7eb'};
      border-radius: 14px;
      padding: 20px;
      text-decoration: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: box-shadow .15s, transform .15s;
      overflow: hidden;
      position: relative;
    }
    .wooa-orig-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 4px;
      background: var(--wooa-color);
    }
    .wooa-orig-card:hover {
      box-shadow: 0 6px 20px rgba(0,0,0,${dark ? '.4' : '.1'});
      transform: translateY(-2px);
    }
    .wooa-orig-top {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 4px;
    }
    .wooa-orig-icon {
      font-size: 28px;
      line-height: 1;
    }
    .wooa-orig-badge {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .06em;
      color: ${dark ? '#64748b' : '#888'};
    }
    .wooa-orig-title {
      font-size: 16px;
      font-weight: 700;
      color: ${dark ? '#e2e8f0' : '#111'};
      line-height: 1.4;
    }
    .wooa-orig-desc {
      font-size: 13px;
      color: ${dark ? '#94a3b8' : '#666'};
      line-height: 1.6;
      flex: 1;
    }
    .wooa-orig-link {
      font-size: 13px;
      font-weight: 600;
      color: ${dark ? '#60a5fa' : '#3B82F6'};
      margin-top: 4px;
    }
  `;
  document.head.appendChild(style);

  const wrap = document.createElement('div');
  wrap.className = 'wooa-orig-wrap';
  wrap.innerHTML = `
    <div class="wooa-orig-header">
      <span class="wooa-orig-dot"></span>
      <span class="wooa-orig-label">👀 こちらもいかがですか？</span>
    </div>
    <p class="wooa-orig-sub">WooaHouseの他の無料ツール</p>
    <div class="wooa-orig-grid">
      ${picks.map(s => `
        <a href="${s.url}?utm_source=${utmSource}&utm_medium=originals&utm_campaign=wooahouse" class="wooa-orig-card" style="--wooa-color:${s.color}" target="_blank" rel="noopener">
          <div class="wooa-orig-top">
            <span class="wooa-orig-icon">${s.icon}</span>
            <span class="wooa-orig-badge">${s.badge}</span>
          </div>
          <div class="wooa-orig-title">${s.title}</div>
          <div class="wooa-orig-desc">${s.desc}</div>
          <div class="wooa-orig-link">今すぐ →</div>
        </a>
      `).join('')}
    </div>
  `;

  const anchor = document.querySelector('.wooa-orig-anchor');
  const toolsSection = document.querySelector('.tools-section');
  if (anchor) anchor.replaceWith(wrap);
  else if (toolsSection) toolsSection.prepend(wrap);
  else {
    const fallback = document.querySelector('footer');
    if (fallback) fallback.before(wrap);
    else document.body.appendChild(wrap);
  }

  if (!isToolPage) {
    requestAnimationFrame(() => {
      const grid = wrap.querySelector('.wooa-orig-grid');
      if (!grid || grid.children.length < 2) return;
      const items = [...grid.children];
      const topFirst = Math.round(items[0].getBoundingClientRect().top);
      const perRow = items.filter(el => Math.round(el.getBoundingClientRect().top) === topFirst).length;
      if (perRow < 1 || perRow >= items.length) return;
      const rem = items.length % perRow;
      if (rem !== 0) items.slice(-rem).forEach(el => el.remove());
    });
  }
})();
