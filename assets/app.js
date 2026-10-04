(function () {
  const news = Array.isArray(window.AI_NEWS_DATA) ? [...window.AI_NEWS_DATA] : [];
  const sorted = news.sort((a, b) => new Date(b.date) - new Date(a.date));
  const state = { filter: "all", query: "" };

  const $ = (selector, root = document) => root.querySelector(selector);
  const grid = $("#news-grid");
  const featured = $("#featured-story");
  const timeline = $("#timeline-list");
  const ticker = $("#daily-ticker");
  const resultLine = $("#result-line");
  const emptyState = $("#empty-state");
  const searchInput = $("#search-input");
  const filterRoot = $("#filters");

  const escapeHTML = (value = "") =>
    String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  const formatDate = (date) => {
    const d = new Date(date);
    return new Intl.DateTimeFormat("zh-CN", {
      month: "2-digit",
      day: "2-digit",
      timeZone: "Asia/Shanghai"
    }).format(d).replace("/", ".");
  };

  function renderFeatured() {
    const item = sorted.find((entry) => entry.featured) || sorted[0];
    if (!item || !featured) return;

    featured.innerHTML = `
      <div class="feature-main">
        <div class="feature-meta">
          <span class="source-pill"><i>${escapeHTML(item.brand)}</i>${escapeHTML(item.source)}</span>
          <span>${escapeHTML(item.dateLabel)}</span>
          <span>·</span>
          <span>${escapeHTML(item.category)}</span>
        </div>
        <h3>${escapeHTML(item.title)}</h3>
        <p class="feature-summary">${escapeHTML(item.summary)}</p>
        <div class="feature-facts">
          <div class="fact">
            <small>为什么重要</small>
            <p>${escapeHTML(item.background)}</p>
          </div>
          <div class="fact">
            <small>核心变化</small>
            <p>${escapeHTML(item.signal)}</p>
          </div>
        </div>
      </div>
      <div class="feature-side">
        <span class="side-label">VERIFIED NOTE / 01</span>
        <h4>${escapeHTML(item.content)}</h4>
        <p>不把厂商宣传语直接当作事实结论。正文中的能力、价格与范围均保留原始出处。</p>
        <div class="side-divider"></div>
        <div class="verification-row">
          <b>${escapeHTML(item.verification.level)}</b>
          <div>
            <small>核验状态</small>
            <strong>${escapeHTML(item.verification.label)}</strong>
          </div>
        </div>
        <a class="feature-link" href="${escapeHTML(item.url)}" target="_blank" rel="noopener noreferrer">打开官方原文 <span>↗</span></a>
      </div>
    `;
  }

  function renderTicker() {
    if (!ticker) return;
    const items = sorted.slice(0, 4);
    ticker.innerHTML = `<span>${items
      .map((item) => `<b>${escapeHTML(item.source)}</b> · ${escapeHTML(item.title)}`)
      .join("　　◆　　")}</span>`;
  }

  function renderTimeline() {
    if (!timeline) return;
    timeline.innerHTML = sorted
      .map(
        (item) => `
        <article class="timeline-item">
          <time class="timeline-date" datetime="${escapeHTML(item.date)}">${escapeHTML(item.dateLabel)}</time>
          <div class="timeline-content">
            <small>${escapeHTML(item.source)} / ${escapeHTML(item.category)}</small>
            <h3>${escapeHTML(item.title)}</h3>
            <p>${escapeHTML(item.signal)}</p>
            <a href="${escapeHTML(item.url)}" target="_blank" rel="noopener noreferrer">查看原始来源 ↗</a>
          </div>
        </article>
      `
      )
      .join("");
  }

  function cardTemplate(item) {
    return `
      <article class="news-card reveal" data-category="${escapeHTML(item.categoryKey)}">
        <div class="card-top">
          <div class="card-source">
            <span class="brand-badge">${escapeHTML(item.brand)}</span>
            <span>
              <strong>${escapeHTML(item.source)}</strong>
              <small>${escapeHTML(item.sourceKind)}</small>
            </span>
          </div>
          <time class="card-date" datetime="${escapeHTML(item.date)}">${escapeHTML(item.dateLabel)}</time>
        </div>
        <span class="category-tag">${escapeHTML(item.category)}</span>
        <h3>${escapeHTML(item.title)}</h3>
        <p class="card-summary">${escapeHTML(item.summary)}</p>
        <div class="card-details">
          <div class="detail-row">
            <b>背景</b>
            <p>${escapeHTML(item.background)}</p>
          </div>
          <div class="detail-row">
            <b>内容</b>
            <p>${escapeHTML(item.content)}</p>
          </div>
        </div>
        <div class="card-footer">
          <div class="verify-inline" title="${escapeHTML(item.verification.note)}">
            <span class="verify-grade">${escapeHTML(item.verification.level)}</span>
            <span>${escapeHTML(item.verification.label)}</span>
          </div>
          <a class="source-link" href="${escapeHTML(item.url)}" target="_blank" rel="noopener noreferrer">原文 ↗</a>
        </div>
      </article>
    `;
  }

  function filteredNews() {
    const query = state.query.trim().toLowerCase();
    return sorted.filter((item) => {
      const matchesFilter = state.filter === "all" || item.categoryKey === state.filter;
      const haystack = [item.title, item.summary, item.background, item.content, item.source, ...(item.tags || [])]
        .join(" ")
        .toLowerCase();
      return matchesFilter && (!query || haystack.includes(query));
    });
  }

  function updateGrid(animate = true) {
    if (!grid) return;
    const items = filteredNews();
    grid.innerHTML = items.map(cardTemplate).join("");
    if (resultLine) resultLine.textContent = `显示 ${items.length} / ${sorted.length} 条，按官方发布时间倒序`;
    if (emptyState) emptyState.hidden = items.length !== 0;
    if (animate) requestAnimationFrame(observeReveals);
  }

  let observer;
  function observeReveals() {
    const elements = document.querySelectorAll(".reveal:not(.is-visible)");
    if (!("IntersectionObserver" in window)) {
      elements.forEach((el) => el.classList.add("is-visible"));
      return;
    }
    if (!observer) {
      observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.08, rootMargin: "0px 0px -30px" }
      );
    }
    elements.forEach((el) => observer.observe(el));
  }

  filterRoot?.addEventListener("click", (event) => {
    const button = event.target.closest(".filter");
    if (!button) return;
    state.filter = button.dataset.filter || "all";
    filterRoot.querySelectorAll(".filter").forEach((el) => el.classList.toggle("is-active", el === button));
    updateGrid();
  });

  searchInput?.addEventListener("input", (event) => {
    state.query = event.target.value || "";
    updateGrid();
  });

  renderFeatured();
  renderTicker();
  renderTimeline();
  updateGrid();
  document.querySelector("#metric-count")?.replaceChildren(document.createTextNode(String(sorted.length)));
})();
